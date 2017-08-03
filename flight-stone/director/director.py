from interface.controllers import GenericMotionController, GENERIC_TYPES
from iomanager import IOManager
import time


class Director:
    '''Dummy director class'''

    def manageIOResponse(self, response):
        print(response)


if __name__ == '__main__':

    manager = IOManager().getInstance()
    controller = GenericMotionController()

    director = Director()

    dir_id = manager.addSubscriber(director, GENERIC_TYPES['motion'])
    con_id = manager.addController(controller)

    # manager.readController(con_id)

    for i in range(1000):
        manager.writeController(con_id, 'Hello, buddy!'.encode('utf-8'))
        time.sleep(3)
