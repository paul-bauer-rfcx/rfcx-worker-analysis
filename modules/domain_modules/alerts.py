'''Alerts module: Triggers a outbound alert to a 3rd party API when a
known sound has been detected.
'''

import requests
import json
import datetime


def push_alerts(profile):
    '''If Profile passed in has sound(s) of a KNOWN type,
    trigger alert to both 3rd party and RFCx internal API.
    '''
    for sound in set(profile.classification):
        service_key = "TEST ONLY - NO API CALL" # get account key from config file
        guardian_id = profile.guardian_id
        snd_class = profile.classification
        # TO DO: pull date/time from spectrum slice and sound start time
        date_time = str(datetime.datetime.now())
        incident_key = guardian_id +'-'+str(snd_class)+'-'+ date_time
        api_url = 'http://localhost:/5000:' # Send an alert event to API via JSON data
        payload = '''{
                    "service_key": %s,
                    "incident_key": %s,
                    "event_type": "trigger",
                    "description": "Detection of sound (%s) by guardian %s on %s",
                    "client": "Rainforest Connection Monitoring Service",
                    "client_url": "http://rfcx.org/",
                    "details": { "ping time": "1500ms", "load avg": 0.75 }
                }''' % (service_key, incident_key, snd_class, guardian_id, date_time)
        api_req = requests.post(api_url, headers={'content-type': 'application/json'}, data=json.dumps(payload))
