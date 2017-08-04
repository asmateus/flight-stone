'''
This manager this the link between hardware controller classes (communication boilerplate) and
end user requests. It keeps all connections alive, and therefore it should be instanciated only
once through out the execution of the program.

Singleton design pattern is implemented for this porpuse
'''
from threading import Thread


class IOManager():
    # Unique buffer instance
    instance = None

    @staticmethod
    def getInstance():
        if not IOManager.instance:
            IOManager.instance = IOManager()

        return IOManager.instance

    def __init__(self):
        self.controllers = []
        self.subscribers = []

    def __call__(self):
        pass

    def addController(self, controller):
        if IOManager.instance:
            gen_id = 0
            if IOManager.instance.controllers:
                _, ids, _ = zip(*IOManager.instance.controllers)
                gen_id = IOManager.instance.generateUniqueID(ids)
            IOManager.instance.controllers.append((controller, gen_id, None))
            return gen_id

    def addSubscriber(self, subscriber, scope):
        if IOManager.instance:
            gen_id = 0
            if IOManager.instance.subscribers:
                _, _, ids = zip(*IOManager.instance.subscribers)
                gen_id = IOManager.instance.generateUniqueID(ids)
            IOManager.instance.subscribers.append((subscriber, scope, gen_id))
            return gen_id

    def removeSubscriber(self, subscriber_id):
        if IOManager.instance:
            _, _, ids = zip(*IOManager.instance.subscribers)
            i = -1
            for id_index in range(len(ids)):
                if subscriber_id == ids[id_index]:
                    i = id_index
                    break
            if i is not -1:
                IOManager.instance.subscribers.remove(i)

    def generateUniqueID(self, ids):
        return max(ids) + 1

    def onControllerResponse(self, controller_type, response):
        if IOManager.instance:
            for subscriber_stamp in IOManager.instance.subscribers:
                subscriber, subscriber_scope, _ = subscriber_stamp
                if subscriber_scope == controller_type:
                    subscriber.manageIOResponse(response)

    def readController(self, controller_id):
        if IOManager.instance:
            action = None
            for stamp_index in range(len(IOManager.instance.controllers)):
                controller, stamp_id, action = IOManager.instance.controllers[stamp_index]
                if stamp_id == controller_id and action is None:
                    IOManager.instance.controllers[stamp_index] = (controller, stamp_id, 'r')
                    controller.endtr = False
                    act_thread = Thread(
                        None,
                        target=IOManager.instance._read,
                        args=(controller, stamp_index))
                    act_thread.start()
                    return

    def stopReading(self, controller_id):
        if IOManager.instance:
            for stamp_index in range(len(IOManager.instance.controllers)):
                controller, stamp_id, action = IOManager.instance.controllers[stamp_index]
                if stamp_id == controller_id:
                    controller.endtr = True
                    IOManager.instance.controllers[stamp_index] = (controller, stamp_id, None)
                    return

    def writeController(self, controller_id, data):
        if IOManager.instance:
            for stamp_index in range(len(IOManager.instance.controllers)):
                controller, stamp_id, action = IOManager.instance.controllers[stamp_index]
                if stamp_id == controller_id:
                    controller.pushData(data)
                return

    def _read(self, controller, stamp_index):
        if IOManager.instance:
            _, _, action = IOManager.instance.controllers[stamp_index]
            for result in controller.pullData():
                if result:
                    IOManager.instance.onControllerResponse(controller.controller_type, result)
                if not action:
                    controller.endtr = True

            # If endtr here is False, something wrong happened
            if not controller.endtr:
                while not controller.deviceQuery():
                    if controller.endtr:
                        return
                IOManager.instance._read(controller, stamp_index)
