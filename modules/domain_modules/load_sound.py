''' Load Sound module: classes and function to validate and set up a
sound object with the audio and meta data passed in from a device.
'''

import os
import random
import requests
import subprocess
import numpy as np
from scipy.io           import wavfile as wav
from scipy              import signal
from scipy.interpolate  import interp1d


class Sound(object):
    """
    waveform container
    """
    def __init__(self, data, samplerate, meta_data):
        """
        create a new sound
        data .. 1-D numpy array
        samplerate .. numper of elements in 'data' that represents one second
        meta_data .. dict of associated data
        """
        self.data = data
        self.samplerate = samplerate
        self.duration = float(self.data.shape[0])/self.samplerate
        self.meta_data = meta_data

    def resample(self, newsamplerate):
        """create a new sound object by resampling this one
        newsamplerate .. sample rate for new sound
        """
        if self.samplerate == newsamplerate:
            return self
        shape = self.data.shape[0]
        newshape = int(shape*newsamplerate/self.samplerate)

        x = np.linspace(0, self.duration, shape)
        y = self.data

        f = interp1d(x, y, kind='linear')

        newx = np.linspace(0., self.duration, newshape)

        w = signal.get_window(4.0, 9)
        #newdata = resample(self.data, newshape, window=w)
        newdata = f(newx)
        return Sound(newdata, newsamplerate, self.meta_data)

    def crop(self, starttime, endtime):
        """
        create a new sound from a section of this sound
        """
        if starttime is None: starttime=0.
        if endtime is None: endtime = self.duration
        sr = self.samplerate
        start_ix = int(sr*starttime)
        end_ix =  int(sr*endtime)
        newdata = self.data[start_ix:end_ix]
        return Sound(newdata, self.samplerate, self.meta_data)

def read_sound(fp, meta_data):
    """
    create a Sound object from audio file
    """
    samplerate, data = wav.read(fp)
    if len(data.shape)>1:
        data = data[:, 0]
    data = data.astype('float64')
    data /= 32768.  #data.max()
    s = Sound(data, samplerate, meta_data)
    s.fp = fp
    return s


def write_sound(fp, sound):
    """
    create audio file from sound object
    guess encoding based on filename extension
    """
    if fp.endswith('mp3'):
        tempname = 'temp.wav'
        wav.write(tempname, sound.samplerate, sound.data)
        #lame -q0 -b128 sample.wav  sample.mp3
        result = subprocess.call(['lame', '-q0', '-b128', tempname, fp])
        assert(result is 0)
    if fp.endswith('wav'):
        wav.write(fp, sound.samplerate, sound.data)
