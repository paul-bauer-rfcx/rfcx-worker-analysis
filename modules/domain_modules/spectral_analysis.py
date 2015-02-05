'''Module of classes and function for the extraction of and analysis
of an audio sample into a spectrum and any related data.
'''

import numpy as np
import scipy.signal
import os
import scipy.io.wavfile as wav
import subprocess
from matplotlib import pyplot as plt
from load_sound import Sound

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
    silence = 0.0000001
    tooloud = 100000.
    def __init__(self, sound, framesz=.2, hop=.1):
        self.sound = sound
        self.framesz = framesz
        self.hop = hop
        self.duration = sound.duration
        self.complex_arr, self.samplerate, freqs = stft(
            sound.data, sound.samplerate, self.framesz, self.hop
        )
        self.freq_count = freqs.shape[0]/2
        self.freqs = freqs[:self.freq_count]
        self._calc()
        self.times = np.linspace(0., self.duration, self.complex_arr.shape[1])

    def _calc(self):
        
        self.abs_arr = np.absolute(self.complex_arr[:self.freq_count,:])
        self.abs_arr[0:2,:] = self.silence
        #self.abs_arr[-1,:] = self.silence
        np.clip(self.abs_arr, self.silence, self.tooloud, out=self.abs_arr)
        self.db_arr = 20.*np.log10(self.abs_arr)

    def isolate(self, start_freq=None, end_freq=None, start_time=None, end_time=None):
        bbox = Bbox(self, start_freq, end_freq, start_time, end_time)
        freq_slice, time_slice = bbox.ix()
        cpy = self.complex_arr[freq_slice, time_slice].copy()
        self.complex_arr[:,:] = self.silence * (1.0 + 1.0j)
        self.complex_arr[freq_slice, time_slice] = cpy
        self._calc()

    def to_sound(self):
        """
        return a sound object converted from this spectrum
        """
        data = istft(self.complex_arr, self.sound.samplerate, self.framesz, self.hop)
        s = Sound(data, self.sound.samplerate, self.sound.meta_data)
        return s

    def timeslice(self, time):
        """
        return 1D slice of the decibel array
        time .. slice location (s)
        """
        time_ix = np.argmin(np.abs(self.times-time))
        return self.abs_arr[:, time_ix]


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


def istft(X, fs, framesz, hop):
    """
    inverse stft
    """
    framesamp = int(framesz*fs)
    hopsamp = int(hop*fs)
    newsamps = X.shape[1]
    xlen = hopsamp*(newsamps-1)+framesamp
    x = scipy.zeros(xlen)
    w = scipy.hamming(framesamp)
    # TODO .. look into double hamming weighting vs alternate compensation for overlap
    for n,i in enumerate(range(0, xlen-framesamp, hopsamp)):
        x[i:i+framesamp] += np.real(np.fft.ifft(X[:,n]))*w
    return x


def read_sound(fp):
    """
    create a normalized float array and datarate from any audo file
    """
    if fp.endswith('mp3'):
        try:
            oname = 'temp.wav'
            #cmd = 'lame --decode "{0}" {1}'.format( fp ,oname )
            result = subprocess.call(['lame', '--decode', fp, oname])
            assert(result is 0)
            samplerate, data = wav.read(oname)
        except:
            print "couldn't run lame"
            try:
                import moviepy.editor as mpy
                aud_clip = mpy.AudioFileClip(fp)
                samplerate = aud_clip.fps
                data = aud_clip.to_soundarray()
            except:
                print "moviepy not installed?"
    if fp.endswith('aif'):
        #sf = aifc.open(fp)
        oname = fp
        sf = Sndfile(fp, 'r')
        sf.seek(0)
        data = sf.read_frames(sf.nframes)
        samplerate = sf.samplerate
    if fp.endswith('wav'):
        samplerate, data = wav.read(fp)

    if len(data.shape)>1: data = data[:,0]
    data = data.astype('float64')
    data /= data.max()
    return data, samplerate



