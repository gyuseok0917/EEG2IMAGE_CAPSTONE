import numpy as np
import pyqtgraph as pg

from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction
from PyQt6 import  uic
from gui_class import UploadWindow, eeg_plot


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        uic.loadUi('./ui/main.ui', self)
        self.initUI()
        self.eeg_graph()

    def initUI(self):
        upload_action = self.findChild(QPushButton, 'uploadButton') 
        self.uploadButton.clicked.connect(self.showUploadWindow) 
        
    def showUploadWindow(self):
        self.uploadWindow = UploadWindow()
        self.uploadWindow.show()

    def eeg_graph(self):
        eeg_widget = self.findChild(pg.PlotWidget, "graph")
        eeg_plot(eeg_widget, np.random.randn(8, 500))
        
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()