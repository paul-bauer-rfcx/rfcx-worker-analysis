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
  # parse JSON received to get filename/key
  key = request.get_json()["filename"]
  gevent.joinall([
    # SL call to analyze the audio linked to given key value
    gevent.spawn(service_layer.AnalyzeSound(key))
  ])
  return """Worker thread started! :) Closing out the HTTP request!"""

@app.route('/updateSoundProfile', methods=['POST'])
def update_sound_profile():  
  return "Update the sounds from ML...?"

if __name__ == "__main__":
  app.run() 
  