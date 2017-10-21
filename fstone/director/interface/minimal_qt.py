from interface.QtAutogen.minimal_autogen import Ui_MainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication
from collections import namedtuple
import sys
import cv2


Point = namedtuple('Point', ['x', 'y'])


class MinimalApplication(QMainWindow):
    instance = None
    app = None

    @staticmethod
    def getInstance():
        MinimalApplication.app = QApplication(sys.argv)
        if MinimalApplication.instance is None:
            MinimalApplication.instance = MinimalApplication()
        return MinimalApplication.instance

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.img_update = False
        self.last_frame = None

        self.region_to_draw = False
        self.region = (Point(x=0, y=0), Point(x=0, y=0))

    def startApplication(self):
        self.show()

        sys.exit(MinimalApplication.app.exec_())
        self.end()

    def loadFrame(self, img):
        self.applyExtraDrawings(img)
        data = img.data
        height, width, _ = img.shape
        pixmap = QImage(data, width, height, 3 * width, QImage.Format_RGB888)
        self.ui.video_holder.setPixmap(QPixmap(pixmap))

    def applyExtraDrawings(self, img):
        if self.region_to_draw:
            cv2.rectangle(
                img,
                (self.region[0].x, self.region[0].y),
                (self.region[1].x, self.region[1].y),
                (0, 255, 0),
                5)

    def updateVideoState(self, frame):
        if not self.img_update:
            self.last_frame = frame
            self.img_update = True
            self.updateVideoHolder()

    def setRegionToDraw(self, p1, p2):
        self.region_to_draw = True
        self.region = (Point(x=p1[0], y=p1[1]), Point(x=p2[0], y=p2[1]))

    def updateVideoHolder(self):
        if self.img_update:
            self.img_update = False

            if self.last_frame is not None:
                self.loadFrame(self.last_frame)
