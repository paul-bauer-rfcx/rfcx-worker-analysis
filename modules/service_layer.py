'''Service Layer Module.
Contains high-level code from which calls to the logic layer can be made.
'''
import re
import logging
import db_layer 
#import custom RFCx modules from modules folder
from domain_modules import load_sound
from domain_modules import spectral_analysis
from domain_modules import fingerprinting
from domain_modules import sound_profiling
from domain_modules import sound_classification 
from domain_modules import anomaly_detection 
from domain_modules import alerts


# Todo: replace logging level by config file or command line options

class AnalyzeSound(object):
    def __init__(self, key, meta_data):
        '''Spectral Analysis Class:
        Processes audio files and outputs spectrum data in the form
        of a Spectrum Class object.
        '''
        # validate JSON input data
        if self.validate(key):
        # analyze audio file
            self.analyze(key, meta_data)
        else:
            raise Exception("Key passed to AnalyzeSound ("+ key +") was not valid.")

    def validate(self, key):
        '''Validate: Check JSON string against signed S3 url regex
        '''
        regex = re.compile("https://rfcx-ark.s3-eu-west-1.amazonaws.com/")
        if regex.findall(key) != None:
            return True
        else:
            return False

    def analyze(self, key, meta_data):
        '''Analyze: Processes a wav file into a spectrum, profile it,
        and trigger results.
        '''

        # setup logging
        logger = logging.getLogger("services")
        logger.addHandler(logging.StreamHandler())  
        # Todo: add a handler to log in a file 
        # Todo: set logging level via config file / command line  
        logger.setLevel(level=logging.INFO)

        # basic workflow 

        # (1) download sound file 
        sound = load_sound.Sound(key, meta_data)

        # (2) spectral analysis 
        spectrum = spectral_analysis.Spectrum(sound)

        # (3) create an audio finger print 
        prof_meta = fingerprinting.Fingerprinter(spectrum).profile

        # (4) classify the sound via known sound sources 
        sound_classification.SoundClassifier(logger).classify(prof_meta)

        # (5) use ML to determine whether the sound is an anomaly 
        # Todo: add requirements for anomaly detection, then add these lines
        #repo = AnomalyDetectionRepo() 
        #AnomalyDetector(logger, repo).determine_anomaly(prof_meta)

        # (6) 
        prof_final = sound_profiling.SoundProfiler(prof_meta).profile

        # (7) alert if necessary 
        alert = alerts.Alert(prof_final)


class UpdateSoundProfile(object):
    def __init__(self, profile, settings):
        '''Update Sound Profile Class: Updates or creates sound profile
        based on ML framework.
        '''
        pass

    def validate(profile, settings):
        '''Validate: Check JSON string against valid profile object properties'''
        pass

    def update(self):
        '''Update. Adds or edits sound profiles in the database.'''
        pass
