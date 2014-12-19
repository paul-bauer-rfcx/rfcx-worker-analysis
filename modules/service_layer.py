from modules import spectral_analysis # spectral analysis with Welch
from modules import sound_profiling # compare against known / anomaly sound profiles
from modules import alerts # trigger alerts
from modules import machine_learning  # save spectrum for ML

# TO DO: Define stub classes/objects for the interfaces in service layer

class SpectralAnalysis():
  def __init__(self):
    '''Spectral Analysis Class:
    Processes audio files and outputs spectrum data in the form of a Spectrum Class object.
    '''
    pass

  def validate(self):
    pass

  def analyze():
    '''Processes a wav file into a Spectrum class object.'''
    pass
    # return Spectrum()


class Spectrum():
  def __init__(self):
    '''Spectrum Class: 
    Holds all data from the transformation of an audio file into it's 
    amplitude(dB) over frequency(Hz) values.'''
    pass

  def validate(self):
    pass
