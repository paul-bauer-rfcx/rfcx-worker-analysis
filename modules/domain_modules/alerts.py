class Alert:
  def __init__(self, profile):
    if self.validate(profile):
      self.alert_status = self.push_alert(profile)
    else:
        raise Exception("Profile passed to Alert module was not valid.")
      
  def validate(self, profile):
    # check to be sure that the profile passed in has correct data.
    return True

  def push_alert(self, profile):
    # if profile passed in of KNOWN type, trigger alert to API with SQS, else do nothing.
    if profile.type == "Known":
      # make new SQS item to push alert event to 3rd party API
      # testing alert output after worker thread starts and HTTP closes by writing out to local file
      f = open('./alert_file.txt', 'w')
      f.write("Alert was triggered successfully! Rejoice! :)\n")
      f.close()
      return True
    else:
      # there is no explicit detection of sound. No alert is needed.
      return False
