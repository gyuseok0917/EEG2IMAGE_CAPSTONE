
from PyQt6 import QtWidgets, uic, QtCore, QtGui

class UploadCompleteWindow(QtWidgets.QDialog):
    def __init__(self):
        super(UploadCompleteWindow, self).__init__()
        uic.loadUi('./ui/uploadCompleteWindow.ui', self) 
        self.confirmButton = self.findChild(QtWidgets.QPushButton, 'confirmButton') 
        self.confirmButton.clicked.connect(self.close)

class UploadWindow(QtWidgets.QDialog):  #업로드 창
    def __init__(self):
        super(UploadWindow, self).__init__()
        uic.loadUi('./ui/uploadWindow.ui', self) 
        self.lineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit') 
        self.lineEdit.mousePressEvent = self.openFileDialog
        self.uploadButton = self.findChild(QtWidgets.QPushButton, 'uploadButton') 
        self.uploadButton.clicked.connect(self.showUploadCompleteWindow)
        self.filePath = None  # 파일 경로 초기화
        self.uploadCompleteWindow = UploadCompleteWindow()  # 업로드 완료 창 인스턴스 생성
        self.uploadCompleteWindow.confirmButton.clicked.connect(self.closeAndDisplayImage)

    def openFileDialog(self, event):
        filters = "Image files (*.png *.jpg *.jpeg *.bmp);;All files (*.*)"
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'OPEN', '/home', filters)
        if fname:
            self.lineEdit.setText(fname) 

    def showUploadCompleteWindow(self):
        self.uploadCompleteWindow = UploadCompleteWindow()
        self.uploadCompleteWindow.show()
        self.uploadCompleteWindow.confirmButton.clicked.connect(self.close)

    def displayImage(self):  # 이미지 띄우기 
        if self.uploadWindow.filePath:  # 파일 경로가 있는 경우
            image_widget = QtWidgets(self.origin_image_widget)  # 레이블 생성
            pixmap = QtGui.QPixmap(self.uploadWindow.filePath)  # QPixmap 객체 생성
            # 이미지 크기를 top_frame의 크기에 맞게 조절
            pixmap = pixmap.scaled(self.origin_image_widget.size(), QtCore.Qt.AspectRatioMode.IgnoreAspectRatio)
            image_widget.setPixmap(pixmap)  # 레이블에 QPixmap 객체 설정
            image_widget.show()  # 레이블 보이기  

    def closeAndDisplayImage(self):
        self.close()  # 업로드 창 닫기
        self.displayImage()  # 이미지 표시

      