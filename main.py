#!/usr/bin/python3

import sys
import cv2 as cv
import numpy

from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QPoint, QTimer

class DancingWidget(QWidget):
    """ A class for rendering video coming from OpenCV"""

    def __init__(self, parent=None):
        QWidget.__init__(self)
        self._capture = cv.VideoCapture(0)

        self.label = QLabel()
        self.initUI()
        
        # Paint every 50 ms
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.queryFrame)
        self._timer.start(50)
        

    def initUI(self):
        self.label.setText('OpenCV Video')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('border: gray; border-style:solid; border-width: 1px;')

        btn_pause = QPushButton('Pause')
        btn_pause.clicked.connect(self.pause)

        btn_resume = QPushButton('Resume')
        btn_resume.clicked.connect(self.resume)

        btn_exit = QPushButton('Exit')
        btn_exit.clicked.connect(self.Close)
        
        top_bar = QHBoxLayout()
        top_bar.addWidget(btn_pause)
        top_bar.addWidget(btn_resume)
        top_bar.addWidget(btn_exit)

        root = QVBoxLayout(self)
        root.addLayout(top_bar)
        root.addWidget(self.label)

        self.resize(640, 500)
        self.setWindowTitle('OpenCV & PyQT 5 test')
    """
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(QPoint(0, 0), self._image)
    """
    
    def queryFrame(self):
        _, frame = self._capture.read()
        self.image = frame
        self.display()
        self.update()

    def pause(self):
        self._timer.stop()

    def resume(self):
        self._timer.start()

    def display(self):
        size = self.image.shape
        step = self.image.size / size[0]
        qformat = QImage.Format_Indexed8

        if len(size) == 3:
            if size[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(self.image, size[1], size[0], step, qformat)
        img = img.rgbSwapped()

        self.label.setPixmap(QPixmap.fromImage(img))
        self.resize(self.label.pixmap().size())
    
    def Close(self):
        self._capture.release()
        cv.destroyAllWindows()
        print("exitting...")
        self.close()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    widget = DancingWidget()
    widget.show()
    
    sys.exit(app.exec_())
