import numpy as np
from PyQt5.QtGui import QImage


def qimg2nparr(qimg):
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
    # return np.array(ptr).reshape(h, w, 3).astype(np.uint8)  #  Copies the data


def nparr2qimg(cvimg):
    ''' convert cv2 bgr image -> rgb qimg '''
    h, w, c = cvimg.shape
    byte_per_line = w * c  # cvimg.step() #* step # NOTE:when image format problem..
    return QImage(cvimg.data, w, h, byte_per_line,
                  QImage.Format_RGB888).rgbSwapped()