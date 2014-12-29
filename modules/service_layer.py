'''Service Layer Module.
Contains high-level code from which calls to the logic layer can be made.
'''
import re
# import custom RFCx modules from modules folder
# from modules.domain_modules import load_sound
# from modules.domain_modules import spectral_analysis
# from modules.domain_modules import fingerprinting
# from modules.domain_modules import sound_profiling
# from modules.domain_modules import alerts

# class AnalyzeSound(object):
#     def __init__(self, key, meta_data):
#         '''Spectral Analysis Class:
#         Processes audio files and outputs spectrum data in the form
#         of a Spectrum Class object.
#         '''
#         # validate JSON input data
#         if self.validate(key):
#         # analyze audio file
#             self.analyze(key, meta_data)
#         else:
#             raise Exception("Key passed to AnalyzeSound ("+ key +") was not valid.")

#     def validate(self, key):
#         '''Validate: Check JSON string against signed S3 url regex
#         '''
#         regex = re.compile("https://rfcx-ark.s3-eu-west-1.amazonaws.com/")
#         if regex.findall(key) != None:
#             return True
#         else:
#             return False

#     def analyze(self, key, meta_data):
#         '''Analyze: Processes a wav file into a spectrum, profile it,
#         and trigger results.
#         '''
#         sound = load_sound.Sound(key, meta_data)
        # spectrum = spectral_analysis.Spectrum(sound)
        # prof_meta = fingerprinting.Fingerprinter(spectrum).profile
        # prof_final = sound_profiling.SoundProfiler(prof_meta).profile
        # alert = alerts.Alert(prof_final)


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
