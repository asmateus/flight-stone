'''
    Manages keyboard events and handles listeners. As of now only supports entries of single
    characters.
    POSIX system assumed.
'''
import sys
import tty
from threading import Thread
import termios


class KeyboardListener:
    def __init__(self):
        self.subscribers = []
        self.event_type = 'keyboard'
        self._state = False

    def _getch(self):
        '''Getch a character from stdin'''
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        ch = None
        while self._state:
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            if ch:
                if ch == 'q':
                    self._state = False
                    self.manageEvent('exit')
                else:
                    self.manageEvent(ch)

    def startListener(self):
        self._state = True
        Thread(None, target=self._getch, args=()).start()

    def stopListener(self):
        self._state = False

    def manageEvent(self, response):
        for subscriber_stamp in self.subscribers:
            subscriber, _ = subscriber_stamp
            subscriber.manageEventResponse(self.event_type, response)

    def addSubscriber(self, subscriber):
        gen_id = 0
        if self.subscribers:
            _, ids = zip(*self.subscribers)
            gen_id = self.generateUniqueID(ids)
        self.subscribers.append((subscriber, gen_id))
        return gen_id

    def removeSubscriber(self, subscriber_id):
        _, ids = zip(*self.subscribers)
        i = -1
        for id_index in range(len(ids)):
            if subscriber_id == ids[id_index]:
                i = id_index
                break
        if i is not -1:
            self.subscribers.remove(i)

    def generateUniqueID(self, ids):
        return max(ids) + 1
