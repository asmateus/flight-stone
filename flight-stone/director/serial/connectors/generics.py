from devices import ArduinoUnoDevice
from serial.tools.list_ports import comports
import serial
import re

ROOT_DEVICE_PATH = '/dev/bus/usb/'
DEVICE_QUERY_EXPRESSION = re.compile(
    "Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$",
    re.I)

GENERIC_TYPES = {
    'none': 0,
    'hw_generic_client': 1,
}


def checkDevice(func):
    def check(*args):
        if args[0].device:
            if(args[0].deviceQuery()):
                func(*args)
        else:
            return
    return check


class Controller:
    device = None

    def pullData(self):
        raise NotImplementedError

    def pushData(self):
        raise NotImplementedError

    def deviceQuery(self):
        devices = comports()
        for d in devices:
            if d.hwid.split('PID')[1].split()[0][1:] == self.device['identifier']:
                self.device['port'] = d.device
                return d.device
        return None

    def serialize(self, packet):
        raise NotImplementedError


class GenericMotionController(Controller):

    '''The GenericMotionController by default manipulates an Arduino Uno system. With drony
    protocol language. This class supports sudden device disconnection and immediate recovery
    upon reconnection; special thanks to sorelyss (Github) for the code provided.'''

    def __init__(self):
        super(GenericMotionController, self).__init__()

        self.device = ArduinoUnoDevice

    @checkDevice
    def pullData(self):
        try:
            with serial.Serial(self.device['port'], self.device['baudrate'], timeout=10) as ser:
                while(1):
                    print(ser.readline())
        except Exception:
            print('Device disconnected. Retrying...')
            while not self.deviceQuery():
                pass
            self.pullData()

    @checkDevice
    def pushData(self):
        pass
