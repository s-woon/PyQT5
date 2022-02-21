import sys
import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtMultimedia import QCameraInfo, QCamera, QCameraImageCapture
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUi

class Move(QWidget):
    def __init__(self, parent=None, thread=None):
        super(Move, self).__init__(parent)
        loadUi('move.ui', self)
        self.parent = parent
        self.thread = thread
        self.thread.changePixmap.connect(self.originImage)

    def originImage(self, image):
        self.cameraLb.setPixmap(QPixmap.fromImage(image).scaled(self.cameraLb.size(), Qt.KeepAspectRatio))

    def up(self):
        print("up")
        move = self.cameraLb.geometry()
        move.moveTop(move.y() - 10)
        self.cameraLb.setGeometry(move)

    def down(self):
        print("down")
        move = self.cameraLb.geometry()
        move.moveTop(move.y() + 10)
        self.cameraLb.setGeometry(move)

    def left(self):
        print("left")
        move = self.cameraLb.geometry()
        move.moveLeft(move.x() - 10)
        self.cameraLb.setGeometry(move)

    def right(self):
        print("right")
        move = self.cameraLb.geometry()
        move.moveLeft(move.x() + 10)
        self.cameraLb.setGeometry(move)