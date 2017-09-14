import json
import os

PTH = os.path.dirname(os.path.abspath(__file__)).split('flight-stone')[0]
PTH += 'flight-stone/'
CONFIG_FILE = 'fstone/config/flight-stone.json'
DEFAULT_CONFIGS = dict()

with open(PTH + CONFIG_FILE, 'rb') as jfile:
    DEFAULT_CONFIGS = json.load(jfile)


def loadConfigInstance():
    with open(PTH + CONFIG_FILE, 'rb') as jfile:
        DEFAULT_CONFIGS = json.load(jfile)
        return DEFAULT_CONFIGS


def saveDefaultConfig(config):
    with open(PTH + CONFIG_FILE, 'wb') as jfile:
        jfile.write(json.dumps(config, sort_keys=True, indent=4).encode('utf8'))
