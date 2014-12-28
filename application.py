# web server modules
from flask import flask, request
# import gevent
# import requests
# import json

# import RFCx custom modules via service layer
# from modules import service_layer

# setup web app instance
application = Flask(__name__)

# Set to enable tracebacks on Beanstalk log output
application.debug = True

@application.route('/analyzeSound')
def hello_world():
    return "Hello, world!"

#routes to call the correct request handlers
# @application.route('/analyzeSound', methods=['POST'])
# def analyze_sound():
#     # parse JSON received from SQS
#     data = request.get_json()
#     key = str(data["guardianAudio"]["uri:"])
#     # SL call to analyze the audio linked to given key value
#     gevent.joinall([
#         gevent.spawn(service_layer.AnalyzeSound(key, data))
#     ])
#     return """Background worker thread started!"""

# @application.route('/updateSoundProfile', methods=['POST'])
# def update_sound_profile():
#     # parse JSON received to get filename/key
#     data = request.get_json()
#     # SL call to analyze the audio linked to given key value
#     gevent.joinall([gevent.spawn()])
#     return "Update the sounds from ML."

if __name__ == "__main__":
    application.run(host='0.0.0.0')
