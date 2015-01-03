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
        self.data = data
        self.samplerate = samplerate
        self.duration = float(self.data.shape[0])/self.samplerate
        self.guardian_id = meta_data["guardian_id"]
        self.file_id = meta_data["audio_id"]
        self.start_time = meta_data["start_time"]
        self.duration_ms = meta_data["duration_ms"]
        self.latitude = meta_data["latitude"]
        self.longitude = meta_data["longitude"]
        self.ambient_temp = meta_data["ambient_temp"]

    def read(self, fp):
        ''''''
        self.data, self.samplerate = read_sound(fp)
        self.duration = float(self.data.shape[0])/self.samplerate

    def write(self, fp):
        ''''''
        write_sound(fp, data, samplerate)

    def resample(self, samplerate):
        ''''''
        newsample = int(self.data.shape[0]*samplerate/self.samplerate)
        s = Sound()
        s.from_array(resample(self.data, newsample), samplerate)
        return s

def read_sound(fp):
    """
    create a normalized float array and datarate from any audo file
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
        return data, samplerate
