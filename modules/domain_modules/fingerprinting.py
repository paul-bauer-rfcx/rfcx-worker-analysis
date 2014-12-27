'''Sound Fingerprinting Module. Holds all classes pertaining to audio
additional audio and spectrum analysis.
'''

class Fingerprinter(object):
    '''Sound Profiler Class.'''
    def __init__(self, spectrum):
        # validate the spectrum data passed in
        if self.validate(spectrum):
            self.profile = Profile(spectrum)
            # fingerprint the new profile and return profile object to Alert module
            self.analyze(self.profile)
        else:
            raise Exception("Spectrum passed to Fingerprinter module was not valid.")

    def validate(self, spectrum):
        '''validate the spectrum input received'''
        return True

    def analyze(self, profile):
        '''Adds new meta information to the growing audio profile to aid in downstream
        sound classification
        '''
        profile.type = "chainsaw"


class Profile(object):
    ''''Profile Class. Holds all data needed to do an analysis of audio sample.'''
    def __init__(self, spectrum):
        # test properties
        self.type = "unknown"
        self.classification = "unknown"
        self.spectrum = spectrum
