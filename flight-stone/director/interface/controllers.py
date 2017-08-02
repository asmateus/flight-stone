from serial.tools.list_ports import comports
from interface.devices import ArduinoUnoDevice
import serial

GENERIC_TYPES = {
    'none': 0,
    'motion': 1,
}


def checkDevice(func):
    def check(*args):
        if args[0].device:
            if(args[0].deviceQuery()):
                func(*args)
        else:
            return
    return check


def genCheckDevice(func):
    def check(*args):
        if args[0].device:
            if(args[0].deviceQuery()):
                yield from func(*args)
        else:
            return
    return check


class Controller:
    device = None
    controller_type = GENERIC_TYPES['none']
    endtr = False

    def pullData(self):
        raise NotImplementedError

    def pushData(self):
        raise NotImplementedError

    def deviceQuery(self):
        try:
            devices = comports()
            for d in devices:
                if d.hwid.split('PID')[1].split()[0][1:] == self.device['identifier']:
                    self.device['port'] = d.device
                    return d.device
        except Exception:
            return None
        return None

    def serialize(self, packet):
        raise NotImplementedError


class GenericMotionController(Controller):

    '''The GenericMotionController by default manipulates an Arduino Uno system. With drony
    protocol language. This class supports sudden device disconnection and immediate recovery
    upon reconnection; special thanks to sorelyss (Github) for the code provided.'''

    def __init__(self, device=ArduinoUnoDevice):
        super(GenericMotionController, self).__init__()

        self.device = device
        self.deviceQuery()
        self.controller_type = GENERIC_TYPES['motion']

    @genCheckDevice
    def pullData(self):
        try:
            with serial.Serial(self.device['port'], self.device['baudrate'], timeout=10) as ser:
                while(1):
                    if self.endtr:
                        return
                    yield ser.readline()
        except Exception:
            print('Device disconnected. Retrying...')

    @checkDevice
    def pushData(self, data):
        try:
            with serial.Serial(self.device['port'], self.device['baudrate'], timeout=10) as ser:
                ser.write(data)
        except Exception:
            print('Device disconnected. No retrying on pushing...')

    def endCommunication(self):
        self.endtr = True
