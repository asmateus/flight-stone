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
from core.trackers.kcftracker import KCFTracker
from collections import namedtuple
import numpy as np
import cv2

Point = namedtuple('Point', ['x', 'y'])


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
        self.original_patch = root_patch
        self.descriptor = None

    def assignRootPatch(self, patch):
        if patch.descriptions[0][0] == str(self.descriptor):
            if self.original_patch is None:
                self.original_patch = patch
            self.root_patch = patch

    def findTarget(self, obj):
        raise NotImplementedError

    def updateTarget(self):
        raise NotImplementedError

    def getDescriptors(self):
        raise NotImplementedError

    def restartTarget(self):
        raise NotImplementedError


class FeatureFusionUpdateMechanic(_PatchBasedMechanics):
    def __init__(self, default_patch=None):
        super(FeatureFusionUpdateMechanic, self).__init__()


class ColorTracker:
    @staticmethod
    def rgb2hsv(frame):
        return cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    @staticmethod
    def distance(p1, p2):
        if p1 is None or p2 is None:
            return 0
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def __init__(self, configs):
        # Target color is expressed in HSV color space
        self._color = [configs['default_hsi_tcolor_lower'], configs['default_hsi_tcolor_upper']]
        self._color = [np.array(c) for c in self._color]
        self._erosion_kernel = configs['default_erode_kernel_size']
        self._dilate_kernel = configs['default_dilate_kernel_size']
        self._previous_point = None

    def findTarget(self, frame):
        # Frame must be RGB
        # First obtain the respective HSV value
        frame_hsv = ColorTracker.rgb2hsv(frame)

        # Threshold the HSV image to get only red colors
        mask = cv2.inRange(frame_hsv, self._color[0], self._color[1])

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame, frame, mask=mask)
        ret, res = cv2.threshold(res, 20, 255, 0)

        # Reduce dimensionality of result
        res = res[:, :, 0]

        # If no drone was found, return None
        if len(set(res.flatten())) == 1:
            return None

        # Eliminate noise, and increment interesting areas
        kernel = np.ones((self._erosion_kernel, self._erosion_kernel), np.uint8)
        res = cv2.erode(res, kernel, iterations=1)
        kernel = np.ones((self._dilate_kernel, self._dilate_kernel), np.uint8)
        res = cv2.dilate(res, kernel, iterations=2)

        # Segmentate drone posible places via find contours. The drone will be chosen to be
        # the largest element of all. A second choice parameter is available, and that is, to
        # considerate the vecinity of the previous location only
        contours = cv2.findContours(res, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
        if not len(contours):
            return None

        mins_x, mins_y = list(), list()
        maxs_x, maxs_y = list(), list()
        for contour in contours:
            cnt = [c[0] for c in contour]
            cnt_x = [c[0] for c in cnt]
            cnt_y = [c[1] for c in cnt]
            mins_x.append(min(cnt_x))
            mins_y.append(min(cnt_y))
            maxs_x.append(max(cnt_x))
            maxs_y.append(max(cnt_y))

        dists_x = [ma - mi for ma, mi in zip(maxs_x, mins_x)]
        dists_y = [ma - mi for ma, mi in zip(maxs_y, mins_y)]

        areas = [x * y for x, y in zip(dists_x, dists_y)]

        index_of_largest = areas.index(max(areas))

        top_left_pt = (mins_x[index_of_largest], mins_y[index_of_largest])
        bottom_right_pt = (maxs_x[index_of_largest], maxs_y[index_of_largest])

        x, y = top_left_pt[0], top_left_pt[1]
        w, h = bottom_right_pt[0] - top_left_pt[0], bottom_right_pt[1] - top_left_pt[1]

        self._previous_point = (x + w // 2, y + h // 2)

        return ((x, y), (x + w, y + h))


class MixedTracker(_PatchBasedMechanics):
    '''
        This is a MixedTracker, it implements both TDLTracker and ColorTracker, when initializating
        this tracker you must specify which of the two will be the main tracker and which will be
        the support tracker. The default execution will be that of the main tracker, but, at fixed
        intervals, a second hand opinion is issued to the support tracker, via the method
        (getSupportDecision), and an agreement function is executed to determine the following
        state of the algorithm.

        Current limitations:
        The support tracker can not be a memory algorithm, that is, it can not rely on
        previous data as it is only called sporadically. As such, any tracker that subclasses
        _PatchBasedMechanics is not suitable for observing. Well, you can do it, but it is not
        recomended.
    '''

    MAXIMUM_AGREE_DISTANCE = 20

    @staticmethod
    def distance(p1, p2):
        if p1 is None or p2 is None:
            return 0
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def __init__(self, main=None, support=None):
        self._main = main
        self._support = support

        # Generalized call functions that receive the next frame as a parameter
        self._main_find = None
        self._support_find = None

        # Interval to check for support decision, counted in frames
        self.interval = 50

    def overloadFindFunctions(self, main_overload, support_overload):
        self._main_find = main_overload
        self._support_find = support_overload

    def findTarget(self, frame, state):
        response = None
        if self._main_find is not None and self._support_find is not None:
            # See if support help is required
            if self.interval == 50:
                self.interval = 0
                posible_main = self._main_find(frame, state)
                posible_support = self._support_find(frame)

                # Reach an agreement between the two conclusions
                response = self.agreement(main=posible_main, support=posible_support)

                # Change the main behavior, if possible, as a result of the agreement
                self.changeOnAgreement(response, frame)
            else:
                response = self._main_find(frame, state)
                self.interval += 1
        return response

    def getSupportDecision(self, frame):
        self._support_find(frame)

    def changeOnAgreement(self, agreement, frame):
        x, y = agreement[0][0], agreement[0][1]
        w, h = abs(x - agreement[1][0]), abs(y - agreement[1][1])
        self._main.resetPatch([x, y, w, h], frame)

    def agreement(main=None, support=None):
        if main is None or support is None:
            return main
        else:
            # Calculate the distance between the main and support decisions points
            # Use MixedTracker own distance function for this
            distance = MixedTracker.distance(main, support)

            # Tracked points differ too much
            if distance > MixedTracker.MAXIMUM_AGREE_DISTANCE:
                # Support method is trusted for x, y location. Main is trusted for size
                middle = (
                    support[0][0] + abs(support[0][0] - support[1][0]) // 2,
                    support[0][1] + abs(support[0][1] - support[1][1]) // 2)

                agreement = (
                    (middle[0] - abs(main[0][0] - main[1][0]) // 2,
                        middle[1] - abs(main[0][1] - main[1][1]) // 2),
                    (middle[0] + abs(main[0][0] - main[1][0]) // 2,
                        middle[1] + abs(main[0][1] - main[1][1]) // 2)
                )

                return agreement

            else:  # Tracked points are similar, trust main, unchanged
                return main


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
        self.tracker = None

        self.dispatcher = {
            TDLTracker.STATE_UNINITIATED: self.findTarget,
            TDLTracker.STATE_INITIATED: self.updateTarget,
            TDLTracker.STATE_INTERRUPTED: self.restartTarget,
            TDLTracker.STATE_FINISHED: self.updateTarget,
        }

    def assignRootPatch(self, patch):
        super().assignRootPatch(patch)
        self.patch_h, self.patch_w, _ = self.root_patch.patch.shape

    @checkPatch
    def feedFrame(self, frame, external_status):
        self.current_frame = frame
        return self.dispatcher[external_status]()

    def restartTarget(self):
        self.assignRootPatch(self.original_patch)
        self.findTarget()

    def resetPatch(self, min_patch, frame):
        self.tracker.init(min_patch, frame)

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
            target_top_left[0]: target_bottom_right[0] + 1, :]
        patch.p1 = Point(x=target_top_left, y=target_bottom_right)
        self.assignRootPatch(patch)

        self.tracker = KCFTracker(True, True, True)
        self.tracker.init(
            [target_top_left[0], target_top_left[1], self.patch_w, self.patch_h],
            self.current_frame)

        return (target_top_left, target_bottom_right)

    def updateTarget(self):
        box = self.tracker.update(self.current_frame)
        box = [int(b) for b in box]
        for b in box:
            if b < 0:
                print('ERROR')
                return

        # Update Patch with current info
        patch = self.root_patch.copy()
        patch.patch = self.current_frame[
            box[1]: box[1] + box[3] + 1,
            box[0]: box[0] + box[2] + 1, :]
        patch.p1 = Point(x=box[0], y=box[1])
        self.assignRootPatch(patch)

        return ((box[0], box[1]), (box[0] + box[2], box[1] + box[3]))
