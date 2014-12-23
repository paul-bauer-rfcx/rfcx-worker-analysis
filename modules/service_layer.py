from modules.domain_modules import load_sound  # download and load audio file from s3 storage
from modules.domain_modules import spectral_analysis # spectral analysis of audio
from modules.domain_modules import sound_profiling # compare against known / anomaly sound profiles
from modules.domain_modules import alerts # trigger alerts

class AnalyzeSound:
  def __init__(self, key):
    '''Spectral Analysis Class:
    Processes audio files and outputs spectrum data in the form of a Spectrum Class object.
    '''
    # validate JSON input data
    if self.validate(key):
      # analyze audio file
      self.analyze(key)
    else:
      raise Exception("Key passed to AnalyzeSound was not valid.")

  def validate(self, key):
    # check JSON string against signed S3 url regex
    # return re.match(key)
    return True

  def analyze(self, key):
    '''Processes a wav file into a spectrum, profile it, and trigger results.'''
    sound = load_sound.Sound(key)
    spectrum = spectral_analysis.SpectralAnalysis(sound).spectrum
    profile = sound_profiling.SoundProfiler(spectrum).profile
    alert = alerts.Alert(profile)


class UpdateSoundProfile:
  def __init__(self, profile, settings):
      '''Update Sound Profile Class: Updates or creates sound profile based on ML framework.'''
      pass

  def validate(profile):
    # check JSON data against valid profile object properties
    # return re.match(profile)
    pass

  def update(self):
    pass
