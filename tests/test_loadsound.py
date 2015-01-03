import nose
import mock
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from modules.domain_modules import load_sound

# # setup a stub sound object to test with.
# @mock_sound = load_sound.Sound('../assets/test.wav', good_json)

# # test Sound objects init args respond correctly
# def testSoundCanOnlyTakeWavFiles():
#     assert False

# def testSoundHasDurationInFrames():
#     assert False

# def testSoundHasDurationInMilliseconds():
#     assert False

# def testSoundHasAudioDataAsNumpyArray():
#     assert False
