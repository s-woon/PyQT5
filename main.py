import datetime
import sys
import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from face import facecam
from edge import Edge
from rgb import rgb
from movecam import Move
from rgbvideo import rgbvideo
from affine import Affine


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    recordFrame = pyqtSignal(np.ndarray)
    Frame = pyqtSignal(np.ndarray)

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
                self.recordFrame.emit(frame)
                self.Frame.emit(rgbImage)
                # print('3')


class WindowClass(QMainWindow):
    def __init__(self):
        super(WindowClass, self).__init__()
        loadUi('main.ui', self)
        self.th = Thread(self)

        self.actionhome.triggered.connect(self.gobackhome)
        self.actionface.triggered.connect(self.goface)
        self.actionrgb.triggered.connect(self.gorgb)
        self.actionmove.triggered.connect(self.gomove)
        self.actionedges.triggered.connect(self.goedge)
        self.actionrgbvideo.triggered.connect(self.gorgbvideo)
        self.actionaffine.triggered.connect(self.goaffine)

        self.stackedWidget.insertWidget(1, facecam(self))
        self.stackedWidget.insertWidget(2, Edge(self, self.th))
        self.stackedWidget.insertWidget(3, rgb(self, self.th))
        self.stackedWidget.insertWidget(4, Move(self, self.th))
        self.stackedWidget.insertWidget(5, rgbvideo(self, self.th))
        self.stackedWidget.insertWidget(6, Affine(self, self.th))

        self.startbtn.setCheckable(True)
        # self.startbtn.clicked.connect(self.recstart) # Pyqt designer 에서 준 시그널이랑 중복돼서 두번 녹화, 저장됨

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

    def recstart(self, state):
        global writer
        if state:
            fps = 29.97
            # size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            # delay = round(1000 / fps)
            date = datetime.datetime.now()
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            writer = cv2.VideoWriter(str(date)+'.avi', fourcc, fps, (640, 480))
            self.th.recordFrame.connect(self.recording)
        else:
            writer.release()
            self.th.recordFrame.disconnect(self.recording)
            print('Recording Stop')

    def recording(self, frame):
        writer.write(frame)
        print('Recording.')
        print('Recording..')
        print('Recording...')

    def gobackhome(self):
        self.stackedWidget.setCurrentIndex(0)

    def goface(self):
        self.stackedWidget.setCurrentIndex(1)

    def goedge(self):
        self.stackedWidget.setCurrentIndex(2)

    def gorgb(self):
        self.stackedWidget.setCurrentIndex(3)

    def gomove(self):
        self.stackedWidget.setCurrentIndex(4)

    def gorgbvideo(self):
        self.stackedWidget.setCurrentIndex(5)

    def goaffine(self):
        self.stackedWidget.setCurrentIndex(6)


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()