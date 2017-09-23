import freenect
import time
import sys

TILT_MAX = 30
TILT_STEP = 10
TILT_START = 0


ctx = freenect.init()
dev = freenect.open_device(ctx, freenect.num_devices(ctx) - 1)

if not dev:
    freenect.error_open_device()

print("Starting TILT Cycle")
for tilt in range(TILT_START, TILT_MAX+TILT_STEP, TILT_STEP):
    print("Setting TILT: ", tilt)
    freenect.set_tilt_degs(dev, tilt)
    time.sleep(3)

freenect.set_tilt_degs(dev, 0)
