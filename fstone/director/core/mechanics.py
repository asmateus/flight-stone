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
import cv2


def checkPatch(func):
    def check(*args):
        if args[0].root_patch is not None:
            return func(*args)
        else:
            return
    return check


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
    STATE_UNINITIATED = 0
    STATE_INITIATED = 1
    STATE_INTERRUPTED = 2
    STATE_FINISHED = 3

    def __init__(self, root_patch=None):
        self.root_patch = root_patch
        self.descriptor = None

    def assignRootPatch(self, patch):
        if patch.descriptions[0][0] == str(self.descriptor):
            self.root_patch = patch

    def findTarget(self, obj):
        raise NotImplementedError

    def updateTarget(self):
        raise NotImplementedError

    def getDescriptors(self):
        raise NotImplementedError

    def restartDescriptors(self):
        raise NotImplementedError


class FeatureFusionUpdateMechanic(_PatchBasedMechanics):
    def __init__(self, default_patch=None):
        super(FeatureFusionUpdateMechanic, self).__init__()


class TDLTracker(_PatchBasedMechanics):
    '''
        This is a Tracking, learning and detection tracker, implemented in OpenCV.
        This is the only instance that requires the OpenCV library, use other trackers if you
        do not wish to depend on it.
    '''

    def __init__(self, root_patch=None):
        super(TDLTracker, self).__init__(root_patch)
        self.descriptor = ColorHistogramExtractor()
        self.match_method = cv2.TM_CCOEFF
        self.current_frame = None
        self.patch_h, self.patch_w = 0, 0

        self.dispatcher = {
            TDLTracker.STATE_UNINITIATED: self.findTarget,
            TDLTracker.STATE_INITIATED: self.updateTarget,
            TDLTracker.STATE_INTERRUPTED: self.restartDescriptors,
            TDLTracker.STATE_FINISHED: self.updateTarget,
        }

    def assignRootPatch(self, patch):
        super().assignRootPatch(patch)
        self.patch_h, self.patch_w, _ = self.root_patch.patch.shape

    @checkPatch
    def feedFrame(self, frame, external_status):
        self.current_frame = frame
        return self.dispatcher[external_status]()

    def findTarget(self):
        result = cv2.matchTemplate(self.current_frame, self.root_patch.patch, self.match_method)
        _, _, _, max_loc = cv2.minMaxLoc(result)

        # Select found target
        target_top_left = max_loc
        target_bottom_right = (
            target_top_left[0] + self.patch_w,
            target_top_left[1] + self.patch_h)

        # Update Patch with current info
        patch = self.root_patch.copy()
        patch.patch = self.current_frame[
            target_top_left[1]: target_bottom_right[1] + 1,
            target_top_left[0]: target_bottom_right[0] + 1]
        self.assignRootPatch(patch)

        return (target_top_left, target_bottom_right)

    def detectObjectInFrame(self, frame, raw_object):
        pass
