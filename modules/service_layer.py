from modules.domain_modules import spectral_analysis # spectral analysis with Welch
from modules.domain_modules import sound_profiling # compare against known / anomaly sound profiles
from modules.domain_modules import alerts # trigger alerts
from modules.domain_modules import machine_learning  # save spectrum for ML

class AnalyzeSound:
  def __init__(self, key):
    '''Spectral Analysis Class:
    Processes audio files and outputs spectrum data in the form of a Spectrum Class object.
    '''
    self.key = validate(key)
    pass

  def validate(key):
    # check JSON string against signed S3 url regex
    return re.match(key)

  def analyze(self):
    '''Processes a wav file into a Spectrum class object.'''
    pass
    # return Spectrum()


class UpdateSoundProfile:
  def __init__(self, profile):
      '''Update Sound Profile Class: Updates or creates sound profile based on ML framework.'''
      pass

  def validate(profile):
    # check JSON data against valid profile object properties
    # return re.match(profile)
    pass

  def update(self):
    pass
