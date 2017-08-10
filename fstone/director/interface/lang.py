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
    word_size=8,
    verbs=('m', 's', 'f', 'o', 'r'),
    adjectives=('l', 'r', 'u', 'd', '1',
                '2', '3', '4', '5', '6', '7', '8', '9', '0'),
)


class DronyManager:
    def __init__(self):
        self.persistent_adjective = '125'
        self.language = Drony
        self.keys = ['a', 'w', 's', 'd', 'o', 'u', 'h', 'j', 'k',
                     '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.drony_val = ['ml', 'mu', 'md', 'mr', 's', 'ru', 'rl', 'rd', 'rr',
                          '', '', '', '', '', '', '', '', '', '']
        self.associator = {k: v for (k, v) in zip(self.keys, self.drony_val)}

    def manage(self, ch):
        word = ''
        try:
            word_root = self.associator[ch]
            if not word_root:
                level = str(self.translateIntensityLevel(ch))
                self.persistent_adjective = '0' * (3 - len(level)) + level
            else:
                word = word_root + self.persistent_adjective
                instr_count = len(word)
                word = str(instr_count) + word + '#' * (8 - 1 - len(word))
        except Exception:
            pass

        return word

    def translateIntensityLevel(self, ch):
        return int(int(ch) * 255 / 9)
