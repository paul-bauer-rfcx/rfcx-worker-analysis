'''Sound Fingerprinting Module. Holds all classes pertaining to audio
additional audio and spectrum analysis.
'''

class Fingerprinter(object):
    '''Sound Profiler Class.'''
    def __init__(self, sound):
        # validate the spectrum data passed in
        if self.validate(sound):
            self.profile = Profile(sound)
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
        profile.classification = "chainsaw"


# Todo: refactor - seperation of concerns
class Profile(object):
    ''''Profile Class. Holds all data needed to do an analysis of audio sample.'''
    def __init__(self, sound):
        # test properties
        self.type = "unknown"
        self.classification = "unknown"
        self.spectrum = sound.spectrum
        self.peaks = None  
        self.guardian_id = sound.guardian_id
        self.anomaly_prob = 0.0

    def getPeaks(self): 
        if self.peaks == None:
            # replace by Paul's peak finding method 
            self.peaks = [1, 2, 3]

        return self.peaks
