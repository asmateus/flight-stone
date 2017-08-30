class Director:
    '''Dummy director class'''

    def __init__(self):
        self.last_response = ''
        self.extended_manager = None

    def manageIOResponse(self, response):
        self.last_response = response.decode('utf-8')
        print('Controller says:', self.last_response)

    def manageEventResponse(self, ev_type, rs):
        if self.extended_manager:
            idm, manager = self.extended_manager
            if ev_type == 'keyboard':
                manager.writeController(idm, rs)

    def assignExtendedController(self, controller_id, manager):
        self.extended_manager = (controller_id, manager)

    def getLastResponse(self):
        return self.last_response
