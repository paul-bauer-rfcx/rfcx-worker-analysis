class Alert:
  def __init__(self, profile):
    if self.validate(profile):
      #
      self.push_alert(profile)
    else:
        raise ValueError
      
  def validate(profile):
    # check to be sure that the profile passed in has correct data.
    return True

  def push_alert():
    # if profile passed in of KNOWN type, trigger alert to API with SQS, else do nothing.
    if profile.type == "Known":
      # make new SQS item to push alert event to 3rd party API
      return True
    else:
      # there is no explicit detection of sound. No alert is needed.
      return False
