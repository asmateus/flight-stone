from devices import ArduinoUnoDevice
import subprocess
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
        df = subprocess.check_output("lsusb").decode('utf-8')
        devices = []
        for i in df.split('\n'):
            if i:
                info = DEVICE_QUERY_EXPRESSION.match(i)
                if info:
                    dinfo = info.groupdict()
                    dinfo['device'] = '%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                    devices.append(dinfo)
        for i in devices:
            if i['id'] == self.device.identifier:
                return i['device']
        return None

    def serialize(self, packet):
        raise NotImplementedError


class GenericMotionController(Controller):

    '''The GenericMotionController by default manipulates an Arduino Uno system. With drony
    protocol language'''

    def __init__(self):
        super(GenericMotionController, self).__init__()

        self.device = ArduinoUnoDevice

    @checkDevice
    def pullData(self):
        print('Pulling')

    @checkDevice
    def pushData(self):
        print('Pushing')
