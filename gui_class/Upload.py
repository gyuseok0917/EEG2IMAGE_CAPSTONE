from PyQt6 import QtWidgets, uic, QtGui, QtCore
import mne
import numpy as np 


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
    def __init__(self):
        super(UploadWindow_eeg, self).__init__()
        uic.loadUi('./ui/uploadWindow.ui', self)
        self.lineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.lineEdit.mousePressEvent = self.openFileDialog
        self.EEG_upload_btn = self.findChild(QtWidgets.QPushButton, 'btn_UP_open')
        self.filePath = ""
        self.EEG_upload_btn.clicked.connect(self.loadAndClose)

    def openFileDialog(self, event):
        filters = "EEG file (*.fif);"
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'EEG file Open', QtCore.QDir.homePath(), filters)

        if fname:
            self.lineEdit.setText(fname)
            self.filePath = fname
          
    def loadAndClose(self):
        
        if self.filePath:
         
           
            print(self.filePath)
            try:
                raw = mne.io.read_raw_fif(self.filePath, preload=True)
                eeg_data = raw.get_data()
                print("데이터 로드 중, 데이터 유형 확인 중.")
                if isinstance(eeg_data, np.ndarray):
                    print("Upload.py Alert : 데이터는 NumPy 배열입니다.")
                else:
                    print("Upload.py Alert : 로드된 데이터는 NumPy 배열이 아닙니다. 데이터 형식:", type(eeg_data))
            except Exception as e:
                print("Upload.py Alert : Error loading EEG data:", e)
            finally:
                self.close()
            # try:
            #     print("Loading EEG data from:", self.filePath)
            #     raw = mne.io.read_raw_fif(self.filePath, preload=True)
            #     eeg_data = raw.get_data()
            #     print("Data loaded, checking data type...")
            #     if isinstance(eeg_data, np.ndarray):
            #         print("Data is a NumPy array.")
            #     else:
            #         print("Data loaded is not a NumPy array. Data type:", type(eeg_data))
            # except Exception as e:
            #     print("Error loading EEG data:", e)