from PIL import Image, ImageTk
import tkinter as tk


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
        self.img_update = False
        self.last_frame = None

    def updateVideoHolder(self):
        if self.img_update:
            self.img_update = False
            img = Image.fromarray(self.last_frame, 'RGB')
            self.photo = ImageTk.PhotoImage(img)
            self._video_holder.imgtk = self.photo
            self._video_holder.config(image=self.photo)
            self._video_holder.pack()

    def updateVideoState(self, frame):
        if not self.img_update:
            self.last_frame = frame
            self.img_update = True

    def on_quit(self):
        self.status = False
        self.root.destroy()
