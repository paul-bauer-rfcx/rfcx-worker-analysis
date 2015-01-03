'''Module of classes and function for the extraction of and analysis
of an audio sample into a spectrum and any related data.
'''

import numpy as np
import scipy.signal


class SpectralAnalysis:
    def __init__(self, framesz=.2, hop=.1):
        self.hop = hop
        self.framesz = framesz

    def add_spectrum(self, sound):
        sound.spectrum = stft(sound.data, sound.samplerate, self.framesz, self.hop)


def stft(x, fs, framesz, hop):
    ''' Rolling/hopping hamming window FFT:
    x       .. data - 1D numpy array
    fs      .. data rate in samples per sec
    framesz .. frame size in seconds
    hop     .. sampling resoltuion in seconds
    '''
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
    return X
