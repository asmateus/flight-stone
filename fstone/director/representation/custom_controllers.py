'''Non generic controllers here. '''
from representation.controllers import Controller
from representation.controllers import genCheckDevice
from representation.devices import LocalDevice
from representation.responses import IOResponse, RESPONSE_STATUS
from time import sleep
import traceback
import sys
import subprocess as sp
import numpy as np
import os.path


# Custom types start with 2
CUSTOM_TYPES = {
    'local_video': 2,
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
