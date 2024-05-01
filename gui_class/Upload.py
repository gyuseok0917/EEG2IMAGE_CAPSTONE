from PyQt6 import QtWidgets, uic, QtGui, QtCore

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
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'OPEN', QtCore.QDir.homePath(), filters)
        if fname:
            self.lineEdit.setText(fname)
            self.filePath = fname  # 파일 경로 저장
        

          
class UploadWindow_eeg(QtWidgets.QDialog):  # 업로드 창
    def __init__(self):
        super(UploadWindow_eeg, self).__init__()
        uic.loadUi('./ui/uploadWindow.ui', self)
        self.lineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.lineEdit.mousePressEvent = self.openFileDialog
        self.EEG_upload_btn = self.findChild(QtWidgets.QPushButton, 'btn_UP_open')  # 버튼 요소 찾기 
        
        self.filePath1 = ""  # 파일 경로를 저장할 변수 추가

        # displayImage 메소드를 버튼 클릭 시그널에 연결합니다.

        self.EEG_upload_btn.clicked.connect(self.close)
        #btn_UP_open이 눌렸을 때, self.close == 현재 클래스(창)을 닫음. 
        # 업로드윈도우에 이 코드가 있으므로 이 창이 꺼짐.
    
    def openFileDialog(self,event):
        filters = "EEG file (*.fif);"
        fname1, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'OPEN', QtCore.QDir.homePath(), filters)
        if fname1:
            self.lineEdit.setText(fname1)
            self.filePath = fname1  # 파일 경로 저장