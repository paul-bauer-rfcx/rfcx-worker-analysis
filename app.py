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
# from modules import known_recognition # compare against known sound profiles
# from modules import anomaly_detection # look for anomalies in sound profile
# from modules import alert_ml # trigger alerts and save spectrum for ML

class MainPage(tornado.web.RequestHandler):
  def get(self):
    self.write("Home page! <br> TEST PLACEHOLDER ONLY!")

class FeatureExtraction(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  @tornado.gen.engine
  def get(self):
    # grab wav file from S3 location based on filename in JSON data pushed from SQS with Boto
    conn = boto.connect_s3(options.AWS_KEY, options.AWS_SECRET)
    bucket = conn.get_bucket(options.BUCKET_NAME)
    filename = json.loads(self.request.body)['filename']
    key = bucket.get_key(filename)
    wav_file = key.get_contents_to_filename('sound.wav')
    
    # process wav file with feature extraction module
    client = tornado.httpclient.AsyncHTTPClient()
    analyzer = feature_extraction.FeatureExtractor()
    response = yield tornado.gen.Task(client.fetch, analyzer.extract(wav_file))
    spectrum = response.effective_url

    # test only! Rewrite to send numpy data to perm storage(redis?)
    self.write("""<h2>Finshed processing audio! Frequency spectrum has been created!</h2>
                  <ul>
                    <li>Length: %s </li>
                    <li>Size: %s </li>
                  </ul>
              """ % (len(spectrum), sys.getsizeof(spectrum)))
    self.finish()

# TO DO: pass spectrum data array to the Sound Profiler modules
class SoundProfiling(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  @tornado.gen.engine
  def get(self):
    client = tornado.httpclient.AsyncHTTPClient()
    profiler = sound_profiler.SoundProfiler()
    response = yield tornado.gen.Task(client.fetch, profiler.extract(redis_key))
    profile = response.effective_url
    self.finsh()

# class AnomalyDetection(tornado.web.RequestHandler):
#   @tornado.web.asynchronous
#   @tornado.gen.engine
#     client = tornado.httpclient.AsyncHTTPClient()
#     profiler = known_sounds_profiler.SoundProfiler()
#     response = yield tornado.gen.Task(client.fetch, profiler.extract(redis_key))
#     profile = response.effective_url
#     self.finsh()

# TO DO:  1) Trigger 3rd party alert via API call
#         2) Send sprectum data to ML DB for processing
#         3) Final cleanup of sound file
class AlertML(tornado.web.RequestHandler):
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
  (r"/", MainPage), # testing placeholder! Remove!
  (r"/featureExtraction", FeatureExtraction),
  (r"/soundProfiling", SoundProfiling),
  # (r"/anomalyDetection", AnomalyDetection)
  (r"/AlertML", AlertML)
])


if __name__ == "__main__":
  port = 5000
  base = "http://localhost:" + str(port) + "/"
  app.listen(port)
  print "Web server started: " + base
  print "Test FeatExtr: " + base + "featureExtraction?q=test.wav"
  tornado.ioloop.IOLoop.instance().start()
  