'''Alerts module: Triggers a outbound alert to a 3rd party API when a
known sound has been detected.
'''

import requests
import json
import datetime

class Alert(object):
    '''Alert Class. Defines how the framework should respond to a given
    sound profile type and the end API to call.
    '''
    def __init__(self, profile):
        if self.validate(profile):
            self.profile = profile
            self.alert_status = self.push_alert()
        else:
            raise Exception("Profile passed to Alert module was not valid.")

    def validate(self, profile):
        '''check to be sure that the profile passed in has correct data.'''
        return True

    def push_alert(self):
        '''If profile passed in of KNOWN type, trigger alert to API with SQS, else do nothing.
        '''
        if self.profile.type == "known":
            service_key = "TEST ONLY - NO API CALL" # get account key from config file
            guardian_id = self.profile.guardian_id
            snd_class = self.profile.classification
            # TO DO: pull date/time from spectrum slice and sound start time
            date_time = str(datetime.datetime.now())
            incident_key = guardian_id +'-'+snd_class+'-'+ date_time
            # Send an alert event to the 3rd party API via JSON data
            url = 'http://localhost/:5000' #'https://events.pagerduty.com/generic/2010-04-15/create_event.json'
            payload = '''{
                "service_key": %s,
                "incident_key": %s,
                "event_type": "trigger",
                "description": "Detection of sound (%s) by guardian %s on %s",
                "client": "Rainforest Connection Monitoring Service",
                "client_url": "http://rfcx.org/",
                "details": { "ping time": "1500ms", "load avg": 0.75 }
                }''' % (service_key, incident_key, snd_class, guardian_id, date_time)
            req = requests.post(url, headers={'content-type': 'application/json'}, data=json.dumps(payload))
            return True
        else:
            # there is no explicit detection of sound. No alert is needed.
            return False
