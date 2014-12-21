import sys
import boto

class DownloadAudio:
  def __init__(self, key):
    # validate key passed in
    if self.validate(key):
      # download audio file
      self.grab_file(key)
    else:
      raise ValueError

  def validate(self, key):
    # validate the JSON input received
    return True

  def grab_file(self, key):
    file_path = "./assets/test.wav"
    return file_path
