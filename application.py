# web server modules
from flask import Flask, request
from os import mkdir
import sys
import gevent
import json
import base64

# import RFCx custom modules via service layer
from modules import service_layer

# setup web app instance
application = Flask(__name__)

# Set to enable tracebacks on Beanstalk log output
application.debug = True

@application.route('/healthCheck')
def check_stuff():
    return "Server is running"

# routes to call the correct request handlers
@application.route('/analyzeSound', methods=['POST'])
def analyze_sound():
    try:
        decoded = request.get_data()
    except:
        try:
           decoded = base64.b64decode(request.get_data())
        except (TypeError, ValueError), e:
            # TO DO: add logging and logic for JSON decoding failures
            # error_log.exception('Failed to decode JSON from SQS')
            raise Exception('''***** Failed to decode JSON from SQS *****\n%s'''%(e))
    json_data = json.loads(json.loads(decoded)["Message"])

    # key = str(json_data["guardianAudio"]["uri:"])
    # mocking test data for processing while true json post meta-data is unavailable
    key = "https://rfcx-ark.s3-eu-west-1.amazonaws.com/development/guardians/fedcba/2014/12/23/fedcba-2014-12-23T14-24-49.wav?Expires=1419944732&AWSAccessKeyId=AKIAJ2EUNGZ4RMEMMWMA&Signature=NYkA8yA5QE%2FTbwHu9cVrB8eNr%2BI%3D"
    test_data = json.loads('{"guardianAudio": { "id": "60819a58-69e9-4253-87bf-eb462aa846b2", "uri:": "https://rfcx-ark.s3-eu-west-1.amazonaws.com/development/guardians/fedcba/2014/12/23/fedcba-2014-12-23T14-24-49.wav?Expires=1419944732&AWSAccessKeyId=AKIAJ2EUNGZ4RMEMMWMA&Signature=NYkA8yA5QE%2FTbwHu9cVrB8eNr%2BI%3D", "createdAt": "2014-12-23T13:46:42.311Z", "lengthMilliseconds": 150000, "checkIn": { "id": "806dfafk-ghss-3423-bdh3-dkvnkdoskndk", "createdAt": "2014-12-23T13:46:42.311Z", "ambientTemperature": 30, "guardian": { "id": "vhdsdfehfoks", "latitude": 3.6141375, "longitude": 14.2108033 }}}}')
    # SL call to analyze the audio linked to given key value
    # gevent.joinall([
    #     gevent.spawn(service_layer.AnalyzeSound(key, test_data))
    # ])
    return """Background worker thread started!""", 202 # 202-accepted but not completed


@application.route('/updateSoundProfile', methods=['POST'])
def update_sound_profile():
    # parse JSON received to get filename/key
    # data = json.loads(json.loads(request.data)["Message"])["guardianAudio"]["uri:"]
    # SL call to analyze the audio linked to given key value
    # gevent.joinall([
    #     gevent.spawn(service_layer.UpdateSoundProfile(True, True))
    # ])
    # test = service_layer.UpdateSoundProfile(True, True)
    return """Update the sounds from ML."""

def main(argv):
    try:
        mkdir('./tmp')
    except:
        pass
    finally:
        application.run(host='0.0.0.0')


if __name__ == "__main__":
    main(sys.argv[1:])
