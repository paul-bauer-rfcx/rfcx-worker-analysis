# web server modules
from flask import Flask, request
from os import mkdir
import sys
import gevent
import json
import base64

# import RFCx custom modules via service layer
# from modules import service_layer

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
        decoded = request.get_data() # parse JSON received from SQS
    except (TypeError, ValueError), e:
        # TO DO: add logging and logic for JSON decoding failures
        # error_log.exception('Failed to decode JSON from SQS')
        raise Exception('''***** Failed to decode JSON from SQS *****\n%s'''%(e))
    json_data = json.loads(json.loads(decoded)["Message"])
    key = str(json_data["guardianAudio"]["uri:"])
    # SL call to analyze the audio linked to given key value
    # gevent.joinall([
    #     gevent.spawn(service_layer.AnalyzeSound(key, data))
    # ])
    return """Background worker thread started!"""


@application.route('/updateSoundProfile', methods=['POST'])
def update_sound_profile():
    # parse JSON received to get filename/key
    data = json.loads(json.loads(request.data)["Message"])["guardianAudio"]["uri:"]
    # SL call to analyze the audio linked to given key value
    # gevent.joinall([
    #     gevent.spawn(service_layer.UpdateSoundProfile(True, True))
    # ])
    test = service_layer.UpdateSoundProfile(True, True)
    return """Update the sounds from ML. %s""" % str(data)

def main(argv):
    try:
        mkdir('./tmp')
    except:
        pass
    finally:
        application.run(host='0.0.0.0')


if __name__ == "__main__":
    main(sys.argv[1:])
