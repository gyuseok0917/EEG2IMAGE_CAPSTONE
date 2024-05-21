import mne
import numpy as np 
import base64
import zlib
import json
from mne.io.fiff.raw import Raw
from mne import Info
from PyQt6 import  uic, QtCore
from PyQt6.QtCore import pyqtSignal, QUrl
from PyQt6.QtWidgets import *
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

class UploadWindow(QDialog):  # 업로드 창
    def __init__(self):
        super(UploadWindow, self).__init__()
        uic.loadUi('./ui/uploadWindow.ui', self)
        self.lineEdit = self.findChild(QLineEdit, 'lineEdit')
        self.lineEdit.mousePressEvent = self.openFileDialog
        self.filePath = ""  # 파일 경로를 저장할 변수 추가
        self.btn_UP_open.clicked.connect(self.close)
    
    def openFileDialog(self, event):
        filters = "Image files (*.png *.jpg *.jpeg *.bmp);"
        fname, _ = QFileDialog.getOpenFileName(self, 'Image file Open', QtCore.QDir.homePath(), filters)
        if fname:
            self.lineEdit.setText(fname)
            self.filePath = fname  # 파일 경로 저장


class UploadWindow_eeg(QDialog):
    eegDataReceived = pyqtSignal(np.ndarray, Info)
    imageDataReceived = pyqtSignal(list)  

    def __init__(self):
        super(UploadWindow_eeg, self).__init__()
        uic.loadUi('./ui/uploadWindow.ui', self)

        self.filePath = ""
        self.raw = None
        self.response_bytes = None

        self.lineEdit = self.findChild(QLineEdit, 'lineEdit')
        self.lineEdit.mousePressEvent = self.openFileDialog
        self.EEG_upload_btn = self.findChild(QPushButton, 'btn_UP_open')
        self.EEG_upload_btn.clicked.connect(self.loadAndClose)
        self.network_manager = QNetworkAccessManager(self)

    def openFileDialog(self, event):
        filters = "EEG file (*.fif);"
        fname, _ = QFileDialog.getOpenFileName(self, 'EEG file Open', QtCore.QDir.homePath(), filters)

        if fname:
            self.lineEdit.setText(fname)
            self.filePath = fname
            self.loadAndClose()

    def generation_visualization(self, number):
        print("Image Number :", number)
        data = self.raw.get_data()  
        data_bytes = data.tobytes()
        compressed_data = zlib.compress(data_bytes)
        encoded_data = base64.b64encode(compressed_data).decode('utf-8')
                
        json_data = json.dumps({'eeg_data': encoded_data, "shape": data.shape, "number": number})
        self.send_data(json_data)


    def loadAndClose(self):
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
    def send_data(self, json_data):
        # 서버 URL 설정
        url = QUrl('http://210.119.103.61:5000/transfer')
        request = QNetworkRequest(url)
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, 'application/json')
        
        # 데이터 전송
        reply = self.network_manager.post(request, json_data.encode('utf-8'))
        reply.finished.connect(self.handle_response)

    # 서버 응답 처리 
    def handle_response(self):
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
                    encoded_data = json_data['eeg_data'] # Encoded eeg data
                    data_shape = json_data["shape"]      # EEG data's shape
                    compressed_data = base64.b64decode(encoded_data) # Decode base64 format
                    data_bytes = zlib.decompress(compressed_data) # Restore compressed data
                    print('frombuffer shape print : ',np.frombuffer(data_bytes, dtype=np.float64).shape)
                    # Convert byte form to numpy matrix (reshape to size of original data)
                    data_array = np.frombuffer(data_bytes, dtype=np.float64).reshape(data_shape)

                    self.eegDataReceived.emit(data_array, self.raw.info)
                except json.JSONDecodeError:
                    print("Failed to decode JSON data.")
            else:
                print("Received empty data from server.")
        else:
            print("Network error occurred:", reply.errorString())
