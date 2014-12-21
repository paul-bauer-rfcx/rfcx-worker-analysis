class Profiler:
  def __init__(self, spectrum):
    self.detected = Profile()
    # validate the spectrum data passed in
    if self.validate(spectrum):
      # profile the spectrum data and return profile object to Alert module
      self.analyze(spectrum)
    else:
      raise ValueError

  def validate(self, spectrum):
    # validate the spectrum input received
    return True

  def analyze(self, spectrum):
    # determine if a given spectrum falls within know sound profiles
    return self.detected


class Profile:
  def __init__(self):
    pass
