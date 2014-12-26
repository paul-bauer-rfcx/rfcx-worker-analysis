# web server modules
from flask import Flask, request
import gevent #import monkey; monkey.patch_all()
import requests
import json

# import Flask and AWS settings from file
import settings
# import RFCx custom modules via service layer
from modules import service_layer

# setup web app instance
app = Flask(__name__)

# routes to call the correct request handlers
@app.route('/analyzeSound', methods=['POST'])
def analyze_sound():
    # parse JSON received from SQS
    data = request.get_json()
    key = str(data["guardianAudio"]["uri:"])
    # SL call to analyze the audio linked to given key value
    gevent.joinall([
        gevent.spawn(service_layer.AnalyzeSound(key, data))
    ])
    return """Background worker thread started!"""

@app.route('/updateSoundProfile', methods=['POST'])
def update_sound_profile():
    # parse JSON received to get filename/key
    data = request.get_json()
    # SL call to analyze the audio linked to given key value
    gevent.joinall([gevent.spawn()])
    return "Update the sounds from ML."

if __name__ == "__main__":
    app.run(debug=True)

