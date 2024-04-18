import numpy as np
import pyqtgraph as pg

from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction
from PyQt6 import  uic

class UploadCompleteWindow(QDialog):
    def __init__(self):
        super(UploadCompleteWindow, self).__init__()
        uic.loadUi('./ui/uploadCompleteWindow.ui', self) 
        self.confirmButton = self.findChild(QPushButton, 'confirmButton') 
        self.confirmButton.clicked.connect(self.close)

class UploadWindow(QDialog):  #업로드 창
    def __init__(self):
        super(UploadWindow, self).__init__()
        uic.loadUi('./ui/uploadWindow.ui', self) 
        self.lineEdit = self.findChild(QLineEdit, 'lineEdit') 
        self.lineEdit.mousePressEvent = self.openFileDialog
        self.uploadButton = self.findChild(QPushButton, 'uploadButton') 
        self.uploadButton.clicked.connect(self.showUploadCompleteWindow)

    def openFileDialog(self, event):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname:
            self.lineEdit.setText(fname) 

    def showUploadCompleteWindow(self):
        self.uploadCompleteWindow = UploadCompleteWindow()
        self.uploadCompleteWindow.show()
        self.uploadCompleteWindow.confirmButton.clicked.connect(self.close) 

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        loadUi('./ui/main.ui', self)
        self.initUI()
        self.eeg_graph()

    def initUI(self):
        file_menu = self.menuBar().findChild(QMenu, 'menuFile') 
        upload_action = QAction('Upload', self)  
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
