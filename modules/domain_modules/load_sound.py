''' Load Sound module: classes and function to validate and set up a
sound object with the audio and meta data passed in from a device.
'''

import os
import random
import requests
from scipy.io import wavfile as wav
from scipy.signal import resample

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
        newshape = int(self.data.shape[0]*newsamplerate/self.samplerate)
        newdata = resample(self.data, newshape)
        return Sound(newdata, newsamplerate, self.meta_data)

    def crop(self, starttime, endtime):
        """
        create a new sound from a section of this sound
        """
        sr = self.samplerate
        start_ix = int(sr*starttime)
        end_ix =  int(sr*endtime)
        newdata = self.data[start_ix:end_ix]
        return Sound(newdata, self.samplerate, self.meta_data)

def read_sound(fp):
    """
    create a Sound object from audio file
    """
    try:
        samplerate, data = wav.read(fp)
    except Exception, e:
        self.logger.error("""Unsupported file type was used: %s\n %s""" % (audio_id, e))
        exit(1)
    else:
        if len(data.shape)>1:
            data = data[:, 0]
        data = data.astype('float64')
        data /= data.max()
        return Sound(data, samplerate, {})
