'''Sound Fingerprinting Module. Holds all classes pertaining to audio
additional audio and spectrum analysis.
'''
from spectral_analysis import Bbox
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
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


class Profile(object):
    '''Profile Class. Holds all data needed to do an analysis of audio sample.'''
    def __init__(self, spectrum):
        self.classification = [] # could have many sounds per audio clip
        self.spectrum = spectrum
        self.guardian_id = spectrum.sound.meta_data.get('guardian_id')
        self.anomaly_prob = 0.0
        self.harmonic_power = None
        self.harmonic_intvl = None
        self.interest_areas = []

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
        #if self.harmonic_power is not None:
        #    return self.harmonic_power, self.harmonic_intvl
        pwrs = np.empty_like(self.spectrum.times)
        ints = np.empty_like(self.spectrum.times)
        for i,t in enumerate(self.spectrum.times):
            res = self.getPeaks(t, ct=10, interval_range=(5.,50.))
            pwrs[i] = res[2]
            ints[i] = res[3]
        self.harmonic_power = pwrs
        self.harmonic_intvl = ints
        return self.harmonic_power, self.harmonic_intvl

    def get_harmonic_sound_bounds(self):
        a = self.harmonic_power.astype(bool)
        k = np.ones(2*self.spectrum.samplerate, dtype=bool)
        r = np.convolve(a, k, 'same')
        stops = np.argwhere(np.logical_and(r[:-1], np.logical_not(r[1:]))).flatten()
        starts = np.argwhere(np.logical_and(np.logical_not(r[:-1]), r[1:])).flatten()
        if not starts.shape[0] or not stops.shape[0]:
            return []
        if stops[0]<starts[0]:
            stops=stops[1:]
        l = zip(self.spectrum.times[starts], self.spectrum.times[stops])
        l = [e for e in l if e[1]-e[0]>5.]
        self.interest_areas = l


    def getPeaks(self, t, ct=10, interval_range=(None, None)):
        '''
        find harmonic peaks in spectrum at given time
        t .. time value (seconds) to sample spectrum
        ct .. number of peaks to return
        interval_range .. hz
        returns list of freqencies where harmonic peaks are
        '''
        #if self.peaks is not None:
        #    return self.peaks

        s = self.spectrum
        a = self.spectrum.timeslice(t)

        dfreq = s.freqs[1]-s.freqs[0]
        guess_intvl = 100. #hz

        mn_freq = interval_range[0]
        mx_freq = interval_range[1]
        base = np.arange(ct)+1.

        interp_func = interp1d(s.freqs, a,
            kind='linear', bounds_error=False)

        def sample(freq_intvl):
            fqs = base*freq_intvl
            #f(fqs)
            return np.average(interp_func(fqs))

        def opt_func(x):
            return 1./sample(float(x))

        r = scipy.optimize.brute(opt_func,
            ranges=(slice(mn_freq,mx_freq,(mx_freq-mn_freq)/400.),)
        )

        freq_intvl = r[0]
        peak_freqs = base * freq_intvl

        peak_mags = sample(freq_intvl)
        bbox = Bbox(s, mn_freq, mx_freq)
        freq_ix_slice = bbox.ix()[0]

        overall_mag = np.average(a[freq_ix_slice])
        peaks_mag = np.average(peak_mags)

        # update profile values
        peak_mags = np.average(peak_mags)
        harmonic_power = peak_mags/overall_mag
        overall_mag = overall_mag
        peaks = peak_freqs

        if not interval_range[0]<freq_intvl<interval_range[1]:
            freq_intvl = 0.
            harmonic_power = 0.

        return peaks, peak_mags, harmonic_power, freq_intvl

    def profile_plot(self, **kwargs):
        return profile_plot(self, **kwargs)

    def power_plot(self, **kwargs):
        return power_plot(self, **kwargs)


def profile_plot(self,
        start_freq=None, end_freq=None,
        start_time=None, end_time=None,
        t = None,
    ):
    """
    generate plot of all of or bbox of spectrogram
    self ... spectrogam object
    """
    spc = self.spectrum
    bbox = Bbox(spc, start_freq, end_freq, start_time, end_time)

    freq_slice, time_slice = bbox.ix()
    x2 = spc.db_arr[freq_slice, time_slice][::-1,::1]
    mn, mx = np.percentile(x2,[25,99.9])
    x3 = np.clip(x2,mn,mx)
    x3-= x3.min()
    x3/= x3.max()
    # build plot
    plt.clf()
    plt.imshow(
        x3,
        extent=[bbox.start_time, bbox.end_time, bbox.start_freq, bbox.end_freq],
        aspect='auto',
        cmap='gist_heat_r',
    )
    if start_time or end_time:
        plt.xlim(start_time, end_time)
    if hasattr(self, 'harmonic_intvl') and self.harmonic_intvl is not None:
        for i in range(10):
            plt.plot(spc.times, self.harmonic_intvl*(i+1), '.', color='g')
    if t:
        plt.axvline(t, color='r')
    plt.grid(b=True, which='major',linestyle='-', alpha=.5)
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    return plt.gcf()



def power_plot(self, t=None,
        start_time=None, end_time=None,
    ):
    """
    """
    spc = self.spectrum
    plt.cla()
    plt.clf()
    plt.plot(spc.times, self.harmonic_power, color='b')
    plt.ylabel('Power')
    plt.twinx()
    plt.plot(spc.times, self.harmonic_intvl, color='g')

    if start_time or end_time:
        plt.xlim(start_time, end_time)
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    if t:
        plt.axvline(t, color='r')
    return plt.gcf()
