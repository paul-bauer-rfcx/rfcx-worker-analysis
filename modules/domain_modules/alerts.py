'''Alerts module: Triggers a outbound alert to a 3rd party API when a
known sound has been detected.
'''

import requests
import json
import datetime
import os


class AlertSender(object):
    # basic dependency injection
    def __init__(self, logger, profile):
        self.logger = logger
        self.profile = profile

    def push_alerts(self):
        '''If alerts array passed in has sound(s) of a KNOWN type,
        trigger alert to both 3rd party and RFCx internal API.
        '''
        if self.profile.alerts != []:
            for sound in set(self.profile.classification):
                service_key = "TEST ONLY - NO API CALL" # get account key from config file
                guardian_id = self.profile.guardian_id
                snd_class = self.profile.classification
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
                api_req = requests.post(api_url, files=payload)
        else:
            self.logger.info("""No alerts to send for file: %s""" % (self.profile.spectrum.sound.meta_data['audio_id']))
