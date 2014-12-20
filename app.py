# web server modules
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.gen
import json

# import Tornado and AWS settings from file
import settings
from tornado.options import options

# import RFCx custom modules via service layer
from modules import service_layer

class AnalyzeSound(tornado.web.RequestHandler):
  @tornado.gen.coroutine
  def post(self):
    # filename = json.loads(self.request.body)['filename']
    self.finish()

class UpdateSoundProfile(tornado.web.RequestHandler):
  @tornado.gen.coroutine
  def post(self):
    self.finsh()

# routes to call the correct request handlers
app = tornado.web.Application([
  (r"/analyzeSound", AnalyzeSound),
  (r"/updateSoundProfile", UpdateSoundProfile)
])

if __name__ == "__main__":
  port = 5000
  app.listen(port)
  print "Web server started: http://localhost:" + str(port) + "/"
  tornado.ioloop.IOLoop.instance().start()
  