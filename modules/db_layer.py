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
		meanLZ= uuid.uuid4()
		varianceLZ= uuid.uuid4()
		c(stationHZ)
		c(station)
		c(self.r)

		self.r.hset(self.baseH, station, stationHZ)
		x= self.r.hget(self.baseH, station)
		c(x)
		stationH= {'varianceLZ': varianceLZ, 'meanLZ': meanLZ}
		self.r.hmset(stationHZ, stationH)
		y= self.r.hgetall(stationHZ)
		c(y)
		c("and that's it we're good to go.")

	def get_model(self, station): 
		''' returns the current model or None, if
		no model exists'''
		stationHZ= self.r.hget(self.baseH, station)
		stationH= self.r.hgetall(stationHZ)
		return stationHZ


	def update_model(self, station, model): 
		# Todo: save model to redis 
		#self.model = model 
		# here we assume station is a string and model looks like:
		# model= {'meanL': [bunch of floats], 'varianceL' [bunch of floats] }

x= AnomalyDetectionRepo()
x.register_station("station1")

