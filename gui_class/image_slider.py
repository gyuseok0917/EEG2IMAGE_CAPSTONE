from PyQt6.QtGui import QPixmap

class ImageSlider:
    def __init__(self, create_image_widget, prevBtn, nextBtn):
        self.create_image_widget = create_image_widget
        self.prevBtn = prevBtn
        self.nextBtn = nextBtn
        self.image_paths = []
        self.current_index = 0
        self.initUI()

    def initUI(self):
        # 버튼 클릭 시 연결될 함수 설정
        self.prevBtn.clicked.connect(self.show_prev_image)
        self.nextBtn.clicked.connect(self.show_next_image)
        self.nextBtn.setStyleSheet("QPushButton { opacity: 0.2; }")
        self.prevBtn.setStyleSheet("QPushButton { opacity: 0.2; }")
    
    def show_next_image(self):
        if self.image_paths:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            self.images_slice()

    def show_prev_image(self):
        if self.image_paths:
            self.current_index = (self.current_index - 1) % len(self.image_paths)
            self.images_slice()

    def images_slice(self):
        if self.image_paths:
            pixmap = QPixmap(self.image_paths[self.current_index])  # 현재 인덱스의 이미지 파일 경로를 사용하여 QPixmap에 로드
            self.create_image_widget.setPixmap(pixmap)  # 레이블에 QPixmap 설정
            self.create_image_widget.show()  # 레이블 표시

    def enterEvent(self, event):
        self.prevBtn.setStyleSheet("QPushButton { opacity: 1.0; }")
        self.nextBtn.setStyleSheet("QPushButton { opacity: 1.0; }")

    def leaveEvent(self, event):
        self.prevBtn.setStyleSheet("QPushButton { opacity: 0.2; }")
        self.nextBtn.setStyleSheet("QPushButton { opacity: 0.2; }")
