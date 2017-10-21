'''
    This project only supports Kinect device, but any other device can be adapted as long as it
    implements the *serialize* method.

    Also, only one Kinect at a time can be used. To assure that singleton pattern is enforced
    from the controller superclass
'''
from representation.lang import Drony, KinectLang

LocalDevice = {
    'port': '/home/asmateus/Git/flight-stone/extra/example_videos/',
    'identifier': 'VID_20170917_162916636.mp4',
    'datatype': type(bytes),
    'baudrate': (720, 1280, 3),
    'language': None,
}


StreamDeviceStarTEC = {
    'port': None,
    'identifier': '1c4f:3002',
    'datatype': type(bytes),
    'baudrate': (480, 640, 3),
    'language': None,
}


StreamDeviceGoPro = {
    'port': '/dev/video1',
    'identifier': '0603:8612',
    'datatype': type(bytes),
    'baudrate': (480, 640, 3),
    'language': None,
}


KinectDevice = {
    'port': None,
    'identifier': ('045e:02bf', '045e:02be', '045e:02c2'),
    'datatype': type(bytes),
    'baudrate': None,
    'language': KinectLang,
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
    'identifier': '10c4:ea60',  # idVendor - idProduct
    'datatype': type(str),
    'baudrate': 9600,
    'language': Drony,
}
