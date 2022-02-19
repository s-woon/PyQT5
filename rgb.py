import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUi
from PyQt5 import QtGui


class rgb(QWidget):

    def __init__(self, parent=None, thread=None):
        super(rgb, self).__init__(parent)
        loadUi('rgb.ui', self)
        self.parent = parent
        self.thread = thread
        # self.thread.changePixmap.connect(self.originImage) # 집 윈도우에서 캠오류

        # 사진파일 읽기
        imgBGR = cv2.imread('lake_louise.jpg')
        imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)

        B, G, R = cv2.split(imgBGR)

        zeros = np.zeros((imgBGR.shape[0], imgBGR.shape[1]), np.uint8)

        imgR = cv2.merge((zeros, zeros, R))
        imgG = cv2.merge((zeros, G, zeros))
        imgB = cv2.merge((B, zeros, zeros))
        imgRG = cv2.merge((R, G, zeros))
        imgRB = cv2.merge((R, zeros, B))
        imgGB = cv2.merge((zeros, G, B))

        h, w, c = imgRGB.shape

        qimg = QtGui.QImage(imgRGB.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        Rimg = QtGui.QImage(imgR.data, w, h, w * c, QtGui.QImage.Format_RGB888)
        Gimg = QtGui.QImage(imgG.data, w, h, w * c, QtGui.QImage.Format_RGB888)
        Bimg = QtGui.QImage(imgB.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        RGimg = QtGui.QImage(imgRG.data, w, h, w * c, QtGui.QImage.Format_RGB888)
        RBimg = QtGui.QImage(imgRB.data, w, h, w * c, QtGui.QImage.Format_RGB888)
        GBimg = QtGui.QImage(imgGB.data, w, h, w * c, QtGui.QImage.Format_RGB888)

        p = qimg.scaled(640, 480, Qt.KeepAspectRatio)
        r = Rimg.scaled(640, 480, Qt.KeepAspectRatio)
        g = Gimg.scaled(640, 480, Qt.KeepAspectRatio)
        b = Bimg.scaled(640, 480, Qt.KeepAspectRatio)
        rg = RGimg.scaled(640, 480, Qt.KeepAspectRatio)
        rb = RBimg.scaled(640, 480, Qt.KeepAspectRatio)
        gb = GBimg.scaled(640, 480, Qt.KeepAspectRatio)

        self.originCam.setPixmap(QPixmap.fromImage(p).scaled(self.originCam.size(), Qt.KeepAspectRatio))
        self.lbB.setPixmap(QPixmap.fromImage(r).scaled(self.lbR.size(), Qt.KeepAspectRatio))
        self.lbG.setPixmap(QPixmap.fromImage(g).scaled(self.lbG.size(), Qt.KeepAspectRatio))
        self.lbR.setPixmap(QPixmap.fromImage(b).scaled(self.lbR.size(), Qt.KeepAspectRatio))
        self.lbRG.setPixmap(QPixmap.fromImage(rg).scaled(self.lbRG.size(), Qt.KeepAspectRatio))
        self.lbRB.setPixmap(QPixmap.fromImage(rb).scaled(self.lbRB.size(), Qt.KeepAspectRatio))
        self.lbGB.setPixmap(QPixmap.fromImage(gb).scaled(self.lbGB.size(), Qt.KeepAspectRatio))

















    # def originImage(self, image):
    #     self.originCam.setPixmap(QPixmap.fromImage(image).scaled(self.originCam.size(), Qt.KeepAspectRatio))

    # def labelR(self, image):
    #     r, g, b = cv2.split(image)
    #     self.lbR.setPixmap(QPixmap.fromImage(r).scaled(self.lbR.size(), Qt.KeepAspectRatio))
    #
    # def labelG(self, image):
    #     self.lbG.setPixmap(QPixmap.fromImage(image).scaled(self.lbG.size(), Qt.KeepAspectRatio))
    #
    # def labelB(self, image):
    #     self.lbB.setPixmap(QPixmap.fromImage(image).scaled(self.lbB.size(), Qt.KeepAspectRatio))
    #
    # def RSlot(self):
    #     self.thread.changePixmap.connect(self.labelR)
    #
    # def GSlot(self):
    #     self.rgbImage.connect(self.labelR)
    #
    # def BSlot(self):
    #     self.rgbImage.connect(self.labelR)
    #
    # def RGSlot(self):
    #     self.rgbImage.connect(self.labelR)
    #
    # def RBSlot(self):
    #     self.rgbImage.connect(self.labelR)
    #
    # def GBSlot(self):
    #     self.rgbImage.connect(self.labelR)

    # def imagR(self, image):
    #     pass
        # print(image)
        # self.imageR.setPixmap(QPixmap.fromImage(image).scaled(self.originCam.size(), Qt.KeepAspectRatio))
        # # r, g, b = cv2.split(image)
        # # print(r, g, b)

