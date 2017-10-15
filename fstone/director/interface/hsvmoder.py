import sys
import cv2
import numpy as np
import threading
import time

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import (QCoreApplication, Qt, QBasicTimer)
from PyQt5.QtGui import QIcon, QPixmap, QImage

from QtAutogen.hsvmoder import Ui_MainWindow
from matplotlib import pyplot as plt

from os import listdir, path


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Sliders
        self.ui.hSliderT.valueChanged[int].connect(self.hManageT)
        self.ui.hSliderB.valueChanged[int].connect(self.hManageB)

        self.ui.sSliderT.valueChanged[int].connect(self.sManageT)
        self.ui.sSliderB.valueChanged[int].connect(self.sManageB)

        self.ui.vSliderT.valueChanged[int].connect(self.vManageT)
        self.ui.vSliderB.valueChanged[int].connect(self.vManageB)

        # Buttons
        self.ui.picLoad.clicked.connect(self.bLoader)

        self.ui.bBack.clicked.connect(self.prevPic)
        self.ui.bNext.clicked.connect(self.nextPic)

        # CheckBox
        self.ui.cErosion.clicked.connect(self.togleErotion)
        self.ui.cDilate.clicked.connect(self.togleDilate)

        self.loadImage(np.zeros((480, 640, 3)))

        self.imgList = imageHandeler()

        self.selector = 0
        self.ui.lSelector.setText(str(self.selector+1) + "/" + str(len(self.imgList.img)))

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Escape:
            QCoreApplication.quit()
        elif key == Qt.Key_E:
            self.nextPic()
        elif key == Qt.Key_Q:
            self.prevPic()

    def loadImage(self, img):
        data = img.data
        height, width, _ = img.shape
        pixmap = QImage(data, width, height, 3 * width, QImage.Format_RGB888)
        self.ui.pic.setPixmap(QPixmap(pixmap))

    def hManageT(self, value):
        self.ui.hSliderTValue.setText(str(value))
        self.setImg()

    def hManageB(self, value):
        self.ui.hSliderBValue.setText(str(value))
        self.setImg()

    def sManageT(self, value):
        self.ui.sSliderTValue.setText(str(value))
        self.setImg()

    def sManageB(self, value):
        self.ui.sSliderBValue.setText(str(value))
        self.setImg()

    def vManageT(self, value):
        self.ui.vSliderTValue.setText(str(value))
        self.setImg()

    def vManageB(self, value):
        self.ui.vSliderBValue.setText(str(value))
        self.setImg()

    def prevPic(self):
        if(self.selector > 0):
            self.selector = self.selector - 1
            self.setImg()
        self.ui.lSelector.setText(str(self.selector+1) + "/" + str(len(self.imgList.img)))

    def nextPic(self):
        if(self.selector < len(self.imgList.img)-1):
            self.selector = self.selector + 1
            self.setImg()
        self.ui.lSelector.setText(str(self.selector+1) + "/" + str(len(self.imgList.img)))

    def togleErotion(self, state):
        self.imgList.erosion = state
        self.setImg()

    def togleDilate(self, state):
        self.imgList.dilate = state
        self.setImg()

    def bLoader(self):
        self.imgList.load(self.ui.filePath.toPlainText())
        self.selector = 0
        self.ui.lSelector.setText(str(self.selector+1) + "/" + str(len(self.imgList.img)))
        self.setImg()

    def setImg(self):
        self.loadImage(self.imgList.hsvModer(self.selector,
            [self.ui.hSliderT.value(), self.ui.sSliderT.value(), self.ui.vSliderT.value()],
            [self.ui.hSliderB.value(), self.ui.sSliderB.value(), self.ui.vSliderB.value()]
        ))

class imageHandeler():
    def __init__(self):
        self.img = [np.zeros((480, 640, 3), dtype=np.uint8)]
        self.erosion = False
        self.dilate  = False

    def load(self, path):
        try:
            self.img = sorted(listdir(path), key=lambda student: int(student.split(".")[0][3:]))
            self.img = [cv2.imread(path + a, cv2.IMREAD_COLOR) for a in self.img]
            #for i in range(len(self.img)):
            #    self.img[i] = cv2.imread(path+self.img[i], cv2.IMREAD_COLOR)
        except Exception as ese:
            print("Error: ", ese)

    def hsvModer(self, index, hsv_valueT, hsv_value_B):
        img_BGR = self.img[index]
        img_RGB = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2RGB)
        img_HSV = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2HSV)

        lower_red = np.array(hsv_value_B)
        upper_red = np.array(hsv_valueT)

        mask = cv2.inRange(img_HSV, lower_red, upper_red)
        res = cv2.bitwise_and(img_RGB, img_RGB, mask=mask)
        if self.erosion:
            kernel = np.ones((5, 5), np.uint8)
            res = cv2.erode(res, kernel, iterations=1)
        if self.dilate:
            kernel = np.ones((9, 9), np.uint8)
            res = cv2.dilate(res, kernel, iterations=1)

        return res

app = QApplication(sys.argv)
w = AppWindow()
w.show()

sys.exit(app.exec_())
w.end()
