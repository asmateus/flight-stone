from PIL import Image, ImageTk, ImageDraw
from collections import namedtuple
from tkinter import filedialog
from core.features import DESCRIPTOR_LIST
import tkinter as tk
import numpy as np

Point = namedtuple('Point', ['x', 'y'])


class PatchSelectorApp(tk.Frame):
    def __init__(self, master, manager):
        super().__init__(master)
        # Associate application root to main controller
        self.root = master
        self.root.configure(bg='white')
        self.root.minsize(width=1000, height=480)
        self.root.resizable(width=False, height=False)
        self.root.title('Patch extraction: USER INTERFACE')

        # Instance the manager: patch_selector
        self.manager = manager

        # Bind the exit of the GUI to a specific function
        self.root.protocol('WM_DELETE_WINDOW', self.on_quit)

        self._video_holder = tk.Label(self.root)
        self._video_holder.bind('<Button-1>', self.imageClick)
        self._video_holder.place(x=0, y=0)

        # Create patch points in image
        self.patch_point_1 = None
        self.patch_point_2 = None

        # The GUI initiated successfully
        self.status = True
        self.process_status = [0, 0, 0, 0, 0, 0]
        self.filename = None

        # Creating thread controls
        self.img_update = False
        self.last_frame = None

        # ****************
        # Control elements
        # ****************

        # File browser
        self.file_selector = tk.Button(
            self.root,
            text='Browse',
            command=self.browseFiles,
            bg='white'
        )
        self.file_selector.place(x=650, y=10)

        # File name display
        self.file_selection_string = tk.StringVar()
        self.file_selection_string.set('No file selected')
        self.file_selection_label = tk.Label(
            self.root,
            textvariable=self.file_selection_string,
            bg='white',
        )
        self.file_selection_label.place(x=730, y=16)

        # Section information
        descriptor_section = tk.Label(
            self.root,
            text='Select the descriptors for the Patch:',
            fg='#666666',
            bg='white',
        )
        descriptor_section.place(x=650, y=50)

        # Descriptor types
        self.descriptor_var_chd = tk.IntVar()
        self.descriptor_chd = tk.Checkbutton(
            self.root,
            text='Color Histogram Descriptor',
            variable=self.descriptor_var_chd,
            bg='white',
            borderwidth=0,
            highlightthickness=0
        )
        self.descriptor_chd.bind('<Button-1>', self.updateDescriptorCHD)
        self.descriptor_chd.place(x=660, y=75)
        self.descriptor_var_sift = tk.IntVar()
        self.descriptor_sift = tk.Checkbutton(
            self.root,
            text='SIFT Descriptors',
            variable=self.descriptor_var_sift,
            bg='white',
            borderwidth=0,
            highlightthickness=0,
        )
        self.descriptor_sift.bind('<Button-1>', self.updateDescriptorSIFT)
        self.descriptor_sift.place(x=660, y=100)

        # Selection of maximum amount of features to find:
        max_features_label = tk.Label(
            self.root,
            text='Select maximum amount of features to find (-1=unlimited):',
            bg='white',
            fg='#666666',
        )
        max_features_label.place(x=650, y=125)

        max_features_label_2 = tk.Label(
            self.root,
            text='MAX amount',
            bg='white',
            anchor='s'
        )
        max_features_label_2.place(x=660, y=147)

        self.max_features_string = tk.StringVar()
        self.max_features_string.set('-1')
        self.max_features_box = tk.Entry(
            self.root,
            textvariable=self.max_features_string,
            bg='white',
            width=5,
            justify='c',
            font=('Verdana', 10),
        )
        self.max_features_box.place(x=740, y=145)

        # Select name for patch
        patch_name_label = tk.Label(
            self.root,
            text='Choose Patch name (no spaces): ',
            bg='white',
            fg='#666666',
            anchor='s'
        )
        patch_name_label.place(x=650, y=170)
        self.patch_name_string = tk.StringVar()
        self.patch_name_string.trace('w', self.patchNameUpdated)
        self.patch_name_string.set('')
        self.patch_name_box = tk.Entry(
            self.root,
            textvariable=self.patch_name_string,
            bg='white',
            width=20,
            justify='l',
        )
        self.patch_name_box.place(x=660, y=190)

        # Generate description buttons
        self.description_generator = tk.Button(
            self.root,
            text='Generate',
            command=self.generateDescriptions,
            bg='white'
        )
        self.description_generator.place(x=650, y=220)

        # Save Patch button
        self.save_patch = tk.Button(
            self.root,
            text='Save',
            command=self.savePatch,
            bg='white'
        )
        self.save_patch.place(x=740, y=220)

        # Rectangle selection info
        self.general_info_string = tk.StringVar()
        self.general_info = tk.Label(
            self.root,
            textvariable=self.general_info_string,
            bg='white',
            fg='red',
            anchor='s'
        )
        self.general_info.place(x=650, y=463)
        self.updateInformation()

    def imageClick(self, location):
        if not self.patch_point_1:
            self.patch_point_1 = Point(x=location.x, y=location.y)
        elif not self.patch_point_2:
            self.patch_point_2 = Point(x=location.x, y=location.y)
        else:
            self.patch_point_1, self.patch_point_2 = None, None

        self.updateRectangleDrawing()
        self.updateInformation()

    def updateDescriptorCHD(self, l):
        if not self.descriptor_var_chd.get():
            self.manager.assignDescriptor(DESCRIPTOR_LIST['CHD']())
            self.process_status[2] = 1
        elif not self.descriptor_var_sift.get():
            self.process_status[2] = 0
        elif self.descriptor_var_sift.get():
            self.process_status[2] = 1

        if self.descriptor_var_chd.get():
            self.manager.removeDescriptor(str(DESCRIPTOR_LIST['CHD']()))

        self.updateInformation()

    def updateDescriptorSIFT(self, l):
        if not self.descriptor_var_sift.get():
            self.manager.assignDescriptor(DESCRIPTOR_LIST['SIFT']())
            self.process_status[2] = 1
        elif not self.descriptor_var_chd.get():
            self.process_status[2] = 0
        elif self.descriptor_var_chd.get():
            self.process_status[2] = 1

        if self.descriptor_var_sift.get():
            self.manager.removeDescriptor(str(DESCRIPTOR_LIST['SIFT']()))

        self.updateInformation()

    def updateRectangleDrawing(self):
        img = Image.fromarray(self.last_frame, 'RGB')
        draw = ImageDraw.Draw(img)
        r = 3
        self.process_status[1] = 0
        if self.patch_point_1:
            draw.ellipse(
                (
                    self.patch_point_1.x - r,
                    self.patch_point_1.y - r,
                    self.patch_point_1.x + r,
                    self.patch_point_1.y + r,
                ),
                fill=(255, 0, 0, 255)
            )
        if self.patch_point_2:
            draw.ellipse(
                (
                    self.patch_point_2.x - r,
                    self.patch_point_2.y - r,
                    self.patch_point_2.x + r,
                    self.patch_point_2.y + r,
                ),
                fill=(255, 0, 0, 255)
            )
        if self.patch_point_1 and self.patch_point_2:
            draw.line(
                [
                    (self.patch_point_1.x, self.patch_point_1.y),
                    (self.patch_point_2.x, self.patch_point_1.y),
                    (self.patch_point_2.x, self.patch_point_2.y),
                    (self.patch_point_1.x, self.patch_point_2.y),
                    (self.patch_point_1.x, self.patch_point_1.y),
                ],
                fill=(255, 0, 0, 255)
            )
            self.manager.samplePatchFromImage(self.patch_point_1, self.patch_point_2)
            self.process_status[1] = 1
        self.photo = ImageTk.PhotoImage(img)
        self._video_holder.imgtk = self.photo
        self._video_holder.config(image=self.photo)

    def updateInformation(self):
        if not self.process_status[0]:
            self.general_info_string.set('Please select an image source')
        elif not self.process_status[1]:
            self.general_info_string.set('No image region selected')
        elif not self.process_status[2]:
            self.general_info_string.set('No descriptor selected')
        elif not self.process_status[3]:
            self.general_info_string.set('No description performed')
        elif not self.process_status[4]:
            self.general_info_string.set('No name given to patch')
        elif not self.process_status[5]:
            self.general_info_string.set('Patch not saved')
        else:
            self.general_info_string.set('')

    def browseFiles(self):
        self.filename = filedialog.askopenfilename(
            title='Select image source',
            filetypes=(('jpeg files', '*.jpg'), ('all files', '*.*'))
        )
        if self.filename:
            self.file_selection_string.set(self.filename.split('/')[-1])
            img = Image.open(self.filename)
            self.last_frame = np.array(img)
            self.img_update = True
            self.process_status[0] = 1

            self.manager.assignSourceImage(self.last_frame, self.filename)

            self.updateVideoHolder()
            self.updateInformation()

    def generateDescriptions(self):
        if self.process_status[0] and self.process_status[1] and self.process_status[2]:
            print(self.manager.triggerFeatureExtraction())
            self.process_status[3] = 1
        self.updateInformation()

    def patchNameUpdated(self, *args):
        name = self.patch_name_string.get()
        if name != '' and ' ' not in name:
            self.process_status[4] = 1
            self.updateInformation()
        else:
            if self.process_status[4] is 1:
                self.process_status[4] = 0
                self.updateInformation()

    def savePatch(self):
        patch = self.manager.getPatchInstance()
        patch.name = self.patch_name_string.get()
        self.manager.generatePersistentCopy()

    def updateVideoHolder(self):
        if self.img_update:
            self.img_update = False
            img = Image.fromarray(self.last_frame, 'RGB')
            self.photo = ImageTk.PhotoImage(img)
            self._video_holder.imgtk = self.photo
            self._video_holder.config(image=self.photo)

    def updateVideoState(self, frame):
        if not self.img_update:
            self.last_frame = frame
            self.img_update = True

    def on_quit(self):
        self.status = False
        self.root.destroy()
