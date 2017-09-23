import subprocess as sp
import numpy as np
import cv2

URL = 'http://192.168.10.20:8080/video'
width = 1280
height = 720
pipe = sp.Popen([
    'ffmpeg',
    '-i', URL,
    '-loglevel', 'quiet',
    '-an',
    '-f', 'image2pipe',
    '-pix_fmt', 'bgr24',
    '-vcodec', 'rawvideo', '-'],
    stdin=sp.PIPE,
    stdout=sp.PIPE
)

while True:
    raw_image = pipe.stdout.read(width * height * 3)
    try:
        image = np.frombuffer(raw_image, dtype=np.uint8).reshape((height, width, 3))
        cv2.imshow('xyz', image)
        if cv2.waitKey(5) == 27:
            break
    except Exception:
        pass
