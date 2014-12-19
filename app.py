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

# import RFCx custom modules via service layer
from modules import serviceLayer

class analyzeSound(tornado.web.RequestHandler):
  @tornado.gen.coroutine
  def post(self):
    

class AddKnownSoundProfile(tornado.web.RequestHandler):
  # TO DO: allow the ML framework a way to interact with sound profiling to update it as needed
  @tornado.gen.coroutine
  def get(self):
    self.finsh()

# routes to call the correct handlers
app = tornado.web.Application([
  (r"/analyzeSound", spectralAnalysis),
  (r"/addKnownSoundProfile", AddKnownSoundProfile)
])

if __name__ == "__main__":
  port = 5000
  base = "http://localhost:" + str(port) + "/"
  app.listen(port)
  print "Web server started: " + base
  tornado.ioloop.IOLoop.instance().start()
  