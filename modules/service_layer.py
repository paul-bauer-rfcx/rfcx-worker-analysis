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
    def read(self, fs, guardian_id, audio_id):
        self.logger.info("""Reading sound file %s""" % (audio_id))
        # TO DO: Return read success/fail for Node to handle local file and SQS
        try:
            data, samplerate = load_sound.read_sound(fs)
        except Exception, e:
            self.logger.error("""Read-in failed for file: %s\n\t%s""" % (audio_id, e))
            exit(1)
        else:
            self.logger.info("Read-in successful for file: %s""" % (audio_id))
            return load_sound.Sound(data, samplerate, guardian_id, audio_id)

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
        self.spec_analyzer.add_spectrum(sound)
        self.logger.info("""Completed spectral analyis for file: %s""" % (sound.file_id))

        # (2) create an audio finger print
        prof_meta = fingerprinting.Fingerprinter(sound).profile
        self.logger.info("""Completed fingerprinting for file: %s""" % (sound.file_id))

        # (3) classify the sound via known sound sources
        sound_classification.SoundClassifier(self.logger).classify(prof_meta)
        self.logger.info("""Completed fingerprinting for file: %s""" % (sound.file_id))

        # (4) use ML to determine whether the sound is an anomaly
        # Todo: add requirements for anomaly detection, then add these lines
        repo = db_layer.AnomalyDetectionRepo()
        anomaly_detection.AnomalyDetector(self.logger, repo).determine_anomaly(prof_meta)
        self.logger.info("""Completed ML analysis for file: %s""" % (sound.file_id))

        # (5)
        prof_final = sound_profiling.SoundProfiler(prof_meta).profile
        self.logger.info("""Completed profiling for file: %s""" % (sound.file_id))

        # (6) alert if necessary
        alert = alerts.Alert(prof_final)
        self.logger.info("""Sent all required alerts for file: %s""" % (sound.file_id))


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
