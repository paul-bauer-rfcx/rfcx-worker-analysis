# extraction and analysis module
import scipy
import numpy as np
from scipy.signal import ricker
import subprocess
import scipy, pylab
from matplotlib import pyplot as plt

class Bbox(object):
    """
    object representing a 2D time-freq "slice" of a spectrogram
    spec .. spectrum object
    """
    def __init__(self, spec, start_freq=None, end_freq=None, start_time=None, end_time=None):
        self.start_freq = start_freq if start_freq is not None else 0.
        self.end_freq = end_freq if end_freq is not None else spec.freqs.max() 
        self.start_time = start_time if start_time is not None else 0.
        self.end_time = end_time if end_time is not None else spec.duration
        self.spec = spec
    def ix(self):
        spec = self.spec
        start_freq_ix = np.argmin(np.abs(spec.freqs-self.start_freq))
        end_freq_ix = np.argmin(np.abs(spec.freqs-self.end_freq))
        start_time_ix = np.argmin(np.abs(spec.times-self.start_time))
        end_time_ix =  np.argmin(np.abs(spec.times-self.end_time))       
        return slice(start_freq_ix, end_freq_ix), slice(start_time_ix, end_time_ix)

class Spectrum(object):
    """
    spectrogram of a sound
    sound .. Sound object
    """
    def __init__(self, sound, framesz=.2, hop=.1):
        self.sound = sound
        self.framesz = framesz
        self.hop = hop
        self.duration = sound.duration_ms
        self.complex_arr, self.samplerate, self.freqs = stft(
            sound.data, sound.samplerate, self.framesz, self.hop
        )
        self._calc()
        self.times = np.linspace(0., self.duration, self.complex_arr.shape[0])
    
    def _calc(self):
        self.db_arr = 20.*np.log10(np.absolute(self.complex_arr))
    
    def isolate(self, start_freq=None, end_freq=None, start_time=None, end_time=None):
        bbox = Bbox(self, start_freq, end_freq, start_time, end_time)
        freq_slice, time_slice = bbox.ix()
        cpy = self.complex_arr[freq_slice, time_slice].copy()
        self.complex_arr[:,:]=.000001+.000001j
        self.complex_arr[freq_slice, time_slice] = cpy
        self._calc()

    def plot(self, *args, **kwargs):
        return spc_plot(self, **kwargs)

    def to_sound(self):
        data = istft(self.complex_arr, self.sound.samplerate, self.framesz, self.hop)
        s = Sound()
        s.from_array(data, self.sound.samplerate)
        return s
    
def stft(x, fs, framesz, hop):
    """
    rolling/hopping hamming window FFT
    x       .. data - 1D numpy array
    fs      .. data rate in samples per sec
    framesz .. frame size in seconds
    hop     .. sampling resoltuion in seconds
    """
    framesamp = int(framesz*fs)
    hopsamp = int(hop*fs)
    xlen = len(x)
    newsamps = (xlen-framesamp)/hopsamp + 1
    #print framesamp, newsamps, xlen, hopsamp
    w = scipy.hamming(framesamp)  
    X = np.empty((framesamp, newsamps), dtype=complex)
    freqs = np.fft.fftfreq(framesamp) * fs
    for n, i in enumerate(range(0, xlen-framesamp, hopsamp)):
        X[:,n] = np.fft.fft(w*x[i:i+framesamp])
    return X, float(fs)*newsamps/xlen, freqs