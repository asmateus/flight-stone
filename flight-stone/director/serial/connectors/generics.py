from collections import namedtuple

GENERIC_TYPES = {
    'none': 0,
    'hw_generic_client': 1,
}

Device = namedtuple('Device', ['port', 'identifier', 'datatype', 'baudrate', 'language'])


def checkDevice(func):
    def check(*args):
        print('checking device')
        if args[0].device:
            func(*args)
        else:
            raise NotImplementedError
    return check


class Controller:
    controller_type = GENERIC_TYPES['none']
    device = None

    def __init__(self, controller_type):
        Controller.controller_type = controller_type

    def pullData(self):
        raise NotImplementedError

    def pushData(self):
        raise NotImplementedError

    def serialize(self, packet):
        raise NotImplementedError


class GenericHWController(Controller):
    def __init__(self, controller_type):
        super(GenericHWController, self).__init__(controller_type)

        self.device = Device(port=0, identifier=0, datatype=0, baudrate=0, language=0)

    @checkDevice
    def pullData(self):
        print('Pulling')

    @checkDevice
    def pushData(self):
        print('Pushing')
