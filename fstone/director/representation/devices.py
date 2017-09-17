'''
    This project only supports Kinect device, but any other device can be adapted as long as it
    implements the *serialize* method.

    Also, only one Kinect at a time can be used. To assure that singleton pattern is enforced
    from the controller superclass
'''
from representation.lang import Drony

LocalDevice = {
    'port': '/home/kenshinn/Documents/Proyects/Python/flight-stone/extra/example_videos/',
    'identifier': 'VID_20170917_162916636.mp4',
    'datatype': type(bytes),
    'baudrate': (720, 1280, 3),
    'language': None,
}


LocalDeviceHQ = {
    'port': '/home/asmateus/Git/flight-stone/extra/example_videos/',
    'identifier': 'drone_flying.mp4',
    'datatype': type(bytes),
    'baudrate': (1080, 1920, 3),
    'language': None,
}

ArduinoUnoDevice = {
    'port': None,
    'identifier': '2341:0043',  # idVendor - idProduct
    'datatype': type(str),
    'baudrate': 115200,
    'language': Drony,
}

ArduinoMegaDevice = {
    'port': None,
    'identifier': '2341:0042',  # idVendor - idProduct
    'datatype': type(str),
    'baudrate': 115200,
    'language': Drony,
}

PIC16F1827Device = {
    'port': None,
    'identifier': '10C4:EA60',  # idVendor - idProduct
    'datatype': type(str),
    'baudrate': 9600,
    'language': Drony,
}
