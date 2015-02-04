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

    def peaks_plot(self, **kwargs):
        return peaks_plot(self, **kwargs)

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
            plt.plot(spc.times, self.harmonic_intvl*(i+1), '.', color='g', alpha=.5)
    if t:
        plt.axvline(t, color='b')
    plt.grid(b=True, which='major',linestyle='-', alpha=.5)
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    return plt.gcf()



def power_plot(self, t=None,
        start_time=None, end_time=None,
        start_freq=None, end_freq=None,
    ):
    """
    """
    spc = self.spectrum
    plt.cla()
    plt.clf()
    plt.plot(spc.times, self.harmonic_power, color='r')
    plt.ylabel('Power')
    plt.twinx()
    plt.plot(spc.times, self.harmonic_intvl, color='g')

    if start_time or end_time:
        plt.xlim(start_time, end_time)
    if start_freq or end_freq:
        plt.ylim(start_freq, end_freq)
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    if t:
        plt.axvline(t, color='b')
    return plt.gcf()

def peaks_plot(self, t=0., 
    start_time=None, end_time=None,
    start_freq=None, end_freq=None, ):
    """max_freq"""
    import matplotlib.gridspec as gridspec
    offset = int(t*self.spectrum.samplerate)
    bbox = Bbox(self.spectrum, start_freq, end_freq, start_time, end_time)
    freq_slice, time_slice = bbox.ix()
    db_arr = self.spectrum.db_arr
    db_arr2 = np.zeros((db_arr.shape[0],db_arr.shape[1]+20),dtype=float)
    db_arr2[:,:] = np.average(db_arr)
    db_arr2[:,10:-10] = db_arr
    #i = np.argmin(np.abs(self.spectrum.freqs-end_freq))
    db_band = db_arr2[freq_slice, offset:offset+20]
    mn, mx = np.percentile(db_band,[25,99.9])
    db_band = np.clip(db_band,mn,mx)
    #print db_band.shape
    db_slice = db_arr[freq_slice, offset]
    #x0p = np.abs(np.average(x0, axis=1))
    #a = peak_find(x0p)
    harmonics = (np.arange(10)+1.)*self.harmonic_intvl[offset]
    plt.clf()
    #fig = plt.gcf()
    gs = gridspec.GridSpec(2, 1, height_ratios=[1,8], hspace=.1)
    ax2 = plt.subplot(gs[1])
    ax1 = plt.subplot(gs[0], sharex=ax2)
    ax2.set_ylabel('Signal (dB)')
    ax2.set_xlabel('Frequency (Hz)')
    #ax1.set_aspect(.1)
    #print ax1.get_aspect()
    '''
    ax1.imshow(db_band.T,
        extent=[0, 150, bbox.start_freq, bbox.end_freq],
        aspect='.1',
        cmap='gist_heat_r',
    )'''
    Z = db_band.T
    X,Y = np.meshgrid(np.linspace(0.,end_freq,Z.shape[1]), np.linspace(-1.,1.,Z.shape[0]))
    ax1.pcolor(X,Y,Z, cmap='gist_heat_r')
    ax1.axhline(0, color='b')
    #ax1.set_xticklabels([])
    ax1.set_yticklabels([])
    #print self.spectrum.freqs[freq_slice], db_slice
    ax2.plot(self.spectrum.freqs[freq_slice], db_slice )
    interp_fn = interp1d(self.spectrum.freqs[freq_slice], db_slice,
            kind='linear', bounds_error=False)
    values = interp_fn(harmonics)
    ax2.plot(harmonics, values, 'o', color='g', alpha=.5)
    ax2.set_ylim(-75, db_arr.max())
    ax2.set_xlim(0, end_freq)
    #fig.canvas.draw()
    #labels = [fmt(item.get_text()) for item in plt.gca().get_xticklabels()]
    #ax2.set_xticklabels(labels)
    
    return plt.gcf() 



def make_video(profile, name='test', bbox=None, plot_type='profile_plot'):
    """
    plot_type .. 'power_plot', 'profile_plot', 'peaks_plot'
    """
    import moviepy.editor as mpy
    from moviepy.video.io.bindings import mplfig_to_npimage
    sound = profile.spectrum.sound
    sound_array = sound.data/(2*np.abs(sound.data).max())
    def video_fn(t):
        fn = getattr(profile, plot_type)
        fig = fn(end_freq=500, t=t)
        return mplfig_to_npimage(fig)
    def audio_fn(t):
        if type(t) is int:
            i = t*sound.samplerate
        elif type(t) is float:
            i = int(t*sound.samplerate)
        else:
            i = (t*sound.samplerate).astype(int)
        return sound_array[i]
    
    #fp = sound.fp
    video_clip = mpy.VideoClip(video_fn, duration=sound.duration)
    audio_clip = mpy.AudioClip(audio_fn, duration=sound.duration)

    animation = video_clip.set_audio(audio_clip)  #.set_duration(duration)
    #animation.fps = 20
    animation.to_videofile(name+'_'+plot_type+'.avi', codec='libx264', fps=24)  
    #, codec='mpeg4'
