'''
This module classifies sounds to categories such as
"chainsaw" or "car"
'''
import fingerprinting

class SoundClassifier(object):
    def __init__(self, logger):
        self.logger = logger

    '''Classifies sounds to categories'''
    def classify_interest_areas(self, profile):
        '''classifies sounds and sets
           the classification array of the profile
        '''
        # Todo: add actual classification + use array instead of a
        # string (allows for multiple detection)
        profile.alerts = []
        interest_areas = profile.classification
        if interest_areas != []:
            for iarea in interest_areas:
                for known_sound in ["chainsaw","car","bird"]:
                    # TO DO: Change placeholder code to compare proper aspects of sound's profile
                    if profile.peaks != None:
                        profile.alerts.append(known_sound)
                    else:
                        profile.alerts.append("unknown")
                self.logger.info("""Classifed interest areas as: %s""" % (profile.alerts))
        return profile
