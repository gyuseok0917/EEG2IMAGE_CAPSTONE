import time
import sys
import os
import pyqtgraph as pg
import numpy as np
# MNE 명명규칙을 따르지않을 때 나타나는 콘솔 오류 안보이도록 설정
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
from mne.io import RawArray
from mne.io.fiff import Raw
from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import *
from gui_class import UPLOADWINDOW_IMG, EEGPlotter, TOPOMAP, UPLOADWINDOW_EEG, ImageSlider, GT_EEG_UPLOAD


# File Menu -> New Open 클릭 시
def Restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('./ui/main.ui', self)  # UI 파일 로드
        self.initUI()  # UI 초기화 함수 호출

    def initUI(self):
        self.uploadWindow = UPLOADWINDOW_IMG()  # 업로드 창 인스턴스 생성
        self.eeg_uploadWindow = UPLOADWINDOW_EEG()  # EEG 업로드 창 인스턴스 생성
        self.GT_eeg_uploadWindow = GT_EEG_UPLOAD()

        # UI 요소들을 찾고 연결
        self.create_image_widget = QLabel(self.findChild(QWidget, 'create_image_widget'))
        self.create_image_widget.setGeometry(
            0, 0, self.create_image_widget.parent().width(),
            self.create_image_widget.parent().height())  # 레이블 크기 설정

        # 이미지 크기를 레이블에 맞추기
        self.create_image_widget.setScaledContents(True)
        # 로딩 애니메이션 설정
        self.loading_movie = QMovie("loading.gif")
        self.create_image_widget.setMovie(self.loading_movie)

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

        # imageDataReceived 호출
        self.eeg_uploadWindow.imageDataReceived.connect(self.DISPLAY_IMAGE_SERVER_CREATE)
        # eegDataReceived 호출
        self.eeg_uploadWindow.eegDataReceived.connect(self.EEG_GRAPH)
        # 채널 변경 호출
        self.eeg_uploadWindow.selectChannelReceived.connect(self.EEG_GRAPH)

        # 라디오 버튼 클릭시 graph 위젯 초기화
        self.Radio_btn.buttonClicked.connect(self.EEG_WIDGET_CLEAR)
        self.startButton.setEnabled(False)  # 시작버튼 비활성화
        # 시그널과 슬롯 연결
        self.eeg_uploadWindow.file_selected.connect(self.EEG_OPEN_COMPLETIED)
        self.New_open.triggered.connect(Restart_program)

        # 버튼 클릭 시 연결될 함수 설정
        self.Grount_Truth_EEG_OPEN.triggered.connect(self.SHOW_UPLOAD_WINDOW_GT_EEG_OPEN)
        self.Ground_Truth_Image_OPEN.triggered.connect(self.SHOW_UPLOAD_WINDOW_IMG)
        self.EEG_upload.clicked.connect(self.SHOW_UPLOAD_WINDOW_EEG)
        self.startButton.clicked.connect(self.HANDLE_START)

    def EEG_Header_widget(self):
        # Header_table 위젯에 대한 참조 생성
        self.eeg_table_view = self.findChild(QTableView, "Header_eeg_table_view")

        eeg_raw_data = self.eeg_uploadWindow.raw # Upload.py raw
        if eeg_raw_data is not None:
            self.table_widget = QTableWidget(self.eeg_table_view) # 테이블 위젯 생성
            self.table_widget.setFixedSize(self.eeg_table_view.size()) # 테이블 크기 설정

            data = [
                ["Number of Channel", f"{eeg_raw_data.info['nchan']} EEG"],
                ["Sampling Rate", f"{eeg_raw_data.info['sfreq']} [Hz]"],
                ["Duration", f"{round(len(eeg_raw_data.times) / eeg_raw_data.info['sfreq'], 4)} [s]"],
            ]
            # 데이터 채우기
            self.table_widget.setRowCount(len(data))
            self.table_widget.setColumnCount(len(data[0]))
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    self.table_widget.setItem(i, j, QTableWidgetItem(item))

            # Header_table에 테이블 위젯 추가
            layout = QVBoxLayout(self.eeg_table_view)
            layout.addWidget(self.table_widget)

    def EEG_OPEN_COMPLETIED(self): # EEG 파일 업로드 완료시 START 버튼 활성화
        self.startButton.setEnabled(True)  # 시작버튼 활성화
        self.EEG_Header_widget()
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
        (self.eeg_uploadWindow.EEG_upload_btn.clicked
         .connect(self.eeg_uploadWindow.OPEN_EEG_FILE_DIALOG))

    # GT_EEG 업로드 창
    def SHOW_UPLOAD_WINDOW_GT_EEG_OPEN(self):
        self.GT_eeg_uploadWindow.show()
        self.GT_eeg_uploadWindow.EEG_GT_upload_btn.clicked.connect(self.handle_GT_EEG_upload)
        time.sleep(1)
        self.eeg_widget.clear()
    def handle_GT_EEG_upload(self):
         self.EEG_GRAPH(self.eeg_uploadWindow.new_raw, self.GT_eeg_uploadWindow.raw)

    # 시작 버튼 클릭 시 실행될 함수
    def HANDLE_START(self):
        self.startButton.setEnabled(False)  # 시작버튼 비활성화
        number = self.ImageNumber.value()  # 생성할 이미지 개수 정보 가져오기
        self.eeg_uploadWindow.EEG_TO_IMAGE_GENERATION(number)  # 시각화 생성 함수 호출
        self.loading_movie.start()  # 로딩 애니메이션 시작


    # 업로드된 이미지 표시
    def DISPLAY_IMAGE_ORIGIN(self):
        if self.uploadWindow.filePath:  # 파일 경로가 있는 경우
            label = QLabel(self.Image_tab)  # 레이블 생성
            pixmap = QPixmap(self.uploadWindow.filePath)  # QPixmap 객체 생성
            label.setPixmap(pixmap)  # 레이블에 QPixmap 객체 설정
            label.setGeometry(0, 0, self.Image_tab.width(), self.Image_tab.height())  # 레이블 크기 설정
            label.setScaledContents(True)  # 이미지 크기를 레이블에 맞추기
            label.show()  # 레이블 표시

    # 서버에서 받은 이미지 표시
    def DISPLAY_IMAGE_SERVER_CREATE(self, paths):
        self.imageSlider.image_paths = paths
        if self.imageSlider.image_paths:
            self.loading_movie.stop()  # 로딩 애니메이션 중지
            self.imageSlider.current_index = 0
            self.imageSlider.images_slice()

            # 버튼 활성화
            self.startButton.setEnabled(False)
            self.EEG_upload.setEnabled(False)
        # score frame 활성화
        # 서버에서 받은 이미지와 비교해야하므로 이 곳에 위치
        self.evaluation_score_frame()


    def evaluation_score_frame(self):
        # evaluation score 함수
        self.score_label = QLabel(self) # QLabel 생성
        score = 85  # 임시 데이터
        self.score_label.setText(str(score))

        # QLabel을 evaluation_score QFrame에 추가
        layout = QVBoxLayout(self.evaluation_score)
        layout.addWidget(self.score_label)

        # 서버에서 받은 EEG 그래프 표시
    def EEG_GRAPH(self, generate_eeg, gt_eeg = None):
        if isinstance(generate_eeg, RawArray):
            if gt_eeg is None:
                self.plotter = EEGPlotter(self.eeg_widget, generate_eeg)
            else:
                self.plotter = EEGPlotter(self.eeg_widget, generate_eeg, gt_eeg)
            self.plotter.regionChanged.connect(self.TOPO_SHOW)
        else:
            print("EEG_GRAPH is not a NumPy array. TYPE:", type(generate_eeg))

    # Topomap 표시 함수
    def TOPO_SHOW(self, tmin, tmax):
        image = TOPOMAP(self.plotter.generate_sr_eeg, tmin, tmax)  # Topomap 이미지 생성
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
