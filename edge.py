import sys
import cv2
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
        self.originCam.setPixmap(QPixmap.fromImage(image))

    def edgeImage(self, image):
        self.edgeCam.setPixmap(QPixmap.fromImage(image))

    def sobel(self):
        self.thread.changePixmap.connect(self.edgeImage)



# if __name__ == "__main__" :
#     app = QApplication(sys.argv)
#     myWindow = Edge()
#     myWindow.show()
#     app.exec_()