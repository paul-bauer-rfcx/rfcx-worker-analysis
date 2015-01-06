'''Sound Fingerprinting Module. Holds all classes pertaining to audio
additional audio and spectrum analysis.
'''

import numpy as np
import scipy

class Fingerprinter(object):
    '''Sound Profiler Class.'''
    def __init__(self, spectrum):
        # validate the spectrum data passed in
        if self.validate(spectrum):
            self.profile = Profile(spectrum)
        else:
            self.logger.error("""Spectrum passed to Fingerprinter module was not valid: %s\n %s""" % (audio_id, e))
            exit(1)

    def validate(self, spectrum):
        '''validate the spectrum input received'''
        return True


# Todo: refactor - seperation of concerns
class Profile(object):
    '''Profile Class. Holds all data needed to do an analysis of audio sample.'''
    def __init__(self, spectrum):
        self.classification = [] # could have many sounds per audio clip
        self.spectrum = spectrum
        #self.peaks = None
        self.guardian_id = spectrum.sound.meta_data.get('guardian_id')
        self.anomaly_prob = 0.0
        self.harmonic_power = None

    def getPeaks2(self, t):
        ''' get peaks based on relative height (ignore harmonics)
        '''
        a = self.spectrum.timeslice(t)
        ix = np.r_[True, a[1:] > a[:-1]] & np.r_[a[:-1] > a[1:], True]
        ix[:] = (a>np.percentile(a,95)) & ix
        return self.spectrum.freqs[ix]

    def get_harmonic_power(self):
        """
        return a 1D array of strength of harmonic peaks for each time
        in spectrum.times
        """
        if self.harmonic_power is not None:
            return self.harmonic_power
        pwrs = np.empty_like(self.spectrum.times)
        for i,t in enumerate(self.spectrum.times):
            pwrs[i] = self.getPeaks(t)[2]
        self.harmonic_power = pwrs
        return pwrs

    def getPeaks(self, t, ct=10):
        '''
        find harmonic peaks in spectrum at given time
        t .. time value (seconds) to sample spectrum
        ct .. number of peaks to return
        returns list of freqencies where harmonic peaks are
        '''
        #if self.peaks is not None:
        #    return self.peaks

        s = self.spectrum
        a = self.spectrum.timeslice(t)
        dfreq = s.freqs[1]-s.freqs[0]
        intvl = 100.
        mn = 0.1*intvl/dfreq
        mx = 2.0*intvl/dfreq

        base = np.arange(ct)+1
        def f(x):
            ix = base*x[0]
            return 1.0/np.sum(a[ix.astype(int)])
        r = scipy.optimize.brute(f,
            ranges=(slice(mn,mx,(mx-mn)/100.), slice(0,1,1))
        )
        intvl = r[0]
        ix = (base*intvl).astype(int)
        peak_freqs = s.freqs[ix]
        peak_mags = (a[ix]*2+a[ix-1]+a[ix+1])/4.

        overall_mag = np.average(a)
        peaks_mag = np.average(peak_mags)
        #20.*np.log10(np.average(10**(peak_mags/20.)))

        harmonic_power = peaks_mag/overall_mag
        self.peaks = peak_freqs

        return self.peaks, peak_mags, harmonic_power
