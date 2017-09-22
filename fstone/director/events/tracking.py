'''
    Manages tracking events and handles listeners.
'''


class TrackingListener:
    def __init__(self):
        self.subscribers = []
        self.event_type = 'tracking'

    def manageEvent(self, response, ov):
        for subscriber_stamp in self.subscribers:
            subscriber, _ = subscriber_stamp
            subscriber.manageEventResponse(self.event_type, [response, ov])

    def addSubscriber(self, subscriber):
        gen_id = 0
        if self.subscribers:
            _, ids = zip(*self.subscribers)
            gen_id = self.generateUniqueID(ids)
        self.subscribers.append((subscriber, gen_id))
        return gen_id

    def removeSubscriber(self, subscriber_id):
        _, ids = zip(*self.subscribers)
        i = -1
        for id_index in range(len(ids)):
            if subscriber_id == ids[id_index]:
                i = id_index
                break
        if i is not -1:
            self.subscribers.remove(i)

    def generateUniqueID(self, ids):
        return max(ids) + 1
