import mne
import os
import numpy as np
import base64
import zlib
import json
import pickle
from mne.io.fiff.raw import Raw
from mne import Info
from PyQt6 import uic, QtCore
from PyQt6.QtCore import pyqtSignal, QUrl
from PyQt6.QtWidgets import *
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


class UPLOADWINDOW_IMG(QDialog):  # 업로드 창
    file_selected = pyqtSignal()  # 시그널 정의
    def __init__(self):
        super(UPLOADWINDOW_IMG, self).__init__()
        uic.loadUi('./ui/uploadWindow.ui', self)
        self.lineEdit = self.findChild(QLineEdit, 'lineEdit')
        self.lineEdit.mousePressEvent = self.OPEN_IMAGE_FILE_DIALOG
        self.filePath = ""  # 파일 경로를 저장할 변수 추가
        self.btn_UP_open.clicked.connect(self.close)

    def OPEN_IMAGE_FILE_DIALOG(self, event):
        OPEN_FILE_DIALOG(self, 'Image file Open', 'Image files (*.png *.jpg *.jpeg *.bmp);', self.lineEdit)
        self.file_selected.emit()  # 시그널 발행

class UPLOADWINDOW_EEG(QDialog):
    # EEG 데이터 수신 시그널 (Raw type)
    eegDataReceived = pyqtSignal(Raw)
    # 채널 수 변경 수신 시그널
    selectChannelReceived = pyqtSignal(Raw)
    # 이미지 데이터 수신 시그널
    imageDataReceived = pyqtSignal(list)
    # 버튼 활성화 시그널
    file_selected = pyqtSignal()
    def __init__(self):
        super(UPLOADWINDOW_EEG, self).__init__()
        uic.loadUi('./ui/uploadWindow.ui', self)

        self.filePath = ""
        self.raw = None
        self.response_bytes = None
        self.new_raw = None
        self.lineEdit = self.findChild(QLineEdit, 'lineEdit')
        self.lineEdit.mousePressEvent = self.OPEN_EEG_FILE_DIALOG
        self.EEG_upload_btn = self.findChild(QPushButton, 'btn_UP_open')
        self.EEG_upload_btn.clicked.connect(self.EEG_DATALOAD)
        self.network_manager = QNetworkAccessManager(self)


    def OPEN_EEG_FILE_DIALOG(self, event):
        OPEN_FILE_DIALOG(self, 'EEG file Open', 'EEG file (*.fif);', self.lineEdit, self.EEG_DATALOAD)
        self.file_selected.emit()  # 시그널 발행

    def EEG_TO_IMAGE_GENERATION(self, number):
        # EEG DATA + NUMBER ==> SERVER transfer

        print("Image Number :", number)
        raw_bytes = pickle.dumps(self.raw)
        raw_base64 = base64.b64encode(raw_bytes).decode('utf-8')
        json_data = json.dumps({'eeg_data': raw_base64, "number": number})
        self.SEND_DATA(json_data)

    def SELECT_CHANNEL(self, n_ch):
        n_ch = int(n_ch.text()[:-2])
        eeg_channels = self.new_raw.info['ch_names'][:n_ch]
        picked_data = self.new_raw.copy().pick_channels(eeg_channels)
        self.selectChannelReceived.emit(picked_data)

    def EEG_DATALOAD(self):
        if self.filePath:
            try:
                self.raw = mne.io.read_raw_fif(self.filePath, preload=True)
                self.raw = self.raw.pick_types(eeg=True)
                if isinstance(self.raw, Raw):
                    print("데이터 로드 중")
                else:
                    print("로드된 데이터는 Raw 객체가 아닙니다. 데이터 형식:", type(self.raw))
            except Exception as e:
                print("EEG 데이터 로딩 오류:", e)
            finally:
                self.close()

    # EEG DATA 서버 전송
    def SEND_DATA(self, json_data):
        # 서버 URL 설정
        url = QUrl('http://210.119.103.61:5000/transfer')
        request = QNetworkRequest(url)
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, 'application/json')

        # 데이터 전송
        reply = self.network_manager.post(request, json_data.encode('utf-8'))
        reply.finished.connect(self.HANDLE_RESPONSE)

    # 서버 응답 처리 
    def HANDLE_RESPONSE(self):
        reply = self.sender()
        if reply.error() == QNetworkReply.NetworkError.NoError:
            response_data = reply.readAll()

            if response_data:
                self.response_bytes = bytes(response_data)

                try:
                    # 서버에서 받은 이미지 데이터 
                    json_data = json.loads(self.response_bytes)
                    image_list = json_data.get('images', [])
                    self.image_paths = []
                    for index, image_base64 in enumerate(image_list):
                        image_bytes = base64.b64decode(image_base64)
                        image_path = f"images/image_{index}.png"

                        with open(image_path, 'wb') as image_file:
                            image_file.write(image_bytes)
                            self.image_paths.append(image_path)

                    # for문 종료되면 호출 메소드 emit 실행 
                    self.imageDataReceived.emit(self.image_paths)

                    # 서버에서 받은 eeg 데이터 
                    encoded_data = json_data['eeg_data']

                    raw_bytes = base64.b64decode(encoded_data)
                    self.new_raw = pickle.loads(raw_bytes)
                    # 호출요청 (emit)
                    self.eegDataReceived.emit(self.new_raw)
                except json.JSONDecodeError:
                    print("Failed to decode JSON data.")
            else:
                print("Received empty data from server.")
        else:
            print("Network error occurred:", reply.errorString())


def OPEN_FILE_DIALOG(parent, dialog_title, filters, line_edit, callback=None):
    current_directory = os.getcwd()  # 현재 작업 디렉토리 가져오기
    fname, _ = QFileDialog.getOpenFileName(parent, dialog_title, current_directory, filters)
    if fname:
        line_edit.setText(fname)
        parent.filePath = fname
        if callback:
            callback()