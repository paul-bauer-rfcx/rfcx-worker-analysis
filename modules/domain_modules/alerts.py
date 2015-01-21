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
        guardian_id = self.profile.guardian_id
        date_time = str(datetime.datetime.now())
        audio_id = self.profile.spectrum.sound.meta_data['audio_id']
        if self.profile.interest_areas != []:
            for event in self.profile.interest_areas:
                service_key = "TEST ONLY - NO API CALL" # get account key from config file
                snd_class = "automobile" # placeholder classification! Remove!
                # TO DO: pull date/time from spectrum slice and sound start time
                incident_key = guardian_id +'-'+str(snd_class)+'-'+ date_time
                api_alert_url = os.environ["ALERT_API_HOST"]+"/v1/guardians/"+guardian_id+"/alerts"
                payload = {"data" : str({   "service_key": service_key,
                                            "incident_key": incident_key,
                                            "event_type": "trigger",
                                            "description": "Detection of sound ("+audio_id+") by guardian "+guardian_id+" on "+date_time,
                                            "client": "Rainforest Connection Monitoring Service",
                                            "client_url": "http://rfcx.org/",
                                            "details": "{\"ping time\": \"1500ms\",\"load avg\": \"0.75\"}"
                                        })
                            }
                api_alert_req = requests.post(api_alert_url, files=payload)
        else:
            self.logger.info("""No alerts to send for file: %s""" % (self.profile.spectrum.sound.meta_data['audio_id']))

        # check in with API to signal completion of processing for a given audio file
        checkin_id = self.profile.spectrum.sound.meta_data['checkin_id']
        
        api_completion_url = os.environ["ALERT_API_HOST"]+"/v1/guardians/"+guardian_id+"/checkins/"+checkin_id+"/audio/"+audio_id
        payload = { "alerts": str(self.profile.interest_areas),
                    "analysis_complete" : date_time
                }
        api_alert_req = requests.post(api_completion_url, files=payload)
