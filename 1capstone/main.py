from PyQt6 import QtWidgets, uic, QtCore, QtGui

class UploadCompleteWindow(QtWidgets.QDialog):
    def __init__(self):
        super(UploadCompleteWindow, self).__init__()
        uic.loadUi('uploadCompleteWindow.ui', self) 
        self.confirmButton = self.findChild(QtWidgets.QPushButton, 'confirmButton') 
        self.confirmButton.clicked.connect(self.close)

class UploadWindow(QtWidgets.QDialog):  #업로드 창
    def __init__(self):
        super(UploadWindow, self).__init__()
        uic.loadUi('uploadWindow.ui', self) 
        self.lineEdit = self.findChild(QtWidgets.QLineEdit, 'lineEdit') 
        self.lineEdit.mousePressEvent = self.openFileDialog
        self.uploadButton = self.findChild(QtWidgets.QPushButton, 'uploadButton') 
        self.uploadButton.clicked.connect(self.showUploadCompleteWindow)

    def openFileDialog(self, event):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname:
            self.lineEdit.setText(fname) 

    def showUploadCompleteWindow(self):
        self.uploadCompleteWindow = UploadCompleteWindow()
        self.uploadCompleteWindow.show()
        self.uploadCompleteWindow.confirmButton.clicked.connect(self.close) 

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('test.ui', self)

        self.initUI()

    def initUI(self):
        uploadAction = QtGui.QAction('Upload', self)
        uploadAction.triggered.connect(self.showUploadWindow)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File') # 파일메뉴 바 추가
        fileMenu.addAction(uploadAction)   # 파일메뉴 하위 옵션 추가 

        toolMenu = menubar.addMenu('Tool') # 도구메뉴 바 추가 
        # toolMenu.addAction(uploadAction)   # 도구메뉴 하위 옵션 추가 (addAction 수정하기)
        OptionMenu = menubar.addMenu('Option')
        
        widget = QtWidgets.QWidget(self)
        self.setCentralWidget(widget)
      
        layout = QtWidgets.QHBoxLayout(widget)
     
        left_frame = QtWidgets.QFrame(self)
        mid_frame = QtWidgets.QFrame(self)
        right_frame = QtWidgets.QFrame(self)
    
        left_frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        mid_frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        right_frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
       
        layout.addWidget(left_frame, 2)
        layout.addWidget(mid_frame, 6)
        layout.addWidget(right_frame, 2)
        left_layout = QtWidgets.QVBoxLayout(left_frame)
      
        start_button = QtWidgets.QPushButton('Start', self)
        # pause_button = QtWidgets.QPushButton('Pause', self)

        
        left_layout.addWidget(start_button)
        # left_layout.addWidget(pause_button)
        left_layout.addStretch()
        mid_layout = QtWidgets.QVBoxLayout(mid_frame)
   
        top_frame = QtWidgets.QFrame(self)
        top_frame1 = QtWidgets.QFrame(self)
        bottom_frame = QtWidgets.QFrame(self)
  
        top_frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        top_frame1.setFrameShape(QtWidgets.QFrame.Shape.Box)
        bottom_frame.setFrameShape(QtWidgets.QFrame.Shape.Box)

        mid_layout.addWidget(top_frame, 3)
        mid_layout.addWidget(top_frame1, 2)
        mid_layout.addWidget(bottom_frame, 2)

      
        widget.setLayout(layout)

    def showUploadWindow(self):
        self.uploadWindow = UploadWindow()
        self.uploadWindow.show()
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    ex = MainWindow()
    ex.show()
    app.exec()
