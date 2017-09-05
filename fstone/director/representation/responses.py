
RESPONSE_STATUS = {
    'OK': 1,
    'ERROR': 2,
    'WAITING': 3,
}


class _Response:
    def __init__(self, response_type):
        self._type = response_type
        self._status = RESPONSE_STATUS['WAITING']
        self._data = None

    def assignStatus(self, status):
        self._status = status

    def assignData(self, data):
        self._data = data

    def getData(self):
        raise NotImplementedError

    def getType(self):
        return self._type


class IOResponse(_Response):
    '''
    IOResponse wraps the controller responses to a standard way. The type of the IOResponse
    is directly hereded from the specific controller
    '''

    def __init__(self, response_type):
        super(IOResponse, self).__init__(response_type)

    def getData(self):
        return self._data
