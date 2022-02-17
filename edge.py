import sys
import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUi
from comm.filters import filter

class Edge(QWidget):
    def __init__(self, parent=None, thread=None):
        super(Edge, self).__init__(parent)
        loadUi('edge.ui', self)
        self.parent = parent
        self.thread = thread
        self.thread.changePixmap.connect(self.setImage)

    def setImage(self, image):
        lbW = self.originCam.width()
        lbH = self.originCam.height()
        self.originCam.setPixmap(QPixmap.fromImage(image).scaled(lbW, lbH, Qt.KeepAspectRatio))

    def robotsEdgeSlot(self):
        pass

    def robotsImage(self):
        pass


    def prewittEdgeSlot(self):
        pass

    def prewittImage(self, image):
        pass


    def sobelEdgeSlot(self):
        self.thread.changePixmap.connect(self.sobelImage)

    def sobelImage(self, image):
        ndarry = self.qimg2nparr(image)
        sobel1 = cv2.Sobel(ndarry, cv2.CV_32F, 1, 0, 3) # x 방향 미분 - 수직마스크
        sobel2 = cv2.Sobel(ndarry, cv2.CV_32F, 0, 1, 3) # y 방향 미분 - 수평마스크
        grayimg = cv2.cvtColor(sobel1, cv2.COLOR_BGR2GRAY)
        sobel1 = cv2.convertScaleAbs(grayimg)
        sobel2 = cv2.convertScaleAbs(sobel2)
        h, w = sobel1.shape
        qimg = QImage(sobel1.data, w, h, QImage.Format_Grayscale8)
        lbW = self.edgeCam.width()
        lbH = self.edgeCam.height()
        self.edgeCam.setPixmap(QPixmap.fromImage(qimg).scaled(lbW, lbH, Qt.KeepAspectRatio))


    def laplacianEdgeSlot(self):
        self.thread.changePixmap.connect(self.laplacianImage)

    def laplacianImage(self, image):
        ndarry = self.qimg2nparr(image)
        grayimg = cv2.cvtColor(ndarry, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(grayimg, cv2.CV_16S, 1)
        laplacian = cv2.convertScaleAbs(laplacian) # 절대값
        h, w = laplacian.shape
        qimg = QImage(laplacian.data, w, h, QImage.Format_Grayscale8)
        lbW = self.edgeCam.width()
        lbH = self.edgeCam.height()
        self.edgeCam.setPixmap(QPixmap.fromImage(qimg).scaled(lbW, lbH, Qt.KeepAspectRatio))


    def cannyEdgeSlot(self):
        self.thread.changePixmap.connect(self.cannyImage)

    def cannyImage(self, image):
        ndarry = self.qimg2nparr(image)
        canny = cv2.Canny(ndarry, 50, 200)
        h, w = canny.shape
        qimg = QImage(canny.data, w, h, QImage.Format_Grayscale8)
        self.edgeCam.setPixmap(QPixmap.fromImage(qimg).scaled(640, 480, Qt.KeepAspectRatio))
        # self.edgeCam.setPixmap(QPixmap.fromImage(qimg).scaled(self.edgeCam.size(), Qt.KeepAspectRatio))


    def qimg2nparr(self, qimg):
        ''' convert rgb qimg -> cv2 bgr image '''
        # NOTE: it would be changed or extended to input image shape
        # Now it just used for canvas stroke.. but in the future... I don't know :(

        # qimg = qimg.convertToFormat(QImage.Format_RGB32)
        # qimg = qimg.convertToFormat(QImage.Format_RGB888)
        h, w = qimg.height(), qimg.width()
        # print(h,w)
        ptr = qimg.constBits()
        ptr.setsize(h * w * 3)
        # print(h, w, ptr)
        return np.frombuffer(ptr, np.uint8).reshape(h, w, 3)  # Copies the data
        #return np.array(ptr).reshape(h, w, 3).astype(np.uint8)  #  Copies the data


# if __name__ == "__main__" :
#     app = QApplication(sys.argv)
#     myWindow = Edge()
#     myWindow.show()
#     app.exec_()
