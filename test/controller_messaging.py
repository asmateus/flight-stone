import path_appending

from entities import Director
from iomanager import IOManager
from interface.controllers import GenericMotionController, GENERIC_TYPES
from interface.devices import ArduinoMegaDevice
from events.keyboard import KeyboardListener
import argparse
import sys


def serialWriteReadTest():
    manager = IOManager().getInstance()
    controller = GenericMotionController(ArduinoMegaDevice)

    director = Director()

    manager.addSubscriber(director, GENERIC_TYPES['motion'])
    con_id = manager.addController(controller)

    manager.readController(con_id)


def simpleKeyboardEventTest():
    director = Director()
    listener = KeyboardListener()
    listener.addSubscriber(director)
    listener.startListener()


def keyboardEventTest():
    manager = IOManager().getInstance()
    controller = GenericMotionController(ArduinoMegaDevice)

    director = Director()

    listener = KeyboardListener()
    listener.addSubscriber(director)
    listener.startListener()

    manager.addSubscriber(director, GENERIC_TYPES['motion'])
    con_id = manager.addController(controller)

    director.assignExtendedController(con_id, manager)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='Test selection.')

    test_mode = parser.parse_args().t

    tests = {
        'keyboard': simpleKeyboardEventTest,
        'keytocontroller': keyboardEventTest,
        'serial': serialWriteReadTest,
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
            print('Error in function')
