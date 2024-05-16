import mne
import numpy as np 
import base64
import zlib
import json
import base64
from mne.io.fiff.raw import Raw
from PyQt6 import QtWidgets, uic, QtGui, QtCore
from PyQt6.QtCore import pyqtSignal, QUrl
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


class UploadWindow(QtWidgets.QDialog):  # 업로드 창
    def __init__(self):
        super(UploadWindow, self).__init__()
        uic.loadUi('./ui/uploadWindow.ui', self)
        self.lineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.lineEdit.mousePressEvent = self.openFileDialog
        self.btn_UP_open = self.findChild(QtWidgets.QPushButton, 'btn_UP_open')  # 버튼 요소 찾기 
        
        self.filePath = ""  # 파일 경로를 저장할 변수 추가

        # displayImage 메소드를 버튼 클릭 시그널에 연결합니다.

        self.btn_UP_open.clicked.connect(self.close)
        #btn_UP_open이 눌렸을 때, self.close == 현재 클래스(창)을 닫음. 
        # 업로드윈도우에 이 코드가 있으므로 이 창이 꺼짐.
    
    def openFileDialog(self,event):
        filters = "Image files (*.png *.jpg *.jpeg *.bmp);"
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Image file Open', QtCore.QDir.homePath(), filters)
        if fname:
            self.lineEdit.setText(fname)
            self.filePath = fname  # 파일 경로 저장
   

class UploadWindow_eeg(QtWidgets.QDialog):
    eegDataLoaded = pyqtSignal(Raw)
    imageDataReceived = pyqtSignal(list)  # list 타입으로 신호 정의

    def __init__(self):
        super(UploadWindow_eeg, self).__init__()
        uic.loadUi('./ui/uploadWindow.ui', self)

        self.filePath = ""
        self.raw = None
        self.response_bytes = None

        self.lineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.lineEdit.mousePressEvent = self.openFileDialog
        self.EEG_upload_btn = self.findChild(QtWidgets.QPushButton, 'btn_UP_open')
        self.EEG_upload_btn.clicked.connect(self.loadAndClose)
        self.network_manager = QNetworkAccessManager(self)

    def openFileDialog(self, event):
        filters = "EEG file (*.fif);"
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'EEG file Open', QtCore.QDir.homePath(), filters)

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

        self.eegDataLoaded.emit(self.raw)

    def loadAndClose(self):
        if self.filePath:
            try:
                self.raw = mne.io.read_raw_fif(self.filePath, preload=True)
                self.raw = self.raw.pick_types(eeg=True)
                if isinstance(self.raw, Raw):
                    print("데이터 로드 중, 데이터 유형 확인 중.")
                else:
                    print("로드된 데이터는 Raw 객체가 아닙니다. 데이터 형식:", type(self.raw))
            except Exception as e:
                print("EEG 데이터 로딩 오류:", e)
            finally:
                self.close()

    def send_data(self, json_data):
        # 서버 URL 설정
        url = QUrl('http://210.119.103.61:5000/transfer')
        request = QNetworkRequest(url)
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, 'application/json')
        
        # 데이터 전송
        reply = self.network_manager.post(request, json_data.encode('utf-8'))
        reply.finished.connect(self.handle_response)

    def handle_response(self):
        reply = self.sender()
        if reply.error() == QNetworkReply.NetworkError.NoError:
            response_data = reply.readAll()
            
            if response_data:
                self.response_bytes = bytes(response_data)
                
                try:
                    json_data = json.loads(self.response_bytes)
                    print("JSON Data:", json_data)  # JSON 데이터 출력하여 구조 확인
                    
                    image_list = json_data.get('images', [])
                    
                    self.image_paths = []
                    for index, image_base64 in enumerate(image_list):
                        print("Image Data:", image_base64)  # 확인용 출력
                        
                        image_bytes = base64.b64decode(image_base64)
                        image_path = f"image_{index}.png"
                        
                        with open(image_path, 'wb') as image_file:
                            image_file.write(image_bytes)
                        
                        self.image_paths.append(image_path)
                    
                    self.imageDataReceived.emit(self.image_paths)  # list 타입으로 emit
                    
                except json.JSONDecodeError:
                    print("Failed to decode JSON data.")
            else:
                print("Received empty data from server.")
        else:
            print("Network error occurred:", reply.errorString())
    eegDataLoaded = pyqtSignal(Raw)
    # imageDataReceived = pyqtSignal(bytes)  # 이미지 데이터 수신 신호
    imageDataReceived = QtCore.pyqtSignal(list)
    def __init__(self):
        super(UploadWindow_eeg, self).__init__()
        uic.loadUi('./ui/uploadWindow.ui', self)


        self.filePath = ""
        self.raw = None
        self.response_bytes = None

        self.lineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.lineEdit.mousePressEvent = self.openFileDialog
        self.EEG_upload_btn = self.findChild(QtWidgets.QPushButton, 'btn_UP_open')
        self.EEG_upload_btn.clicked.connect(self.loadAndClose)
        self.network_manager = QNetworkAccessManager(self)

    def openFileDialog(self, event):
        filters = "EEG file (*.fif);"
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'EEG file Open', QtCore.QDir.homePath(), filters)

        if fname:
            self.lineEdit.setText(fname)
            self.filePath = fname
            self.loadAndClose()


    def generation_visualization(self, number):
        print("Image Number :",number)
        data = self.raw.get_data()  
        data_bytes = data.tobytes()
        compressed_data = zlib.compress(data_bytes)
        encoded_data = base64.b64encode(compressed_data).decode('utf-8')
                
        json_data = json.dumps({'eeg_data': encoded_data, "shape": (data.shape), "number": number})
        self.send_data(json_data)

        self.eegDataLoaded.emit(self.raw)

       
    def loadAndClose(self):
        if self.filePath:
            try:
                self.raw = mne.io.read_raw_fif(self.filePath, preload=True)
                self.raw = self.raw.pick_types(eeg=True)
                if isinstance(self.raw, Raw):
                    print("데이터 로드 중, 데이터 유형 확인 중.")
                else:
                    print("로드된 데이터는 Raw 객체가 아닙니다. 데이터 형식:", type(self.raw))
            except Exception as e:
                print("EEG 데이터 로딩 오류:", e)
            finally:
                self.close()

    def send_data(self, json_data):
        # 서버 URL 설정
        url = QUrl('http://210.119.103.61:5000/transfer')
        request = QNetworkRequest(url)
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, 'application/json')
        
            # 데이터 전송
        reply = self.network_manager.post(request, json_data.encode('utf-8'))
        reply.finished.connect(self.handle_response)

    def handle_response(self):
            reply = self.sender()
            if reply.error() == QNetworkReply.NetworkError.NoError:
                response_data = reply.readAll()
                
                if response_data:
                    self.response_bytes = bytes(response_data)
                    
                    try:
                        json_data = json.loads(self.response_bytes)
                        print("JSON Data:", json_data)  # JSON 데이터 출력하여 구조 확인
                        
                        image_list = json_data.get('images', [])
                        
                        self.image_paths = []
                        for index, image_base64 in enumerate(image_list):
                            print("Image Data:", image_base64)  # 확인용 출력
                            
                            image_bytes = base64.b64decode(image_base64)
                            image_path = f"image_{index}.png"
                            
                            with open(image_path, 'wb') as image_file:
                                image_file.write(image_bytes)
                            
                            self.image_paths.append(image_path)
                        
                        self.imageDataReceived.emit(self.image_paths)  # list 타입으로 emit
                        
                    except json.JSONDecodeError:
                        print("Failed to decode JSON data.")
                else:
                    print("Received empty data from server.")
            else:
                print("Network error occurred:", reply.errorString())
            reply = self.sender()
            if reply.error() == QNetworkReply.NetworkError.NoError:
                response_data = reply.readAll()
                
                if response_data:
                    self.response_bytes = bytes(response_data)
                    
                    try:
                        json_data = json.loads(self.response_bytes)
                        print("JSON Data:", json_data)  # JSON 데이터 출력하여 구조 확인
                        
                        image_list = json_data.get('images', [])
                        
                        self.image_paths = []
                        for index, image_base64 in enumerate(image_list):
                            print("Image Data:", image_base64)  # 확인용 출력
                            
                            image_bytes = base64.b64decode(image_base64)
                            image_path = f"image_{index}.png"
                            
                            with open(image_path, 'wb') as image_file:
                                image_file.write(image_bytes)
                            
                            self.image_paths.append(image_path)
                        
                        self.imageDataReceived.emit(self.image_paths)  # list 타입으로 emit
                        
                    except json.JSONDecodeError:
                        print("Failed to decode JSON data.")
                else:
                    print("Received empty data from server.")
            else:
                print("Network error occurred:", reply.errorString())