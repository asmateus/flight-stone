import os
import sys
import inspect

TEST_TARGET_PATH = '/fstone/director'

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir) + TEST_TARGET_PATH

# Make test target visible to python
sys.path.insert(0, parentdir)
