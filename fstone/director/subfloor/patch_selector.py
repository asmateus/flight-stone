from core.features import ColorHistogramExtractor, SIFTExtractor
from interface.patch_selector_ui import PatchSelectorApp as App
from interface.minimal import Application as MinApp
from tkinter import Tk
import pickle
import os

PTH = os.path.dirname(os.path.abspath(__file__)).split('fstone')[0]


def checkAccess(func):
    def check(*args):
        if args[0].access:
                func(*args)
        else:
            return
    return check


class Patch:
    def __init__(self, name='', origin='', p1=(0, 0), p2=(0, 0), patch=None, descriptions=[]):
        self.name = name
        self.origin = origin
        self.p1 = p1
        self.p2 = p2
        self.patch = patch
        self.descriptions = descriptions


class PatchSelectorManager:
    DEFAULT_DESCRIPTOR = (ColorHistogramExtractor(), SIFTExtractor())
    PERSISTENT_COPY_PATH = PTH + 'fstone/director/subfloor/seeds/'
    INTERACTION_METHODS = {
        'terminal': 1,
        'graphical': 2,
        'interactive': 3,
    }

    def __init__(self, interaction_method=None, *targs):
        # Select a method for choosing the patch, be it terminal or graphical (or interactive)
        self.method = PatchSelectorManager.INTERACTION_METHODS['terminal']
        if interaction_method:
            self.method = interaction_method

        # Choose descriptors
        self.descriptors = list()

        # Instance the target patch of the image
        self.patch = Patch()
        self.source_image = None
        self.image_sample = None

        dispatcher = {
            PatchSelectorManager.INTERACTION_METHODS['terminal']: self.performFullDemand,
            PatchSelectorManager.INTERACTION_METHODS['graphical']: self.launchInteractiveUI,
            PatchSelectorManager.INTERACTION_METHODS['interactive']: self.allowInteractiveCalls,
        }
        # try:
        self.loadPersistentCopy('pruba2')
        self.triggerFeatureExtraction()
        # self.displayPatch()
        # dispatcher[self.method]()
        # except Exception:
        #    print('Error in method selected')

    def performFullDemand(self):
        print('Perfom Full Demand')

    def assignDescriptor(self, descriptor):
        for i in self.descriptors:
            if str(i) == str(descriptor):
                return
        self.descriptors.append(descriptor)

    def removeDescriptor(self, str_descriptor):
        boo = False
        j = 0
        for i in range(self.descriptors):
            if str(self.descriptors.get(i)) == str_descriptor:
                boo = True
                j = i
                break
        if boo:
            self.descriptors.remove(j)

    def launchInteractiveUI(self):
        tk_controller = Tk()
        application = App(tk_controller, self)

        while True:
            try:
                if application.status:
                    application.updateVideoHolder()
                    application.update()
                    application.update_idletasks()
                else:
                    break
            except Exception:
                print('Application exited')

    def assignSourceImage(self, img, pth):
        self.patch.origin = pth
        self.source_image = img

    def samplePatchFromImage(self, p1, p2):
        self.patch.p1 = p1
        self.patch.p2 = p2

        max_x = max(p1.x, p2.x)
        min_x = min(p1.x, p2.x)

        max_y = max(p1.y, p2.y)
        min_y = min(p1.y, p2.y)

        if self.source_image is not None:
            self.image_sample = self.source_image[min_y:max_y, min_x:max_x]
            self.patch.patch = self.image_sample

    def triggerFeatureExtraction(self):
        chd = ColorHistogramExtractor()
        des = chd.getDescription(self.patch.patch)
        return des

    def allowInteractiveCalls(self):
        print('Interactive Calls')

    def getPatchInstance(self):
        return self.patch

    def generatePersistentCopy(self):
        print(PatchSelectorManager.PERSISTENT_COPY_PATH)
        if self.patch:
            with open(
                PatchSelectorManager.PERSISTENT_COPY_PATH + self.patch.name + '.pkl',
                'wb'
            ) as outfile:
                pickle.dump(self.patch, outfile, pickle.HIGHEST_PROTOCOL)

    def loadPersistentCopy(self, copy_name):
        with open(PatchSelectorManager.PERSISTENT_COPY_PATH + copy_name + '.pkl', 'rb') as infile:
            self.patch = pickle.load(infile)

    def displayPatch(self):
        tk_controller = Tk()
        application = MinApp(tk_controller)
        application.updateVideoState(self.patch.patch)

        while True:
            try:
                if application.status:
                    application.updateVideoHolder()
                    application.update()
                    application.update_idletasks()
                else:
                    break
            except Exception:
                print('Application exited')


if __name__ == '__main__':
    p = PatchSelectorManager(2)
