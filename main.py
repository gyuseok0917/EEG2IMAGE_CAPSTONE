import pyqtgraph as pg
from mne.io.fiff.raw import Raw
from PyQt6.QtWidgets import *
from PyQt6 import uic, QtGui, QtCore
from gui_class import UploadWindow, EEGPlotter, topomap, UploadWindow_eeg

class MainWindow(QMainWindow):
    imageDataReceived = QtCore.pyqtSignal(list)  # 클래스 정의 맨 위에 신호 정의

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('./ui/main.ui', self)  # UI 파일 로드
        self.initUI()  # UI 초기화 함수 호출
        self.nextBtn.setStyleSheet("QPushButton { opacity: 0.2; }")
        self.prevBtn.setStyleSheet("QPushButton { opacity: 0.2; }")

    # UI 초기화 함수
    def initUI(self):
        self.uploadWindow = UploadWindow()  # 업로드 창 인스턴스 생성
        self.eeg_uploadWindow = UploadWindow_eeg()  # EEG 업로드 창 인스턴스 생성

        # UI 요소들을 찾고 연결
        self.origin_image_frame = self.findChild(QFrame, 'origin_image_frame')  # 원본 이미지를 표시할 프레임
        self.right_bottom_frame = self.findChild(QFrame, 'right_bottom_frame')  # Topomap을 표시할 프레임
        self.serverImageLabel = QLabel(self.findChild(QWidget, 'create_image_widget'))  # 서버에서 받은 이미지를 표시할 레이블
        self.serverImageLabel.setGeometry(0, 0, self.serverImageLabel.parent().width(),
                                          self.serverImageLabel.parent().height())  # 레이블 크기 설정
        self.serverImageLabel.setScaledContents(True)  # 이미지 크기를 레이블에 맞추기
        # 로딩 애니메이션 설정
        self.loading_movie = QtGui.QMovie("loading.gif")
        self.serverImageLabel.setMovie(self.loading_movie)
        # 버튼 클릭 시 연결될 함수 설정
        self.uploadButton.clicked.connect(self.showUploadWindow)
        self.EEG_upload.clicked.connect(self.showUploadWindow_eeg)
        self.eeg_uploadWindow.eegDataLoaded.connect(self.eeg_graph)  # EEG 데이터 로드 신호 연결
        self.eeg_uploadWindow.imageDataReceived.connect(self.update_image_paths)  # 이미지 데이터 수신 신호 연결
        self.startButton.clicked.connect(self.handle_start)

        self.image_paths = []
        self.current_index = 0
        # 생성 이미지 이전 버튼     
        self.prevBtn.clicked.connect(self.show_prev_image)    
        # 생성 이미지 다음 버튼 
        self.nextBtn.clicked.connect(self.show_next_image) 
        # 이미지 수신 신호 연결
        self.imageDataReceived.connect(self.update_image_paths)

    def update_image_paths(self, paths):
        self.image_paths = paths
        if self.image_paths:
            self.displayServerImage(self.image_paths[0])

    def displayServerImage(self, image_path):
        self.loading_movie.stop()  # 로딩 애니메이션 중지
        self.startButton.setEnabled(True)  # 버튼 활성화

        pixmap = QtGui.QPixmap()  # QPixmap 객체 생성
        pixmap.load(image_path)  # 이미지 파일 경로를 사용하여 QPixmap에 로드
        self.serverImageLabel.setPixmap(pixmap)  # 레이블에 QPixmap 설정
        self.serverImageLabel.show()  # 레이블 표시

    def show_next_image(self):
        if self.image_paths:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            self.displayServerImage(self.image_paths[self.current_index])

    def show_prev_image(self):
        if self.image_paths:
            self.current_index = (self.current_index - 1) % len(self.image_paths)
            self.displayServerImage(self.image_paths[self.current_index])

    def enterEvent(self, event):
        self.prevBtn.setStyleSheet("QPushButton { opacity: 1.0; }")
        self.nextBtn.setStyleSheet("QPushButton { opacity: 1.0; }")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.prevBtn.setStyleSheet("QPushButton { opacity: 0.2; }")
        self.nextBtn.setStyleSheet("QPushButton { opacity: 0.2; }")
        super().leaveEvent(event)

    # 시작 버튼 클릭 시 실행될 함수
    def handle_start(self):
        self.startButton.setEnabled(False)  # 버튼 비활성화
        number = self.ImageNumber.value()  # UI에서 설정한 이미지 번호 가져오기
        self.eeg_uploadWindow.generation_visualization(number)  # 시각화 생성 함수 호출
        self.loading_movie.start()  # 로딩 애니메이션 시작
        print("start loading")

    # 이미지 업로드 창 표시 함수
    def showUploadWindow(self):
        self.uploadWindow.btn_UP_open.clicked.connect(self.displayImage)  # 업로드 버튼 클릭 시 displayImage 함수 연결
        self.uploadWindow.show()  # 업로드 창 표시

    # EEG 업로드 창 표시 함수
    def showUploadWindow_eeg(self):
        # 기존에 연결된 모든 신호를 제거하고 새로 연결 (중복 연결 방지)
        self.eeg_uploadWindow.EEG_upload_btn.clicked.disconnect()
        self.eeg_uploadWindow.EEG_upload_btn.clicked.connect(self.eeg_uploadWindow.openFileDialog)
        self.eeg_uploadWindow.eegDataLoaded.connect(self.eeg_graph)
        self.eeg_uploadWindow.show()  # EEG 업로드 창 표시

    # 업로드된 이미지 표시 함수
    def displayImage(self):
        if self.uploadWindow.filePath:  # 파일 경로가 있는 경우
            label = QLabel(self.origin_image_frame)  # 레이블 생성
            pixmap = QtGui.QPixmap(self.uploadWindow.filePath)  # QPixmap 객체 생성
            label.setPixmap(pixmap)  # 레이블에 QPixmap 객체 설정
            label.setGeometry(0, 0, self.origin_image_frame.width(), self.origin_image_frame.height())  # 레이블 크기 설정
            label.setScaledContents(True)  # 이미지 크기를 레이블에 맞추기
            label.show()  # 레이블 표시

    # 서버에서 받은 이미지 표시 함수
    def displayServerImage(self, image_path):
        self.loading_movie.stop()  # 로딩 애니메이션 중지
        print("stop loading")
        self.startButton.setEnabled(True)  # 버튼 활성화

        pixmap = QtGui.QPixmap()  # QPixmap 객체 생성
        pixmap.load(image_path)  # 이미지 파일 경로를 사용하여 QPixmap에 로드
        self.serverImageLabel.setPixmap(pixmap)  # 레이블에 QPixmap 설정
        self.serverImageLabel.show()  # 레이블 표시

    # EEG 그래프 표시 함수
    def eeg_graph(self, raw_eeg):
        if isinstance(raw_eeg, Raw):  # 전달된 데이터가 Raw 객체인 경우
            eeg_widget = self.findChild(pg.PlotWidget, "graph")  # 그래프를 표시할 위젯 찾기
            self.plotter = EEGPlotter(eeg_widget, raw_eeg)  # EEGPlotter 객체 생성
            self.plotter.regionChanged.connect(self.topo_show)  # 영역 변경 신호에 topo_show 함수 연결
        else:
            print("Main.py Alert : eeg_graph에 전달된 데이터는 Raw 객체가 아닙니다. 수신된 데이터 유형:", type(raw_eeg))

    # Topomap 표시 함수
    def topo_show(self, tmin, tmax):
        image = topomap(self.plotter.raw_eeg, tmin, tmax)  # Topomap 이미지 생성
        label = QLabel(self.right_bottom_frame)  # 레이블 생성
        label.setPixmap(image)  # 레이블에 Topomap 이미지 설정
        label.setGeometry(0, 0, self.right_bottom_frame.width(), self.right_bottom_frame.height())  # 레이블 크기 설정
        label.setScaledContents(True)  # 이미지 크기를 레이블에 맞추기
        label.show()  # 레이블 표시

# 메인 함수
if __name__ == "__main__":
    app = QApplication([])  # QApplication 객체 생성
    window = MainWindow()  # MainWindow 객체 생성
    window.show()  # MainWindow 표시
    app.exec()  # 애플리케이션 실행
