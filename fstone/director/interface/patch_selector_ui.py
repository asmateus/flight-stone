from PIL import Image, ImageTk
import tkinter as tk


class PatchSelectorApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Associate application root to main controller
        self.root = master
        self.root.configure(bg='white')
        self.root.minsize(width=1000, height=480)
        self.root.resizable(width=False, height=False)
        self.root.title('Patch extraction: USER INTERFACE')

        # Bind the exit of the GUI to a specific function
        self.root.protocol('WM_DELETE_WINDOW', self.on_quit)

        self._video_holder = tk.Label(self.root)
        self._video_holder.place(x=0, y=0)

        # The GUI initiated successfully
        self.status = True

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
        var_chd = tk.IntVar()
        self.descriptor_chd = tk.Checkbutton(
            self.root,
            text='Color Histogram Descriptor',
            variable=var_chd,
            bg='white',
            borderwidth=0,
            highlightthickness=0
        )
        self.descriptor_chd.place(x=660, y=75)
        var_sift = tk.IntVar()
        self.descriptor_sift = tk.Checkbutton(
            self.root,
            text='SIFT Descriptors',
            variable=var_sift,
            bg='white',
            borderwidth=0,
            highlightthickness=0,
        )
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
        self.rectangle_selection_info = tk.Label(
            self.root,
            text='No image region selected',
            bg='white',
            fg='red',
            anchor='s'
        )
        self.rectangle_selection_info.place(x=650, y=463)

    def browseFiles(self):
        pass

    def generateDescriptions(self):
        pass

    def savePatch(self):
        pass

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
