'''Module of classes and function for the extraction of and analysis
of an audio sample into a spectrum and any related data.
'''

import numpy as np
import scipy.signal
import os
import scipy.io.wavfile as wav
import subprocess
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
        self.duration = sound.duration
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


def spc_plot(self, start_freq=None, end_freq=None, start_time=None, end_time=None):
    """
    generate plot of all of or bbox of spectrogram
    self ... spectrogam object
    """
    from matplotlib.ticker import FuncFormatter
    bbox = Bbox(self, start_freq, end_freq, start_time, end_time)
    freq_slice, time_slice = bbox.ix()

    x2 = self.db_arr[freq_slice, time_slice]

    plt.clf()

    def freq_fmt(x, pos):
        #print x, pos, self.freqs[x]
        return str(self.freqs[x])
    def time_fmt(x, pos):
        print x, pos
        return str(self.times[x])
    yformatter = FuncFormatter(freq_fmt)
    xformatter = FuncFormatter(time_fmt)
    #plt.gca().yaxis.set_major_formatter(yformatter)
    #plt.gca().xaxis.set_major_formatter(xformatter)

    #plt.plot(self.times, self.freqs)
    plt.imshow(
        np.clip(x2,0,None),
        extent=[bbox.start_time, bbox.end_time, bbox.start_freq, bbox.end_freq],
        aspect='auto',
        cmap='gist_heat_r',
    )
    plt.grid(b=True, which='major',linestyle='-', alpha=.5)
    #plt.rcParams['image.aspect'] = float(x2.shape[0])/x2.shape[1]
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    return plt.gcf()
    #print x.max()
    #show(x[:1000,:], bound=True, clip=.999)



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


def write_sound(fp, data, samplerate):
    """
    create audio file from array and datarate
    guess encoding based on filename extension
    """
    if fp.endswith('mp3'):
        tempname = 'temp.wav'
        wav.write(tempname, samplerate, data)
        #lame -q0 -b128 sample.wav  sample.mp3
        result = subprocess.call(['lame', '-q0', '-b128', tempname, fp])
        assert(result is 0)
    if fp.endswith('wav'):
        wav.write(fp, samplerate, data)
