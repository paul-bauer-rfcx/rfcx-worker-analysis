'''
This module classifies sounds to categories such as
"chainsaw" or "car"
'''
import fingerprinting

class SoundClassifier(object):
    def __init__(self, logger):
        self.logger = logger

    '''Classifies sounds to categories'''
    def classify(self, profile):
        '''classifies sounds and sets
           the classification array of the profile
        '''
        # Todo: add actual classification + use array instead of a
        # string (allows for multiple detection)
        for known_sound in ["chainsaw","car","bird"]:
            # TO DO: Change placeholder code to compare proper aspects of sound's profile
            if profile.peaks != None:
                profile.classification.append(known_sound)
            else:
                profile.classification.append("unknown")
        self.logger.info("""Classifed file as having sound(s): %s""" % (profile.classification))
        return profile
