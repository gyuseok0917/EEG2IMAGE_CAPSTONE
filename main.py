import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import *
from PyQt6 import  uic, QtGui, QtCore
from gui_class import UploadWindow, eeg_plot

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        uic.loadUi('./ui/main.ui', self)

        self.initUI()
        self.eeg_graph()

    def initUI(self):
        self.uploadWindow = UploadWindow()
        self.origin_image_frame = self.findChild(QFrame, 'origin_image_frame')

        self.uploadButton.clicked.connect(self.showUploadWindow) 
           # main.ui에 'uploadButton' 이 존재하기 때문에 findChidren 해줄 필요없음
        

           #uploadWindow 클래스(Upload.py)내에 존재하는 btn_UP_open 끌어옴. 

    def showUploadWindow(self):
        self.uploadWindow.btn_UP_open.clicked.connect(self.displayImage)
        
        self.uploadWindow.show()

    def eeg_graph(self):
        eeg_widget = self.findChild(pg.PlotWidget, "graph")
        eeg_plot(eeg_widget, np.random.randn(8, 500))

    
    def displayImage(self):  # 이미지 띄우기
        if self.uploadWindow.filePath:  # 파일 경로가 있는 경우
            
            label = QLabel(self.origin_image_frame)  # 레이블 생성
            pixmap = QtGui.QPixmap(self.uploadWindow.filePath)  # QPixmap 객체 생성
            label.setPixmap(pixmap)  # 레이블에 QPixmap 객체 설정
            label.setGeometry(0, 0, self.origin_image_frame.width(), self.origin_image_frame.height())  # 레이블의 위치와 크기 설정
            label.setScaledContents(True)  # 이미지의 크기를 레이블 크기에 맞추어 조정   
            label.show()  # 레이블 보이기



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()