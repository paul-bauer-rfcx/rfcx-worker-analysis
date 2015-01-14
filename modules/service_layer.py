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
from domain_modules import sound_classification
from domain_modules import anomaly_detection
from domain_modules import alerts

# Todo: replace logging level by config file or command line options

class Service(object):
    # standard dependencies for services
    def __init__(self, logger):
        self.logger = logger

class AcquireAudio(Service):
    def read(self, fs, meta_data):
        self.logger.info("""Reading sound file %s""" % (meta_data["audio_id"]))
        try:
            sound = load_sound.read_sound(fs, meta_data)
        except Exception, e:
            self.logger.error("""Read-in failed for file: %s\n\t%s""" % (meta_data["audio_id"], e))
            exit(1)
        else:
            self.logger.info("Read-in successful for file: %s""" % (meta_data["audio_id"]))
            return sound

class AnalyzeSound(Service):
    def __init__(self, logger):
        super(AnalyzeSound, self).__init__(logger)

    def analyze(self, sound):
        '''Analyze: Processes a wav file into a spectrum, profile it,
        and trigger results.
        '''
        # (1) spectral analysis
        spectrum = spectral_analysis.Spectrum(sound)
        self.logger.info("""Completed spectrum generation for file: %s""" % (sound.meta_data['audio_id']))
        self.logger.warn("""Analyzing: %s""" %(sound.meta_data['audio_id']))

        # (2) create an audio finger print
        fingerprinter = fingerprinting.Fingerprinter(spectrum)
        fingerprinter.profile.get_harmonic_power()
        fingerprinter.profile.get_harmonic_sound_bounds()
        self.logger.info("""Completed fingerprinting for file: %s""" % (sound.meta_data['audio_id']))

        # (3) explicit detection and classification of sound against known sound sources
        prof_final = sound_classification.SoundClassifier(self.logger).classify_interest_areas(fingerprinter.profile)
        self.logger.info("""Completed classification for file: %s""" % (sound.meta_data['audio_id']))

        # (4) use ML to determine whether the sound is an anomaly
        # Todo: add requirements for anomaly detection, then add these lines
        repo = db_layer.AnomalyDetectionRepo()
        anomaly_detection.AnomalyDetector(self.logger, repo).determine_anomaly(prof_final)
        self.logger.info("""Completed ML analysis for file: %s""" % (sound.meta_data['audio_id']))

        # (5) send alerts if necessary
        alert_sender = alerts.AlertSender(self.logger, prof_final)
        alert_sender.push_alerts()

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
