'''
This is a two way serialization system. It buffers in both manager's data and orchesta information
for further stages of processing. Simply explained Serializer takes the input from a connected
device and fowards its information to any requester.

Buffer implements Singleton design pattern
'''

# from connectors.devices import KinectConnector


class Buffer():
    # Unique buffer instance
    instance = None

    @staticmethod
    def getInstance():
        if not Buffer.instance:
            Buffer.instance = Buffer()

        return Buffer.instance

    def __call__(self):
        pass


class MasterBuffer(Buffer):
    pass


class SlaveBuffer(Buffer):
    pass
