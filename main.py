import sys
import cv2
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from face import facecam
from edge import Edge


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        print('카메라실행')
        global cap
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytePerLine = ch * w
                cvc = QImage(rgbImage.data, w, h, bytePerLine, QImage.Format_RGB888)
                p = cvc.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


class WindowClass(QMainWindow):
    def __init__(self):
        super(WindowClass, self).__init__()
        loadUi('main.ui', self)
        self.th = Thread(self)

        self.actionhome.triggered.connect(self.gobackhome)
        self.actionface.triggered.connect(self.goface)

        self.actionedge.triggered.connect(self.goedge)

        self.stackedWidget.insertWidget(1, facecam(self))
        self.stackedWidget.insertWidget(2, Edge(self, self.th))

    def setImage(self, image): # image = p
        self.cameraLb.setPixmap(QPixmap.fromImage(image))

    def cameraOn(self):
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

    def gobackhome(self):
        self.stackedWidget.setCurrentIndex(0)

    def goface(self):
        self.stackedWidget.setCurrentIndex(1)

    def goedge(self):
        self.stackedWidget.setCurrentIndex(2)


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()