from subfloor.features import ColorHistogram, SIFTExtractor
from interface.patch_selector_ui import PatchSelectorApp as App
from collections import namedtuple
from tkinter import Tk
import pickle
import PIL
import numpy as np
import os

Patch = namedtuple('Patch', ['name', 'origin', 'w', 'h', 'patch', 'descriptions'])
PTH = os.path.dirname(os.path.abspath(__file__)).split('fstone')[0]


def checkAccess(func):
    def check(*args):
        if args[0].access:
                func(*args)
        else:
            return
    return check


class PatchSelectorManager:
    DEFAULT_DESCRIPTOR = (ColorHistogram(), SIFTExtractor())
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

        # Instance the target patch of the image
        self.patch = Patch(
            name='',
            origin='',
            w=0,
            h=0,
            patch=None,
            descriptions=()
        )

        dispatcher = {
            PatchSelectorManager.INTERACTION_METHODS['terminal']: self.performFullDemand,
            PatchSelectorManager.INTERACTION_METHODS['graphical']: self.launchInteractiveUI,
            PatchSelectorManager.INTERACTION_METHODS['interactive']: self.allowInteractiveCalls,
        }
        # try:
        dispatcher[self.method]()
        # except Exception:
        #    print('Error in method selected')

    def performFullDemand(self):
        print('Perfom Full Demand')

    def launchInteractiveUI(self):
        tk_controller = Tk()
        application = App(tk_controller)
        img = PIL.Image.open('/home/asmateus/Git/flight-stone/extra/example_videos/001.jpg')
        arr = np.array(img)
        application.updateVideoState(arr)

        while True:
            if application.status:
                application.updateVideoHolder()
                application.update()
                application.update_idletasks()
            else:
                break

    def allowInteractiveCalls(self):
        print('Interactive Calls')

    def generatePersistentCopy(self):
        print(PatchSelectorManager.PERSISTENT_COPY_PATH)
        if self.patch:
            with open(
                PatchSelectorManager.PERSISTENT_COPY_PATH + self.patch.name + '.pkl',
                'wb'
            ) as outfile:
                pickle.dump(self.patch, outfile, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    p = PatchSelectorManager(2)
