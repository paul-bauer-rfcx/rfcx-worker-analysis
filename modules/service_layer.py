'''Service Layer Module.
Contains high-level code from which calls to the logic layer can be made.
'''
import re
import logging
import db_layer 
import os
#import custom RFCx modules from modules folder
from domain_modules import load_sound
from domain_modules import spectral_analysis
from domain_modules import fingerprinting
from domain_modules import sound_profiling
from domain_modules import sound_classification 
from domain_modules import anomaly_detection 
from domain_modules import alerts


# Todo: replace logging level by config file or command line options

class Service(object): 
    # standard dependencies for services 
    def __init__(self, logger): 
        self.logger = logger 

class AcquireAudio(Service): 
    def download(self, url, guardian_id): 
        self.logger.info("Downloading sound file '%s'", url)
        fs = load_sound.download_file(url)
        sound = self.read(fs, guardian_id)
        os.remove(fs)
        return sound

    def read(self, fs, guardian_id): 
        self.logger.info("Reading sound file '%s'", fs)
        data, samplerate = load_sound.read_sound(fs)
        return load_sound.Sound(data,samplerate, guardian_id)

class AnalyzeSound(Service):
    def __init__(self, logger, spectral_analyzer=spectral_analysis.SpectralAnalysis() ): 
        self.spec_analyzer = spectral_analyzer
        super(AnalyzeSound, self).__init__(logger)

    def analyze(self, sound):
        '''Analyze: Processes a wav file into a spectrum, profile it,
        and trigger results.
        '''
        # basic workflow 

        # (1) spectral analysis 
        self.logger.info("Performing spectral analyis for guardian '%s' ", sound.guardian_id)
        self.spec_analyzer.add_spectrum(sound)

        # (2) create an audio finger print 
        prof_meta = fingerprinting.Fingerprinter(sound).profile

        # (3) classify the sound via known sound sources 
        sound_classification.SoundClassifier(self.logger).classify(prof_meta)

        # (4) use ML to determine whether the sound is an anomaly 
        # Todo: add requirements for anomaly detection, then add these lines
        repo = db_layer.AnomalyDetectionRepo() 
        anomaly_detection.AnomalyDetector(self.logger, repo).determine_anomaly(prof_meta)

        # (5) 
        prof_final = sound_profiling.SoundProfiler(prof_meta).profile

        # (6) alert if necessary 
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
