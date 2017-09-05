from representation.controllers import GENERIC_TYPES
from representation.custom_controllers import CUSTOM_TYPES

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
            print('Controller says:', self.last_response)

    def manageEventResponse(self, ev_type, rs):
        if self.extended_manager:
            idm, manager = self.extended_manager
            if ev_type == 'keyboard':
                manager.writeController(idm, rs)


class AIDirector(_Director):
    def __init__(self):
        super(UserDirector, self).__init__()


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
