import mne
import numpy as np 
from mne.io.fiff.raw import Raw
from PyQt6 import QtWidgets, uic, QtGui, QtCore
from PyQt6.QtCore import pyqtSignal

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
    def __init__(self):
        super(UploadWindow_eeg, self).__init__()
        uic.loadUi('./ui/uploadWindow.ui', self)
        self.lineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.lineEdit.mousePressEvent = self.openFileDialog
        self.EEG_upload_btn = self.findChild(QtWidgets.QPushButton, 'btn_UP_open')
        self.filePath = ""
        self.EEG_upload_btn.clicked.connect(self.loadAndClose)

    def openFileDialog(self):
        filters = "EEG file (*.fif);"
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'EEG file Open', QtCore.QDir.homePath(), filters)

        if fname:
            self.lineEdit.setText(fname)
            self.filePath = fname
            self.loadAndClose()
          
    def loadAndClose(self):
        
        if self.filePath:
         
           
            print(self.filePath)
            try:
                raw = mne.io.read_raw_fif(self.filePath, preload=True)
                raw = raw.pick_types(eeg = True)
                print("데이터 로드 중, 데이터 유형 확인 중.")
                if isinstance(raw, Raw):
                    print("Upload.py Alert : 데이터는 Raw 객체입니다.")
                    self.eegDataLoaded.emit(raw)
                else:
                    print("Upload.py Alert : 로드된 데이터는 Raw 객체가 아닙니다. 데이터 형식:", type(raw))
            except Exception as e:
                print("Upload.py Alert : Error loading EEG data:", e)
            finally:
                self.close()