'''
Contains repositories for domain modules 
''' 
import uuid
import redis
def c(s):
	print s

class AnomalyDetectionRepo: 
	'''
	Now working with Redis,...
	'''
	


	def __init__(self):
		self.model = None
		self.r= redis.StrictRedis(host='localhost', port=6379, db=0)
		self.baseH= "baseHash"
		self.r.set('foo', 'bar')
		bee= self.r.get('foo')
		c(bee)

	def register_station(self, station):
		''' registers a new guardian/station into the system'''
		# lets assume station is simply a string.
		stationHZ= uuid.uuid4()
		c(stationHZ)
		c(station)
		c(self.r)

		self.r.hset(self.baseH, station, stationHZ)
		x= self.r.hget(self.baseH, station)
		c(x)


	def get_model(self, station): 
		''' returns the current model or None, if
		no model exists'''
		# Todo: get model from redis
		return self.model 

	def update_model(self, station, model): 
		# Todo: save model to redis 
		self.model = model 

x= AnomalyDetectionRepo()
x.register_station("station1")

