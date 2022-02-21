import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUi


class Affine(QWidget):
    def __init__(self, parent=None, thread=None):
        super(Affine, self).__init__(parent)
        loadUi('affine.ui', self)
        self.parent = parent
        self.thread = thread



        self.thread.changePixmap.connect(self.setImage)
        self.setMouseTracking(True)

    def setImage(self, image):
        self.originCam.setPixmap(QPixmap.fromImage(image).scaled(self.originCam.size(), Qt.KeepAspectRatio))

    def affineImage(self, image):
        # def contain_pts(p, p1, p2):
        #     return p1[0] <= p[0] < p2[0] and p1[1] <= p[1] < p2[1]
        #
        #
        # def draw_rect(img, pts):
        #     rois = [(p - small, small * 2) for p in pts]
        #     for (x, y), (w, h) in np.int32(rois):
        #         cv2.rectangle(img, (x, y, w, h), (0, 255, 0), 2)
        #     qimg = QImage(img.data, w, h, QImage.Format_RGB888)
        #     self.affineCam.setPixmap(QPixmap.fromImage(qimg).scaled(self.originCam.size(), Qt.KeepAspectRatio))
        #
        # def affine(img):
        #     aff_mat = cv2.getAffineTransform(pts1, pts2)
        #     dst = cv2.warpAffine(img, aff_mat, image.shape[1::-1], cv2.INTER_LINEAR)
        #
        # small = np.array([12, 12])
        # check = -1
        # pts1 = np.float32([(30, 30), (450, 30), (200, 370)])
        # pts2 = np.float32([(30, 30), (450, 30), (200, 370)])
        #
        # draw_rect(np.copy(image), pts1)
        self.affineCam.setPixmap(QPixmap.fromImage(image).scaled(self.affineCam.size(), Qt.KeepAspectRatio))

    def affineSlot(self):
        self.thread.changePixmap.connect(self.affineImage)

    def mousePressEvent(self, event):  # event : QMouseEvent
        if event.buttons() & Qt.LeftButton:
            print('BUTTON PRESS - LEFT', event.x(), event.y())
        self.mdX, self.mdy = event.x(), event.y()

    def mouseReleaseEvent(self, event):  # event : QMouseEvent
        print('BUTTON RELEASE', event.x(), event.y())
        self.muX, self.muy = event.x(), event.y()

    # def mouseMoveEvent(self, event):  # event QMouseEvent
    #     print('(%d %d)' % (event.x(), event.y()))





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