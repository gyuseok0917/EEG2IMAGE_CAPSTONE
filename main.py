from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction
from PyQt6 import  uic
from gui_class.Upload import UploadCompleteWindow, UploadWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        uic.loadUi('./ui/main.ui', self)
        self.initUI()

    def initUI(self):
        upload_btn = self.findChild(QPushButton, "uploadButton") # ui에 정의된 버튼을 uploadButton 변수로 할당.
        upload_btn.clicked.connect(lambda: UploadWindow().show())
     
      
        
    
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
