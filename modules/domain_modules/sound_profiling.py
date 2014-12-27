'''Sounds Profiling Module. Holds all classes pertaining to audio
classification and analysis.
'''

class SoundProfiler(object):
    '''Sound Profiler Class.'''
    def __init__(self, profile):
        # validate the profile data passed in
        if self.validate(profile):
            self.profile = profile
            # profile data against known sounds
            self.analyze(self.profile)
            # pass final profile results on to the Alert module

        else:
            raise Exception("Profile passed to SoundProfiler was not valid.")

    def validate(self, profile):
        '''validate the profile input received'''
        return True

    def analyze(self):
        '''determine if the given profile falls within known sound profiles'''
        if self.profile.classification in ["chainsaw","vehicle"]:
            self.profile.type = "known"
