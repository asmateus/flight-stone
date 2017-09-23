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
import itertools

_Language = namedtuple('Language', [
    'datatype',
    'structure',
    'word_size',
    'triggers',
    'verbs',
    'adjectives',
    'v_mapping',
    'a_mapping'])


# Implementation of MotionController language, alias Drony
_DronyLangDef = _Language(
    datatype=str,
    structure=r'[1..9]<><><>[1..255]###',
    word_size=8,
    triggers=(
        'd', 'a',  # left and right
        'u', 'j',  # up and down
        'w', 's',  # foward and backward
        'h', 'k',  # rotate left and right
        'o',       # start/stop toogle
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
    ),
    verbs=('m', 'r', 's'),  # Move, rotate, start
    adjectives=(
        'l', 'r', 'u', 'd', 'f', 'b'
    ),
    v_mapping={
        'm': 'daujws',
        'r': 'hk',
        's': 'o',
    },
    a_mapping={
        'l': 'dh',
        'r': 'ak',
        'u': 'u',
        'd': 'j',
        'f': 'w',
        'b': 's',
        's': 'o',
    },
)


class Drony:
    '''
        A trigger is a specific user action that has a meaning for this language
        such as move up, down, left, right, foward, backwards, or start and stop
        the engine. Each trigger needs to be associated with a translation value
        that is sent back to the controller.
        Adjectives do not generate response data, but configure future response
        data; you can avoid changing the intensity of adjectives of specifics verbs
        by specifing them in the fixed relations array.
    '''

    DEF_PERSISTENT_ADJECTIVE = '100'
    LANG = _DronyLangDef
    FIXED_RELATIONS = {
        'mr': '124',
        'ml': '124',
        'mf': '124',
        'mb': '124',
        'md': '124',
        'mu': '090',
    }
    EXCLUDED_RELATIONS = [
        'ru', 'rd', 'rf', 'rb', 'sl', 'sr', 'su', 'sd', 'sb', 'sf'
    ]
    OBLIGATORY_RELATIONS = ['ss']

    def __init__(self):
        mov = [''.join(m) for m in itertools.product(Drony.LANG.verbs, Drony.LANG.adjectives)]
        mov = [i for i in mov if i not in Drony.EXCLUDED_RELATIONS]
        mov.extend(Drony.OBLIGATORY_RELATIONS)
        self.associator = {
            k: v for (k, v) in zip(Drony.LANG.triggers, mov)
            if k in Drony.LANG.v_mapping[v[0]] and k in Drony.LANG.a_mapping[v[1]]
        }
        self.persistent_adjective = Drony.DEF_PERSISTENT_ADJECTIVE

    def manage(self, ch):
        word = ''
        if ch in self.associator.keys():
            word = self.associator[ch]
            if word in Drony.FIXED_RELATIONS.keys():
                word = word + str(Drony.FIXED_RELATIONS[word])
            else:
                word = word + str(self.persistent_adjective)
            instr_count = len(word)
            word = str(instr_count) + word + '#' * (Drony.LANG.word_size - 1 - len(word))
        else:
            try:
                int(ch)
                level = str(self.translateIntensityLevel(ch))
                self.persistent_adjective = '0' * (3 - len(level)) + level
            except Exception:
                pass

        return word

    def translateIntensityLevel(self, ch):
        return int(int(ch) * (124) / 9)


class KinectLang:
    pass
