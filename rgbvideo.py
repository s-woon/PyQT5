import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUi
from PyQt5 import QtGui


class rgbvideo(QWidget):

    def __init__(self, parent=None, thread=None):
        super(rgbvideo, self).__init__(parent)
        loadUi('rgbvideo.ui', self)
        self.parent = parent
        self.thread = thread

        self.thread.changePixmap.connect(self.setImage)
        self.thread.Frame.connect(self.setRGB)


    def setImage(self, image):
        self.originCam.setPixmap(QPixmap.fromImage(image).scaled(self.originCam.size(), Qt.KeepAspectRatio))

    def setRGB(self, frame):
        R, G, B = cv2.split(frame)
        zeros = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)

        imgR = cv2.merge((R, zeros, zeros))
        imgG = cv2.merge((zeros, G, zeros))
        imgB = cv2.merge((zeros, zeros, B))
        imgRG = cv2.merge((R, G, zeros))
        imgRB = cv2.merge((R, zeros, B))
        imgGB = cv2.merge((zeros, G, B))

        h, w, c = frame.shape

        Rimg = QtGui.QImage(imgR.data, w, h, w * c, QtGui.QImage.Format_RGB888).scaled(640, 480, Qt.KeepAspectRatio)
        Gimg = QtGui.QImage(imgG.data, w, h, w * c, QtGui.QImage.Format_RGB888).scaled(640, 480, Qt.KeepAspectRatio)
        Bimg = QtGui.QImage(imgB.data, w, h, w*c, QtGui.QImage.Format_RGB888).scaled(640, 480, Qt.KeepAspectRatio)
        RGimg = QtGui.QImage(imgRG.data, w, h, w * c, QtGui.QImage.Format_RGB888).scaled(640, 480, Qt.KeepAspectRatio)
        RBimg = QtGui.QImage(imgRB.data, w, h, w * c, QtGui.QImage.Format_RGB888).scaled(640, 480, Qt.KeepAspectRatio)
        GBimg = QtGui.QImage(imgGB.data, w, h, w * c, QtGui.QImage.Format_RGB888).scaled(640, 480, Qt.KeepAspectRatio)
        self.lbR.setPixmap(QPixmap.fromImage(Rimg).scaled(self.lbR.size(), Qt.KeepAspectRatio))
        self.lbG.setPixmap(QPixmap.fromImage(Gimg).scaled(self.lbG.size(), Qt.KeepAspectRatio))
        self.lbB.setPixmap(QPixmap.fromImage(Bimg).scaled(self.lbR.size(), Qt.KeepAspectRatio))
        self.lbRG.setPixmap(QPixmap.fromImage(RGimg).scaled(self.lbRG.size(), Qt.KeepAspectRatio))
        self.lbRB.setPixmap(QPixmap.fromImage(RBimg).scaled(self.lbRB.size(), Qt.KeepAspectRatio))
        self.lbGB.setPixmap(QPixmap.fromImage(GBimg).scaled(self.lbGB.size(), Qt.KeepAspectRatio))

