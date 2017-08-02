'''
    This project only supports Kinect device, but any other device can be adapted as long as it
    implements the *serialize* method.

    Also, only one Kinect at a time can be used. To assure that singleton pattern is enforced
    from the controller superclass
'''
from interface.lang import Drony


class KinectDevice:
    pass


ArduinoUnoDevice = {
    'port': None,
    'identifier': '2341:0043',
    'datatype': type(str),
    'baudrate': 115200,
    'language': Drony,
}
