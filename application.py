# web server modules
from flask import Flask, request
from os import mkdir
import sys
import gevent
import json

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
    # parse JSON received from SQS
    data = json.loads(json.loads(request.data)["Message"])
    key = str(data["guardianAudio"]["uri:"])
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
