# web server modules
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.gen
import json
import boto
import sys

# import Tornado and AWS settings from file
import settings
from tornado.options import options

# import RFCx custom modules
from modules import feature_extraction # feature extraction with Welch
# from modules import sound_profiling # compare against known / anomaly sound profiles
# from modules import alert_ml # trigger alerts and save spectrum for ML

class MainPage(tornado.web.RequestHandler):
  def get(self):
    self.write("Home page! <br> TEST PLACEHOLDER ONLY!")

class FeatureExtraction(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  @tornado.gen.engine
  def post(self):
    # grab wav file from S3 location based on filename in JSON data pushed from SQS with Boto
    filename = json.loads(self.request.body)['filename']
    # conn = boto.connect_s3(options.AWS_KEY, options.AWS_SECRET)
    # bucket = conn.get_bucket(options.BUCKET_NAME)
    # key = bucket.get_key(filename)
    # wav_file = key.get_contents_to_filename('sound.wav')
    
    # process wav file with feature extraction module
    client = tornado.httpclient.AsyncHTTPClient()
    analyzer = feature_extraction.FeatureExtractor()
    response = yield tornado.gen.Task(client.fetch, analyzer.extract(filename))
    spectrum = response.effective_url

    # Only for testing spectrum object returned from call! REMOVE!
    self.write("""<h2>Finshed processing audio! Frequency spectrum has been created!</h2>
                  <ul>
                    <li>Length: %s </li>
                    <li>Size: %s </li>
                  </ul>
              """ % (len(spectrum), sys.getsizeof(spectrum)))
    self.finish()

class SoundProfiling(tornado.web.RequestHandler):
  # TO DO: pass spectrum data array to the Sound Profiler module
  @tornado.web.asynchronous
  @tornado.gen.engine
  def get(self):
    client = tornado.httpclient.AsyncHTTPClient()
    profiler = sound_profiler.SoundProfiler()
    response = yield tornado.gen.Task(client.fetch, profiler.extract(redis_key))
    profile = response.effective_url
    self.finsh()

class AlertML(tornado.web.RequestHandler):
  # TO DO:  1) Trigger 3rd party alert via API call
  #         2) Send sprectum data to ML DB for processing
  #         3) Final cleanup of sound file
  # Break up into sperate classes to handle ML pushing sound profiles back to analyzer? 
  @tornado.web.asynchronous
  @tornado.gen.engine
  def get(self):
    client = tornado.httpclient.AsyncHTTPClient()
    profiler = known_sounds_profiler.SoundProfiler()
    response = yield tornado.gen.Task(client.fetch, profiler.extract(redis_key))
    profile = response.effective_url
    self.finsh()

class AddKnownSoundProfile(tornado.web.RequestHandler):
  # TO DO: allow the ML framework a way to interact with sound profiling to update it as needed
  @tornado.web.asynchronous
  @tornado.gen.engine
  def get(self):
    client = tornado.httpclient.AsyncHTTPClient()
    profiler = known_sounds_profiler.SoundProfiler()
    response = yield tornado.gen.Task(client.fetch, profiler.extract(redis_key))
    profile = response.effective_url
    self.finsh()


# routes to call the correct handlers
app = tornado.web.Application([
  (r"/featureExtraction", FeatureExtraction),
  (r"/soundProfiling", SoundProfiling),
  (r"/alertML", AlertML),
  (r"/addKnownSoundProfile", AddKnownSoundProfile)
])


if __name__ == "__main__":
  port = 5000
  base = "http://localhost:" + str(port) + "/"
  app.listen(port)
  print "Web server started: " + base
  tornado.ioloop.IOLoop.instance().start()
  