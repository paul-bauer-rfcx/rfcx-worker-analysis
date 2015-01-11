'''Alerts module: Triggers a outbound alert to a 3rd party API when a
known sound has been detected.
'''

import requests
import json
import datetime
import os


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
        api_url = os.environ["ALERT_API_HOST"]+"/v1/guardians/"+guardian_id+"/alerts"
        payload = {"data" : str({   "service_key": service_key,
                                    "incident_key": incident_key,
                                    "event_type": "trigger",
                                    "description": "Detection of sound ("+sound+") by guardian "+guardian_id+" on "+date_time,
                                    "client": "Rainforest Connection Monitoring Service",
                                    "client_url": "http://rfcx.org/",
                                    "details": "{\"ping time\": \"1500ms\",\"load avg\": \"0.75\"}"
                                })
                    }
        try:
            api_req = requests.post(api_url, files=payload)
        except ConnectionError:
            # dev connection to server will not exist (111 response)
            print "Fake alert: in dev mode."
