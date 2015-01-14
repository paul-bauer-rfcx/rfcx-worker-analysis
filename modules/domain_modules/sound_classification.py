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
        interest_areas = profile.interest_areas
        if interest_areas != None:
            for iarea in interest_areas:
                profile.alerts.append("automobile")
                # profile.alerts.append("unknown")
                self.logger.info("""Classifed interest areas as: %s""" % ("automobile")
        return profile
