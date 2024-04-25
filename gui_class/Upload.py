from PyQt6 import QtWidgets, uic, QtGui, QtCore

class UploadWindow(QtWidgets.QDialog):  # 업로드 창
    def __init__(self):
        super(UploadWindow, self).__init__()
        uic.loadUi('./ui/uploadWindow.ui', self)
        self.lineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.lineEdit.mousePressEvent = self.openFileDialog
        self.btn_UP_open = self.findChild(QtWidgets.QPushButton, 'btn_UP_open')
        # displayImage 메소드를 버튼 클릭 시그널에 연결합니다.
        self.filePath = ""  # 파일 경로를 저장할 변수 추가
        self.btn_UP_open.clicked.connect(self.close)
        #btn_UP_open이 눌렸을 때, self.close == 현재 클래스(창)을 닫음. 
        # 업로드윈도우에 이 코드가 있으므로 이 창이 꺼짐.
    def openFileDialog(self, event):
        filters = "Image files (*.png *.jpg *.jpeg *.bmp);;All files (*.*)"
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'OPEN', QtCore.QDir.homePath(), filters)
        if fname:
            self.lineEdit.setText(fname)
            self.filePath = fname  # 파일 경로 저장
            

          
