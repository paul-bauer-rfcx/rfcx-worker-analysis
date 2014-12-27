''' Load Sound module: classes and function to validate and set up a
sound object with the audio and meta data passed in from a device.
'''

import requests
from scipy.io import wavfile as wav
from scipy.signal import resample

class Sound(object):
    """
    waveform container
    """
    def __init__(self, key, meta_data):
        self.s3_key = key
        # validate JSON meta data passed in
        if self.validate(meta_data):
            # grab sound file from s3 to local
            self.fp = download_file(self.s3_key)
            # read in the sound
            self.read(self.fp)

    def validate(self, meta_data):
        '''validate the JSON input received by populating meta data for object'''
        try:
            self.start_time = str(meta_data['guardianAudio']['checkIn']['createdAt'])
            self.duration_ms = int(meta_data['guardianAudio']['lengthMilliseconds'])
            self.latitude = str(meta_data['guardianAudio']['checkIn']['guardian']['latitude'])
            self.longitude = str(meta_data['guardianAudio']['checkIn']['guardian']['longitude'])
            self.ambientTemp = int(meta_data['guardianAudio']['checkIn']['ambientTemperature'])
            self.guardian_id = str(meta_data['guardianAudio']['checkIn']['guardian']['id'])
        except:
            # raise an exception if any of the meta data is missing or the wrong format.
            raise Exception("JSON meta data is not the ocrrect format! File/url:%s"%self.s3_key)
        else:
            return True

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

    def from_array(self, data, samplerate):
        self.data = data
        self.samplerate = samplerate
        self.duration = float(self.data.shape[0])/self.samplerate

def download_file(key):
    '''download the file from s3 to local instance via boto
    '''
    fp = key # test only
    # return downloaded file's path
    # fp = requests.get(key)
    return fp

def read_sound(fp):
    """
    create a normalized float array and datarate from any audo file
    """
    if fp.endswith('wav'):
        samplerate, data = wav.read(fp)
    else:
        raise Exception("Unsupported file type was used: %s" % fp[-4:])
    if len(data.shape)>1:
        data = data[:, 0]
    data = data.astype('float64')
    data /= data.max()
    return data, samplerate
