'''Sounds Profiling Module. Holds all classes pertaining to audio
classification and analysis.
'''

class SoundProfiler(object):
    '''Sound Profiler Class.'''
    def __init__(self, spectrum):
        # validate the spectrum data passed in
        if self.validate(spectrum):
            # profile the spectrum data and return profile object to Alert module
            self.profile = self.analyze(spectrum)
        else:
            raise Exception("Spectrum passed to Profiler module was not valid.")

    def validate(self, spectrum):
        '''validate the spectrum input received'''
        return True

    def analyze(self, spectrum):
        '''determine if a given spectrum falls within know sound profiles'''
        return Profile()


class Profile(object):
    ''''Profile Class. Holds all data needed to do an analysis of audio sample.'''
    def __init__(self):
        # test properties
        self.type = "Known"
        self.classification = "Chainsaw"
