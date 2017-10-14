from representation.controllers import GENERIC_TYPES
from core.mechanics import TDLTracker, ColorTracker
from representation.custom_controllers import CUSTOM_TYPES
from utils.patch_selector import PatchSelectorManager
from utils.config import DEFAULT_CONFIGS
from collections import namedtuple

RESPONSE_TYPES = {**GENERIC_TYPES, **CUSTOM_TYPES}


class _Director:
    '''Super class of Directors'''

    def __init__(self):
        self.last_response = ''
        self.extended_manager = None

    def manageIOResponse(self, response):
        raise NotImplementedError

    def manageEventResponse(self, ev_type, rs):
        raise NotImplementedError

    def assignExtendedController(self, controller_id, manager):
        self.extended_manager = (controller_id, manager)

    def getLastResponse(self):
        return self.last_response


class UserDirector(_Director):
    def __init__(self):
        super(UserDirector, self).__init__()

    def manageIOResponse(self, response):
        if response.getType() == RESPONSE_TYPES['motion']:
            self.last_response = response.getData().decode('utf-8')
            if self.last_response != '':
                print('Controller says:', self.last_response)

    def manageEventResponse(self, ev_type, rs):
        if self.extended_manager:
            idm, manager = self.extended_manager
            if ev_type == 'keyboard':
                manager.writeController(idm, rs)


class UIDirector(_Director):
    def __init__(self):
        super(UIDirector, self).__init__()
        self.app = None

    def manageIOResponse(self, response):
        if response.getType() == RESPONSE_TYPES['local_video']:
            self.last_response = response.getData()
        elif response.getType() == RESPONSE_TYPES['kinect']:
            _, self.last_response = response.getData()
            self.last_response = self.last_response[0]
        elif response.getType() == RESPONSE_TYPES['stream']:
            self.last_response = response.getData()

        if not self.app:
            return
        self.app.updateVideoState(self.last_response)

    def manageEventResponse(self, ev_type, rs):
        if ev_type == 'tracking':
            self.app.setRegionToDraw(rs[0][0], rs[0][1])

    def assignApplicationInstance(self, app):
        self.app = app


class ColorTrackingDirector(_Director):
    def __init__(self):
        super(ColorTrackingDirector, self).__init__()
        self.mechanism = ColorTracker(DEFAULT_CONFIGS)
        self.listener = None

    def manageIOResponse(self, response):
        if response.getType() == RESPONSE_TYPES['local_video']:
            self.last_response = response.getData()
            self.trackNextFrame()
        elif response.getType() == RESPONSE_TYPES['stream']:
            self.last_response = response.getData()
            self.trackNextFrame()

    def setTrackingListener(self, listener):
        self.listener = listener

    def trackNextFrame(self):
        response = self.mechanism.findTarget(self.last_response)

        self.solveIssuedResponse(response)

    def solveIssuedResponse(self, response):
        if response is not None:
            self.listener.manageEvent(response)


class TrackingDirector(_Director):
    def __init__(self, root_patch_name=''):
        super(TrackingDirector, self).__init__()
        self.tracking_state = TDLTracker.STATE_UNINITIATED
        self.mechanism = TDLTracker()
        self.root_patch_name = root_patch_name
        self.lock = False
        self.patch = None
        self.listener = None

        if not root_patch_name:
            self.root_patch_name = DEFAULT_CONFIGS['default_patch_name']

    def manageIOResponse(self, response):
        if response.getType() == RESPONSE_TYPES['local_video']:
            self.last_response = response.getData()
            self.trackNextFrame()
        elif response.getType() == RESPONSE_TYPES['stream']:
            self.last_response = response.getData()
            self.trackNextFrame()

    def setTrackingListener(self, listener):
        self.listener = listener

    def trackNextFrame(self):
        if self.lock:
            # print('Tracker was called and dropped, as it is locked')
            return
        else:
            self.lock = True

            # Look for base patch, either with default name or with the name received by the class
            if self.patch is None:
                self.patch = PatchSelectorManager.loadPersistentCopy(self.root_patch_name)
                self.mechanism.assignRootPatch(self.patch)

            # Await response from mechanism depending on the tracking state
            response = self.mechanism.feedFrame(self.last_response, self.tracking_state)
            self.solveIssuedResponse(response)

            # Enable this method to be called again
            self.lock = False

    def solveIssuedResponse(self, response):
        if response is not None:
            self.tracking_state = TDLTracker.STATE_INITIATED
            self.listener.manageEvent(response, self.mechanism.root_patch.patch)


class StabilityDirector(_Director):
    '''
        StabilityDirector compares the current position of the drone with a saved snapshot
        position and returns the direction gradient for optimal stability.
        The stability director must be initialized with a snapshot of the drone, a snapshot is
        defined as: (X, Y, W, H) where X, Y are the upper left positions of the drone boundbox,
        and W, H are its size.
    '''

    SnapShot = namedtuple('SnapShot', ['x', 'y', 'h', 'w'])
    MARGINS = SnapShot(x=5, y=5, h=5, w=10)
    VZERO = SnapShot(x=0, y=0, h=0, w=0)

    def __init__(self, snapshot):
        self._snapshot = snapshot

    def resetSnapShot(self, snapshot):
        self._snapshot = snapshot

    def _calculateDistanceVector(self, snapshot):
        def perimeter(snap):
            return 2 * (snap.w + snap.h)
        dvector = [0, 0, 0]

        xdelta = snapshot.x - self._snapshot.x
        ydelta = snapshot.y - self._snapshot.y
        pdelta = perimeter(snapshot) - perimeter(self._snapshot)

        if abs(xdelta) > self.MARGINS.x:
            dvector[0] = xdelta // abs(xdelta)
        if abs(ydelta) > self.MARGINS.y:
            dvector[1] = ydelta // abs(ydelta)
        if abs(pdelta) > perimeter(self.MARGINS):
            dvector[2] = pdelta // abs(pdelta)

        return dvector

    def getMovementGradients(self, snapshot, filter_size=3):
        gradient_vector = self._calculateDistanceVector(snapshot)
        return gradient_vector[0: filter_size]


class AIDirector(_Director):
    def __init__(self):
        super(UserDirector, self).__init__()
