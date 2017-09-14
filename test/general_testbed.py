from entities import UserDirector, UIDirector, TrackingDirector
from iomanager import IOManager
from representation.controllers import GenericMotionController, GENERIC_TYPES
from representation.custom_controllers import LocalVideoController, CUSTOM_TYPES
from utils.patch_selector import PatchSelectorManager
from representation.devices import ArduinoMegaDevice
from events.keyboard import KeyboardListener
from interface.minimal import Application as App
from tkinter import Tk
import argparse
import traceback
import sys


def serialWriteReadTest():
    manager = IOManager.getInstance()
    controller = GenericMotionController(ArduinoMegaDevice)

    director = UserDirector()

    manager.addSubscriber(director, GENERIC_TYPES['motion'])
    con_id = manager.addController(controller)

    manager.readController(con_id)


def simpleKeyboardEventTest():
    director = UserDirector()
    listener = KeyboardListener()
    listener.addSubscriber(director)
    listener.startListener()


def keyboardEventTest():
    manager = IOManager.getInstance()
    controller = GenericMotionController(ArduinoMegaDevice)

    director = UserDirector()

    listener = KeyboardListener()
    listener.addSubscriber(director)
    listener.startListener()

    manager.addSubscriber(director, GENERIC_TYPES['motion'])
    con_id = manager.addController(controller)

    director.assignExtendedController(con_id, manager)


def localVideoTest():
    manager = IOManager.getInstance()
    controller = LocalVideoController()

    # In this case the director required is a UI director
    director = UIDirector()

    # Application instance to display the image
    tk_controller = Tk()
    application = App(tk_controller)

    # UI directors require that an application instance is passed to them, and it must implement
    # the updateVideoState method
    director.assignApplicationInstance(application)

    manager.addSubscriber(director, CUSTOM_TYPES['local_video'])
    con_id = manager.addController(controller)

    manager.readController(con_id)

    while True:
        if application.status:
            application.updateVideoHolder()
            application.update()
            application.update_idletasks()
        else:
            break


def patchSelection():
    PatchSelectorManager(2)


def trackingTest():
    manager = IOManager.getInstance()
    controller = LocalVideoController()

    # We require a tracking director
    director = TrackingDirector()

    # TrackingDirector needs a frame buffer, so we subscribe it to the manager
    # manager.addSubscriber(director, CUSTOM_TYPES['local_video'])

    # We assign the controller to the manager and read it
    con_id = manager.addController(controller)
    manager.readController(con_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='Test selection.')

    test_mode = parser.parse_args().t

    tests = {
        'keyboard': simpleKeyboardEventTest,
        'keytocontroller': keyboardEventTest,
        'serial': serialWriteReadTest,
        'localv': localVideoTest,
        'tracking': trackingTest,
        'patchselector': patchSelection,
    }

    if not test_mode:
        print('No test selected.')
    else:
        try:
            test = tests[test_mode]
        except Exception:
            print('Test', test_mode, 'does not exist.')
            sys.exit()

        try:
            test()
        except Exception:
            traceback.print_exc(file=sys.stdout)
