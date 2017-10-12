'''Non generic controllers here. '''
from representation.controllers import Controller
from representation.controllers import genCheckDevice, checkDevice
from representation.devices import LocalDevice, StreamDeviceStarTEC, KinectDevice
from representation.responses import IOResponse, RESPONSE_STATUS
from time import sleep
import traceback
import sys
import subprocess as sp
import numpy as np
import os.path


try:
	import freenect
except Exception:
	print('** x	Current System does not support Kinect Device **')

# Custom types start with 2
CUSTOM_TYPES = {
    'local_video': 2,
    'kinect': 3,
    'stream': 4,
}


class LocalVideoController(Controller):
    def __init__(self, device=LocalDevice):
        super(LocalVideoController, self).__init__()

        self.device = device
        self.pth = self.deviceQuery()
        self.controller_type = CUSTOM_TYPES['local_video']

        # Initialize the response instance
        self.response = IOResponse(self.controller_type)

        # Define connection pipe to file
        self.pipe = None

    def deviceQuery(self):
        pth = self.device['port'] + self.device['identifier']
        if os.path.isfile(pth):
            return pth
        else:
            return None

    @genCheckDevice
    def pullData(self):
        try:
            if self.pth:
                cmd = [
                    'ffmpeg',
                    '-i', self.pth,  # Define path of the video
                    '-f', 'image2pipe',  # Send output to pipe
                    '-pix_fmt', 'rgb24',  # Pixel format as rgb24
                    '-vcodec', 'rawvideo', '-'  # Make output raw
                ]

                self.pipe = sp.Popen(
                    cmd,
                    stdin=sp.PIPE,
                    stderr=sp.PIPE,
                    stdout=sp.PIPE,
                    bufsize=10**8
                )
                while True:
                    if self.endtr:
                        self.pipe.close()
                        return

                    # Slow video to a good rate, for streaming to a person
                    sleep(0.03)
                    frame = self.pipe.stdout.read(np.prod(self.device['baudrate']))
                    self.pipe.stdout.flush()

                    frame = np.fromstring(frame, dtype='uint8')
                    frame = frame.reshape(self.device['baudrate'])

                    self.response.assignStatus(RESPONSE_STATUS['OK'])
                    self.response.assignData(frame)
                    yield self.response
        except Exception:
            traceback.print_exc(file=sys.stdout)
            self.endCommunication()
            print('Video ended or interrupted, dropped Buffer')

    def endCommunication(self):
        self.endtr = True


class StreamController(Controller):
    def __init__(self, device=StreamDeviceStarTEC):
        super(StreamController, self).__init__()
        self.device = device
        self.pth = self.deviceQuery()

        self.controller_type = CUSTOM_TYPES['stream']

        # Initialize the response instance
        self.response = IOResponse(self.controller_type)

    def deviceQuery(self):
        self.device['port'] = '/dev/video1'
        return '/dev/video1'

    @genCheckDevice
    def pullData(self):
        try:
            if self.pth:
                cmd = [
                    'ffmpeg',
                    '-i', self.device['port'],  # Define path of the video
                    '-f', 'image2pipe',  # Send output to pipe
                    '-pix_fmt', 'rgb24',  # Pixel format as rgb24
                    '-vcodec', 'rawvideo', '-'  # Make output raw
                ]

                self.pipe = sp.Popen(
                    cmd,
                    stdin=sp.PIPE,
                    stderr=sp.PIPE,
                    stdout=sp.PIPE,
                    bufsize=10**8
                )
                while True:
                    if self.endtr:
                        self.pipe.close()
                        return

                    frame = self.pipe.stdout.read(np.prod(self.device['baudrate']))
                    self.pipe.stdout.flush()

                    frame = np.fromstring(frame, dtype='uint8')
                    frame = frame.reshape(self.device['baudrate'])

                    self.response.assignStatus(RESPONSE_STATUS['OK'])
                    self.response.assignData(frame)

                    yield self.response
        except Exception:
            traceback.print_exc(file=sys.stdout)
            self.endCommunication()
            print('Video ended or interrupted, dropped Buffer')

    def endCommunication(self):
        self.endtr = True


class KinectController(Controller):
    def __init__(self, device=KinectDevice):
        super(KinectController, self).__init__()
        self.device = device

        self.controller_type = CUSTOM_TYPES['kinect']

        # Initialize the response instance
        self.response = IOResponse(self.controller_type)

    def deviceQuery(self):
        # Check if the Kinect is present in the system. That is, the output of the lsusb command
        # list all the kinect devices (audio, video and motor)

        devices_query = sp.check_output('lsusb')
        devices_query = devices_query.decode('utf-8')

        required_ids = list(self.device['identifier'])
        for device in devices_query.split('\n'):
            if device:
                # Fetch the device ID
                ID = device.split('ID')[1].split(' ')[1]

                if ID.lower() in required_ids:
                    required_ids.remove(ID)

        if len(required_ids):
            return None
        else:
            return 'NA'

    @genCheckDevice
    def pullData(self):
        try:
            while True:
                # The idea is to return four data types: RGB image, Depth image and angle state
                depth, rgb = freenect.sync_get_depth(), freenect.sync_get_video()

                self.response.assignStatus(RESPONSE_STATUS['OK'])
                self.response.assignData((depth, rgb))

                yield self.response
        except Exception:
            traceback.print_exc(file=sys.stdout)
            print('Failed to retreive Kinect data')

    @checkDevice
    def pushData(self, data):
        pass
