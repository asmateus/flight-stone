from PIL import Image, ImageTk, ImageDraw
from collections import namedtuple
import tkinter as tk

Point = namedtuple('Point', ['x', 'y'])


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=640, height=480, bg='white')
        self.width = 640
        self.height = 480

        # Associate application root to main controller
        self.root = master
        self.root.title('Minimal Application FLIGHT STONE')

        # Bind the exit of the GUI to a specific function
        self.root.protocol('WM_DELETE_WINDOW', self.on_quit)

        self._video_holder = tk.Label(self)
        self.pack()

        # The GUI initiated successfully
        self.status = True

        # Creating thread controls
        self.region_to_draw = False
        self.region = (Point(x=0, y=0), Point(x=0, y=0))
        self.img_update = False
        self.last_frame = None

    def setRegionToDraw(self, p1, p2):
        self.region_to_draw = True
        self.region = (Point(x=p1[0], y=p1[1]), Point(x=p2[0], y=p2[1]))

    def updateVideoHolder(self):
        if self.img_update:
            self.img_update = False
            img = Image.fromarray(self.last_frame, 'RGB')

            # All extra drawings to be applied to current frame
            self.applyExtraDrawings(img)

            # Put the image in the label
            self.photo = ImageTk.PhotoImage(img)
            self._video_holder.imgtk = self.photo
            self._video_holder.config(image=self.photo)
            self._video_holder.pack()

    def updateVideoState(self, frame):
        if not self.img_update:
            self.last_frame = frame
            self.img_update = True

    def applyExtraDrawings(self, img):
        if self.region_to_draw:
            draw = ImageDraw.Draw(img)
            draw.line(
                [
                    (self.region[0].x, self.region[0].y),
                    (self.region[1].x, self.region[0].y),
                    (self.region[1].x, self.region[1].y),
                    (self.region[0].x, self.region[1].y),
                    (self.region[0].x, self.region[0].y),
                ],
                fill=(255, 0, 0, 255)
            )

    def on_quit(self):
        self.status = False
        self.root.destroy()
