'''
    This is the language module; as an alternative you can also (in your mind) refer to this as the
    protocol module. It holds the Packet structure for device inter-communication. A language must
    define the following elements for its words:
    -> word datatype
    -> word structure (regex)
    -> word length
    -> finite list of verbs (actions)
    -> finite list of adjectives (information)
    By default we only implement the Kinect language and the MotionController language.
'''
from collections import namedtuple

_Language = namedtuple('Language', ['datatype', 'structure', 'word_size', 'verbs', 'adjectives'])

# Implementation of MotionController language, alias Drony
Drony = _Language(
    datatype=str,
    structure=r'?<><><>',
    word_size=32,
    verbs=('mov', 'sta', 'pff', 'pon', 'rot'),
    adjectives=('lft', 'rht', 'up', 'dwn', 'sus', 'smt'),
    )
