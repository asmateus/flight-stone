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


class _PatchBasedMechanics():
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
