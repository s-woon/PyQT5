import sys
import cv2
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from face import facecam
from edge import Edge
from affine import Affine


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    # print('1')

    def run(self):
        print('카메라실행')
        global cap
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgbImage = cv2.flip(rgbImage, 1) # 좌우반전
                h, w, ch = rgbImage.shape
                bytePerLine = ch * w
                cvc = QImage(rgbImage.data, w, h, bytePerLine, QImage.Format_RGB888)
                p = cvc.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                # print('3')


class WindowClass(QMainWindow):
    def __init__(self):
        super(WindowClass, self).__init__()
        loadUi('main.ui', self)
        self.th = Thread(self)

        self.actionhome.triggered.connect(self.gobackhome)
        self.actionface.triggered.connect(self.goface)

        self.actionedges.triggered.connect(self.goedge)
        self.actionaffine.triggered.connect(self.goaffine)

        self.stackedWidget.insertWidget(1, facecam(self))
        self.stackedWidget.insertWidget(2, Edge(self, self.th))
        self.stackedWidget.insertWidget(3, Affine(self, self.th))

    def setImage(self, image): # image = p
        # lbW = self.cameraLb.width()
        # lbH = self.cameraLb.height()
        # self.cameraLb.setPixmap(QPixmap.fromImage(image).scaled(lbW, lbH, Qt.KeepAspectRatio))
        self.cameraLb.setPixmap(QPixmap.fromImage(image).scaled(self.cameraLb.size(), Qt.KeepAspectRatio))
        # print('4')

    def cameraOn(self):
        self.th.changePixmap.connect(self.setImage)
        self.th.start()
        # print('2')

    def gobackhome(self):
        self.stackedWidget.setCurrentIndex(0)

    def goface(self):
        self.stackedWidget.setCurrentIndex(1)

    def goedge(self):
        self.stackedWidget.setCurrentIndex(2)

    def goaffine(self):
        self.stackedWidget.setCurrentIndex(3)


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()