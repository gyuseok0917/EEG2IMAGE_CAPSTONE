import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


class EEGTableApp(QMainWindow):
    def __init__(self, eeg_headers):
        super().__init__()

        self.setWindowTitle("EEG Header Information")
        self.setGeometry(100, 100, 600, 400)

        # 메인 위젯 설정
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # 레이아웃 설정
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # QTableWidget 생성
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        # 테이블 설정
        self.table_widget.setRowCount(len(eeg_headers))
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Header", "Value"])

        # 데이터 삽입
        for row, (header, value) in enumerate(eeg_headers.items()):
            self.table_widget.setItem(row, 0, QTableWidgetItem(header))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(value)))


def main():
    eeg_headers = {
        "Subject": "Subject_01",
        "Session": "Session_01",
        "Channels": 32,
        "Sampling Rate": "256 Hz",
        "Duration": "5 minutes"
    }

    app = QApplication(sys.argv)
    window = EEGTableApp(eeg_headers)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
