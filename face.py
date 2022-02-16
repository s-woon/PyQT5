import sys
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUi


class facecam(QWidget):
    def __init__(self, parent=None):
        super(facecam, self).__init__(parent)
        loadUi('face.ui', self)


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = facecam()
    myWindow.show()
    app.exec_()