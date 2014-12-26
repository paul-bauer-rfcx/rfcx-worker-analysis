'''Alerts module: Triggers a outbound alert to a 3rd party API when a
known sound has been detected.
'''

from random import randint
import json

class Alert(object):
    '''Alert Class. Defines how the framework should respond to a given
    sound profile type and the end API to call.
    '''
    def __init__(self, profile, spectrum):
        if self.validate(profile):
            self.alert_status = self.push_alert(profile, spectrum)
        else:
            raise Exception("Profile passed to Alert module was not valid.")

    def validate(self, profile):
        '''check to be sure that the profile passed in has correct data.'''
        return True

    def push_alert(self, profile, spectrum):
        '''if profile passed in of KNOWN type, trigger alert to API with SQS, else do nothing.
        '''
        if profile.type == "Known":
            ''' make new SQS item to push alert event to 3rd party API'''
            # testing alert output after worker thread starts and HTTP closes by writing out to local file
            f = open('./tmp_alerts/file_'+str(randint(1,10000))+'.txt', 'w')
            f.write("Alert was triggered! Rejoice! :)\n\n")
            f.write("Spectrum object address(uniqueness):\n")
            f.write(str(spectrum))
            f.close()
            return True
        else:
            # there is no explicit detection of sound. No alert is needed.
            return False
