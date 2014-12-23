import boto
from scipy.io import wavfile as wav


class Sound:
    """
    waveform container
    """
    def __init__(self, key):
      self.s3_key = key
      # validate key passed in
      if self.validate(self.s3_key):
        # grab sound file from s3 to local
        self.fp = download_file(self.s3_key)
        # read in the sound 
        self.read(self.fp)
      else:
        raise Exception("File path passed to Sound was not valid.")

    def validate(self, fp):
      # validate the JSON fp input received
      return True

    def read(self, fp):
        self.data, self.samplerate = read_sound(fp)
        self.duration = float(self.data.shape[0])/self.samplerate

    def write(self, fp):
        write_sound(fp, data, samplerate)

    def resample(self, samplerate):
        from scipy.signal import resample
        newsample = int(self.data.shape[0]*samplerate/self.samplerate)
        s = Sound()
        s.from_array(resample(self.data, newsample), samplerate)
        return s


def download_file(key):
  # download the file from s3 to local instance via boto
  fp = key # test only
  # return downloaded file's path
  return fp

def read_sound(fp):
    """
    create a normalized float array and datarate from any audo file
    """
    if fp.endswith('wav'):
        samplerate, data = wav.read(fp)
    else:
      raise Exception("Unsupported file type was used: %s" % fp[-4:])
    if len(data.shape)>1: data = data[:,0]
    data = data.astype('float64')
    data /= data.max()
    return data, samplerate
