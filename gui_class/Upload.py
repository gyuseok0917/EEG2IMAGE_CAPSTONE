
from PyQt6 import QtWidgets, uic

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

    def openFileDialog(self, event):
        filters = "Image files (*.png *.jpg *.jpeg *.bmp);;All files (*.*)"
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'OPEN', '/home', filters)
        if fname:
            self.lineEdit.setText(fname) 

    def showUploadCompleteWindow(self):
        self.uploadCompleteWindow = UploadCompleteWindow()
        self.uploadCompleteWindow.show()
        self.uploadCompleteWindow.confirmButton.clicked.connect(self.close)