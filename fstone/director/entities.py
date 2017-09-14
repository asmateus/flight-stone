from representation.controllers import GENERIC_TYPES
from core.mechanics import TDLTracker
from representation.custom_controllers import CUSTOM_TYPES
from utils.patch_selector import PatchSelectorManager
from utils.config import DEFAULT_CONFIGS

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
            if not self.app:
                return
            self.app.updateVideoState(self.last_response)

    def assignApplicationInstance(self, app):
        self.app = app


class TrackingDirector(_Director):
    def __init__(self, root_patch_name=''):
        super(TrackingDirector, self).__init__()
        self.tracking_state = TDLTracker.STATE_UNINITIATED
        self.mechanism = TDLTracker()
        self.root_patch_name = root_patch_name
        self.lock = False
        self.patch = None

        if not root_patch_name:
            self.root_patch_name = DEFAULT_CONFIGS['default_patch_name']

    def manageIOResponse(self, response):
        if response.getType() == RESPONSE_TYPES['local_video']:
            self.last_response = response.getData()
            self.trackNextFrame()

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
            # self.lock = False

    def solveIssuedResponse(self, response):
        print('Response')


class AIDirector(_Director):
    def __init__(self):
        super(UserDirector, self).__init__()
