from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6 import QtWidgets, uic, QtCore, QtGui

class UploadCompleteWindow(QtWidgets.QDialog):
    def __init__(self):
        super(UploadCompleteWindow, self).__init__()
        uic.loadUi('uploadCompleteWindow.ui', self) 
        self.confirmButton = self.findChild(QtWidgets.QPushButton, 'confirmButton') 
        self.confirmButton.clicked.connect(self.close)

class UploadWindow(QtWidgets.QDialog):  #업로드 창
    def __init__(self):
        super(UploadWindow, self).__init__()
        uic.loadUi('uploadWindow.ui', self) 
        self.lineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit') 
        self.lineEdit.mousePressEvent = self.openFileDialog
        self.uploadButton = self.findChild(QtWidgets.QPushButton, 'uploadButton') 
        self.uploadButton.clicked.connect(self.showUploadCompleteWindow)

    def openFileDialog(self, event):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname:
            self.lineEdit.setText(fname) 

    def showUploadCompleteWindow(self):
        self.uploadCompleteWindow = UploadCompleteWindow()
        self.uploadCompleteWindow.show()
        self.uploadCompleteWindow.confirmButton.clicked.connect(self.close) 

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        uic.loadUi('main.ui', self)
        self.initUI()

    def initUI(self):
        file_menu = self.menuBar().findChild(QMenu, 'menuFile') 
        upload_action = QtGui.QAction('Upload', self)  
        upload_action.triggered.connect(self.showUploadWindow) 
        file_menu.addAction(upload_action)  
        
    def showUploadWindow(self):
        self.uploadWindow = UploadWindow()
        self.uploadWindow.show()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
