import pyqtgraph as pg
from mne.io.fiff.raw import Raw
from PyQt6.QtWidgets import *
from PyQt6 import  uic, QtGui
from gui_class import UploadWindow, EEGPlotter, topomap, UploadWindow_eeg



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        uic.loadUi('./ui/main.ui', self)
        self.initUI()
        

    def initUI(self):
        self.uploadWindow = UploadWindow()
        self.eeg_uploadWindow = UploadWindow_eeg()

        self.origin_image_frame = self.findChild(QFrame, 'origin_image_frame') # Image
        self.right_bottom_frame = self.findChild(QFrame, 'right_bottom_frame') # Topomap

        self.uploadButton.clicked.connect(self.showUploadWindow) 
           # main.ui에 'uploadButton' 이 존재하기 때문에 findChidren 해줄 필요없음
        self.EEG_upload.clicked.connect(self.showUploadWindow_eeg) 


    def showUploadWindow(self):
        self.uploadWindow.btn_UP_open.clicked.connect(self.displayImage)
        self.uploadWindow.show()


    def showUploadWindow_eeg(self):
        # 기존에 연결된 모든 신호를 제거하고 새로 연결 (여러 번 창을 열 때 중복 연결을 방지)
        self.eeg_uploadWindow.EEG_upload_btn.clicked.disconnect()
        self.eeg_uploadWindow.EEG_upload_btn.clicked.connect(self.eeg_uploadWindow.openFileDialog)

        # 사용자 정의 신호와 eeg_graph 메소드를 연결
        self.eeg_uploadWindow.eegDataLoaded.connect(self.eeg_graph)
        self.eeg_uploadWindow.show()


    def displayImage(self):  # 이미지 띄우기
        if self.uploadWindow.filePath:  # 파일 경로가 있는 경우
            
            label = QLabel(self.origin_image_frame)  # 레이블 생성
            pixmap = QtGui.QPixmap(self.uploadWindow.filePath)  # QPixmap 객체 생성
            label.setPixmap(pixmap)  # 레이블에 QPixmap 객체 설정
            label.setGeometry(0, 0, self.origin_image_frame.width(), self.origin_image_frame.height())  # 레이블의 위치와 크기 설정
            label.setScaledContents(True)  # 이미지의 크기를 레이블 크기에 맞추어 조정   
            label.show()  # 레이블 보이기


    def eeg_graph(self, raw_eeg):
        if isinstance(raw_eeg, Raw):
            eeg_widget = self.findChild(pg.PlotWidget, "graph")
            self.plotter = EEGPlotter(eeg_widget, raw_eeg)
            self.plotter.regionChanged.connect(self.topo_show)
        else:
            print("Main.py Alert : eeg_graph에 전달된 데이터는 Raw 객체가 아닙니다. 수신된 데이터 유형:", type(raw_eeg))


    def topo_show(self, tmin, tmax):
        image = topomap(self.plotter.raw_eeg, tmin, tmax)
        label = QLabel(self.right_bottom_frame)
        label.setPixmap(image)
        label.setGeometry(0, 0, self.right_bottom_frame.width(), self.right_bottom_frame.height())
        label.setScaledContents(True)
        label.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()