# web server modules
from tornado import httpserver, ioloop, httpclient, web, gen, options
import json

# import Tornado and AWS settings from file
import settings
# import RFCx custom modules via service layer
from modules import service_layer

class AnalyzeSound(web.RequestHandler):
  @web.asynchronous
  @gen.engine
  def post(self):
    # parse JSON received to get filename/key
    key = json.loads(self.request.body)['filename']
    # SL call to analyze the audio linked to given key value
    response = yield service_layer.AnalyzeSound(key)
    self.write(response.body)
    self.finish()

class UpdateSoundProfile(web.RequestHandler):
  @web.asynchronous
  @gen.engine
  def post(self):
    self.finsh()

# routes to call the correct request handlers
app = web.Application([
  (r"/analyzeSound", AnalyzeSound),
  (r"/updateSoundProfile", UpdateSoundProfile)
])

if __name__ == "__main__":
  port = 5000
  app.listen(port)
  print "Web server started: http://localhost:" + str(port) + "/"
  ioloop.IOLoop.instance().start()
  