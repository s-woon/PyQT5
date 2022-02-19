import sys
import cv2
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from face import facecam
from edge import Edge
from rgb import rgb
from movecam import Move
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
        self.actionrgb.triggered.connect(self.gorgb)
        self.actionmove.triggered.connect(self.gomove)
        self.actionedges.triggered.connect(self.goedge)
        # self.actionaffine.triggered.connect(self.goaffine)

        self.stackedWidget.insertWidget(1, facecam(self))
        self.stackedWidget.insertWidget(2, Edge(self, self.th))
        self.stackedWidget.insertWidget(3, rgb(self, self.th))
        self.stackedWidget.insertWidget(4, Move(self, self.th))
        # self.stackedWidget.insertWidget(3, Affine(self, self.th))

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

    def record(self):
        print('Recording Start')
        fps = 29.97
        print(1)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        print(2)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        size = (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(3)
        delay = round(1000/fps)
        print(4)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        print(5)
        writer = cv2.VideoWriter('test.avi', fourcc, fps, size)
        print(6)
        if writer.isOpened() == False: raise Exception("동영상 파일 개방 안됨")
        print(7)
        while True:
            print(8)
            ret, frame = cap.read()
            print(9)
            if not ret: break
            print(10)
            if cv2.waitKey(delay) >= 0: break
            print(11)

            writer.write(frame)
            print(12)

        writer.release()
        print(13)
        cap.release()
        print('Recording Stop')


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

    # def goaffine(self):
    #     self.stackedWidget.setCurrentIndex(3)


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()