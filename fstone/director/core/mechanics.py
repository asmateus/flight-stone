'''
    A patch-based mechanic is composed of three elements, a feature representation of the element,
    a search algorithm to find the element in an image and a patch updater.
    The interactions with the mechanics is easy, it has three main methods:
    * findTarget(array):    returns the upper x,y and the w,h of the bounding box in which the
                            element is.
    * getDescriptors():     returns the description array of the last patch found.
    * restartDescriptors(): the patch is reseted to the default version. A default version is
                            always madatory.
'''
from core.features import ColorHistogramExtractor


class HistogramDetector:
    '''
        This is a static class that does not support instantiation
    '''
    descriptor = ColorHistogramExtractor()

    def __init__(self):
        raise NotImplementedError

    @staticmethod
    def detectObject(object, source):
        pass


class _PatchBasedMechanics:
    DEFAULT_PATCH = None

    def __init__(self, default_patch=None):
        if default_patch:
            self.default_patch = default_patch
        else:
            self.default_patch = _PatchBasedMechanics.DEFAULT_PATCH

    def findTarget(self, obj):
        raise NotImplementedError

    def getDescriptors(self):
        raise NotImplementedError

    def restartDescriptors(self):
        raise NotImplementedError


class FeatureFusionUpdateMechanic(_PatchBasedMechanics):
    def __init__(self, default_patch=None):
        super(FeatureFusionUpdateMechanic, self).__init__()


class TDLTracker:
    '''
        This is a Tracking, learning and detection tracker, implemented in OpenCV.
        This is the only instance that requires the OpenCV library, use other trackers if you
        do not wish to depend on it.
    '''

    def __init__(self):
        pass

    def detectObjectInFrame(self, frame, raw_object):
        pass
