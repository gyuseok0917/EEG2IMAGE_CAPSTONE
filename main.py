import time
import pyqtgraph as pg
import numpy as np

from mne.io.fiff.raw import Raw
from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import *
from gui_class import UPLOADWINDOW_IMG, EEGPlotter, TOPOMAP, UPLOADWINDOW_EEG, ImageSlider


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('./ui/main.ui', self)  # UI 파일 로드
        self.initUI()  # UI 초기화 함수 호출

    def initUI(self):
        self.uploadWindow = UPLOADWINDOW_IMG()  # 업로드 창 인스턴스 생성
        self.eeg_uploadWindow = UPLOADWINDOW_EEG()  # EEG 업로드 창 인스턴스 생성

        # UI 요소들을 찾고 연결
        self.create_image_widget = QLabel(self.findChild(QWidget, 'create_image_widget'))  # 서버에서 받은 이미지를 표시할 레이블
        self.create_image_widget.setGeometry(
            0, 0, self.create_image_widget.parent().width(),
            self.create_image_widget.parent().height())  # 레이블 크기 설정

        # 이미지 크기를 레이블에 맞추기
        self.create_image_widget.setScaledContents(True)
        # 로딩 애니메이션 설정
        self.loading_movie = QMovie("loading.gif")
        self.create_image_widget.setMovie(self.loading_movie)

        # 버튼 클릭 시 연결될 함수 설정
        self.uploadButton.clicked.connect(self.SHOW_UPLOAD_WINDOW_IMG)
        self.EEG_upload.clicked.connect(self.SHOW_UPLOAD_WINDOW_EEG)
        self.startButton.clicked.connect(self.HANDLE_START)

        # imageDataReceived 호출
        self.eeg_uploadWindow.imageDataReceived.connect(self.DISPLAY_IMAGE_SERVER_CREATE)
        # eegDataReceived 호출
        self.eeg_uploadWindow.eegDataReceived.connect(self.EEG_GRAPH)

        # 이미지 슬라이더 생성
        self.imageSlider = ImageSlider(self.create_image_widget, self.prevBtn, self.nextBtn)

        # EEG graph widget
        self.eeg_widget = self.findChild(pg.PlotWidget, "graph")

        # QButtonGroup에 라디오 버튼을 추가하고 ID 설정
        self.Radio_btn = QButtonGroup(self)
        self.Radio_btn.addButton(self.radioButton_8ch, 8)
        self.Radio_btn.addButton(self.radioButton_16ch, 16)
        self.Radio_btn.addButton(self.radioButton_32ch, 32)
        self.Radio_btn.addButton(self.radioButton_64ch, 64)
        self.Radio_btn.addButton(self.radioButton_128ch, 128)
        # 버튼 클릭 시그널에 슬롯 연결
        self.Radio_btn.buttonClicked.connect(self.EEG_WIDGET_CLEAR)

        self.eeg_uploadWindow.selectDataReceived.connect(self.EEG_GRAPH)

    def EEG_WIDGET_CLEAR(self, button):
        # 버튼 클릭시 eeg_graph WIDGET 초기화
        self.eeg_widget.clear()
        self.eeg_uploadWindow.SELECT_CHANNEL(button)

    # 이미지 업로드 창
    def SHOW_UPLOAD_WINDOW_IMG(self):
        self.uploadWindow.show()  # 업로드 창 표시
        self.uploadWindow.btn_UP_open.clicked.connect(self.DISPLAY_IMAGE_ORIGIN)

    # EEG 업로드 창
    def SHOW_UPLOAD_WINDOW_EEG(self):
        self.eeg_uploadWindow.show()
        self.eeg_uploadWindow.EEG_upload_btn.clicked.connect(self.eeg_uploadWindow.OPEN_EEG_FILE_DIALOG)

    # 시작 버튼 클릭 시 실행될 함수
    def HANDLE_START(self):
        self.startButton.setEnabled(False)  # 시작버튼 비활성화
        number = self.ImageNumber.value()  # 생성할 이미지 개수 정보 가져오기
        self.eeg_uploadWindow.IMAGE_GENERATION_VISUALIZATION(number)  # 시각화 생성 함수 호출
        self.loading_movie.start()  # 로딩 애니메이션 시작

    # 업로드된 이미지 표시
    def DISPLAY_IMAGE_ORIGIN(self):
        if self.uploadWindow.filePath:  # 파일 경로가 있는 경우
            label = QLabel(self.origin_image_frame)  # 레이블 생성
            pixmap = QPixmap(self.uploadWindow.filePath)  # QPixmap 객체 생성
            label.setPixmap(pixmap)  # 레이블에 QPixmap 객체 설정
            label.setGeometry(0, 0, self.origin_image_frame.width(), self.origin_image_frame.height())  # 레이블 크기 설정
            label.setScaledContents(True)  # 이미지 크기를 레이블에 맞추기
            label.show()  # 레이블 표시

    # 서버에서 받은 이미지 표시
    def DISPLAY_IMAGE_SERVER_CREATE(self, paths):
        self.imageSlider.image_paths = paths
        if self.imageSlider.image_paths:
            self.loading_movie.stop()  # 로딩 애니메이션 중지
            self.startButton.setEnabled(True)  # 버튼 활성화
            self.imageSlider.current_index = 0
            self.imageSlider.images_slice()

    # 서버에서 받은 EEG 그래프 표시
    def EEG_GRAPH(self, raw_eeg):
        if isinstance(raw_eeg, Raw):  # 전달된 데이터가 numpy 배열인 경우
            self.plotter = EEGPlotter(self.eeg_widget, raw_eeg)  # EEGPlotter 객체 생성
            self.plotter.regionChanged.connect(self.TOPO_SHOW)  # 영역 변경 신호에 topo_show 함수 연결
        else:
            print("Main.py Alert : EEG_GRAPH에 전달된 데이터는 numpy 배열이 아닙니다. 수신된 데이터 유형:", type(raw_eeg))

    # Topomap 표시 함수
    def TOPO_SHOW(self, tmin, tmax):
        image = TOPOMAP(self.plotter.raw_eeg, tmin, tmax)  # Topomap 이미지 생성
        label = QLabel(self.right_bottom_frame)  # 레이블 생성
        label.setPixmap(image)  # 레이블에 Topomap 이미지 설정
        label.setGeometry(0, 0,
                          self.right_bottom_frame.width(),
                          self.right_bottom_frame.height())  # 레이블 크기 설정
        label.setScaledContents(True)  # 이미지 크기를 레이블에 맞추기
        label.show()  # 레이블 표시


if __name__ == "__main__":
    app = QApplication([])  # QApplication 객체 생성
    window = MainWindow()  # MainWindow 객체 생성
    window.show()  # MainWindow 표시
    app.exec()  # 애플리케이션 실행
