from entities import UserDirector, UIDirector, TrackingDirector, ColorTrackingDirector
from iomanager import IOManager
from representation.controllers import GenericMotionController, GENERIC_TYPES
from representation.custom_controllers import LocalVideoController, KinectController, CUSTOM_TYPES
from representation.custom_controllers import StreamController
from utils.patch_selector import PatchSelectorManager
from representation.devices import ArduinoMegaDevice, PIC16F1827Device
from events.keyboard import KeyboardListener
from events.tracking import TrackingListener
from interface.minimal import Application as App
from tkinter import Tk
import argparse
import traceback
import sys


def serialWriteReadTest():
    manager = IOManager.getInstance()
    controller = GenericMotionController(PIC16F1827Device)

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
    controller = GenericMotionController(PIC16F1827Device)

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


def trackingTest():
    manager = IOManager.getInstance()
    controller = LocalVideoController()

    # We require a tracking director and a UI director
    ui_director = UIDirector()
    track_director = TrackingDirector()

    # TrackingDirector needs a frame buffer, so we subscribe it to the manager
    manager.addSubscriber(track_director, CUSTOM_TYPES['local_video'])

    # UIDirector also needs to be subscribed, to receive the frames
    manager.addSubscriber(ui_director, CUSTOM_TYPES['local_video'])

    # We assign the controller to the manager
    con_id = manager.addController(controller)

    # Assign application context for ui
    tk_controller = Tk()
    application = App(tk_controller)

    # UI directors require that an application instance is passed to them, and it must implement
    # the updateVideoState method
    ui_director.assignApplicationInstance(application)

    # Now we need to link both directors
    # Tracking director generates a tracking event that the UI director receives
    listener = TrackingListener()
    listener.addSubscriber(ui_director)

    track_director.setTrackingListener(listener)

    # Start reading video source
    manager.readController(con_id)

    # Start UI in main thread
    while True:
        if application.status:
            application.update()
            application.update_idletasks()
        else:
            break


def kinectStreamTest():
    manager = IOManager.getInstance()
    controller = KinectController()

    # In this case the director required is a UI director
    director = UIDirector()

    # Application instance to display the image
    tk_controller = Tk()
    application = App(tk_controller)

    # UI directors require that an application instance is passed to them, and it must implement
    # the updateVideoState method
    director.assignApplicationInstance(application)

    manager.addSubscriber(director, CUSTOM_TYPES['kinect'])
    con_id = manager.addController(controller)

    manager.readController(con_id)

    while True:
        if application.status:
            application.updateVideoHolder()
            application.update()
            application.update_idletasks()
        else:
            break


def simpleStream():
    manager = IOManager.getInstance()
    controller = StreamController()

    # In this case the director required is a UI director
    director = UIDirector()

    # Application instance to display the image
    tk_controller = Tk()
    application = App(tk_controller)

    # UI directors require that an application instance is passed to them, and it must implement
    # the updateVideoState method
    director.assignApplicationInstance(application)

    manager.addSubscriber(director, CUSTOM_TYPES['stream'])
    con_id = manager.addController(controller)

    manager.readController(con_id)

    while True:
        if application.status:
            application.updateVideoHolder()
            application.update()
            application.update_idletasks()
        else:
            break


def trackingFromStream():
    manager = IOManager.getInstance()
    controller = StreamController()

    # We require a tracking director and a UI director
    ui_director = UIDirector()
    track_director = TrackingDirector()

    # TrackingDirector needs a frame buffer, so we subscribe it to the manager
    # manager.addSubscriber(track_director, CUSTOM_TYPES['stream'])

    # UIDirector also needs to be subscribed, to receive the frames
    manager.addSubscriber(ui_director, CUSTOM_TYPES['stream'])

    # We assign the controller to the manager
    con_id = manager.addController(controller)

    # Assign application context for ui
    tk_controller = Tk()
    application = App(tk_controller)

    # UI directors require that an application instance is passed to them, and it must implement
    # the updateVideoState method
    ui_director.assignApplicationInstance(application)

    # Now we need to link both directors
    # Tracking director generates a tracking event that the UI director receives
    listener = TrackingListener()
    listener.addSubscriber(ui_director)

    track_director.setTrackingListener(listener)

    # Start reading video source
    manager.readController(con_id)

    # Start UI in main thread
    while True:
        if application.status:
            application.updateVideoHolder()
            application.update()
            application.update_idletasks()
        else:
            break


def colorTrackingFromStream():
    manager = IOManager.getInstance()
    controller = StreamController()

    # We require a tracking director and a UI director
    ui_director = UIDirector()
    track_director = ColorTrackingDirector()

    # TrackingDirector needs a frame buffer, so we subscribe it to the manager
    manager.addSubscriber(track_director, CUSTOM_TYPES['stream'])

    # UIDirector also needs to be subscribed, to receive the frames
    manager.addSubscriber(ui_director, CUSTOM_TYPES['stream'])

    # We assign the controller to the manager
    con_id = manager.addController(controller)

    # Assign application context for ui
    tk_controller = Tk()
    application = App(tk_controller)

    # UI directors require that an application instance is passed to them, and it must implement
    # the updateVideoState method
    ui_director.assignApplicationInstance(application)

    # Now we need to link both directors
    # Tracking director generates a tracking event that the UI director receives
    listener = TrackingListener()
    listener.addSubscriber(ui_director)

    track_director.setTrackingListener(listener)

    # Start reading video source
    manager.readController(con_id)

    # Start UI in main thread
    while True:
        if application.status:
            application.updateVideoHolder()
            application.update()
            application.update_idletasks()
        else:
            break


def patchSelection():
    PatchSelectorManager(2)


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
        'kinectstream': kinectStreamTest,
        'simplestream': simpleStream,
        'trackingstream': trackingFromStream,
        'colortracking': colorTrackingFromStream,
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
