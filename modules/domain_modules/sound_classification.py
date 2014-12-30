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
        profile.classification = "chainsaw"
        self.logger.info("classifed sound: %s", profile.classification)