'''
Contains repositories for domain modules 
''' 
import random
import uuid
import redis
def c(*s):
	print s

class AnomalyDetectionRepo: 
	'''
	Now working with Redis,...
	'''

	def __init__(self):
		self.model = None
		self.r= redis.StrictRedis(host='localhost', port=6379, db=0)
		self.baseH= "baseHash"

	def register_station(self, station):
		''' registers a new guardian/station into the system'''
		# lets assume station is simply a string.
		stationHZ= uuid.uuid4()
		meanLZ= uuid.uuid4()
		varianceLZ= uuid.uuid4()
		self.r.hset(self.baseH, station, stationHZ)
		stationH= {'varianceLZ': varianceLZ, 'meanLZ': meanLZ}
		self.r.hmset(stationHZ, stationH)

	def get_model(self, station): 
		''' returns the current model or None, if
		no model exists'''
		exists= self.r.hexists(self.baseH, station)
		if exists:
			stationHZ= self.r.hget(self.baseH, station)
			stationH= self.r.hgetall(stationHZ)
			meanLZ= stationH['meanLZ']
			varianceLZ= stationH['varianceLZ']
			s_meanL= self.r.lrange(meanLZ, 0, -1)
			s_varianceL= self.r.lrange(varianceLZ, 0, -1)
			if (len(s_meanL) == 0):
				return None
			else:
				meanL= []
				varianceL= []
				for i in s_meanL:
					f= float(i)
					meanL.append(f)
				for j in s_varianceL:
					g= float(j)
					varianceL.append(g)
				return {'meanL': meanL, 'varianceL': varianceL}
		else:
			return "no such station!"

	def update_model(self, station, model):
		# here we assume station is a string and model looks like:
		# model= {'meanL': [bunch of floats], 'varianceL' [bunch of floats] }
		exists= self.r.hexists(self.baseH, station)
		if not(exists):
			c("need to register it first")
			self.register_station(station)
		stationHZ= self.r.hget(self.baseH, station)
		stationH= self.r.hgetall(stationHZ)
		meanLZ= stationH['meanLZ']
		varianceLZ= stationH['varianceLZ']
		meanL= model['meanL']
		varianceL= model['varianceL']
		self.r.delete(meanLZ)
		self.r.delete(varianceLZ)
		self.r.rpush(meanLZ, *meanL)
		self.r.rpush(varianceLZ, *varianceL)

# TESTS INLINE

x= AnomalyDetectionRepo()
station= "station1"
x.register_station(station)

nonexistentStation= "stationNonExiste"
val0= x.get_model(nonexistentStation)
c("nonexistent: ", val0)

meanL= []
varianceL= []
for i in range(0, 500):
	w=random.random()
	u=random.random()
	meanL.append(w)
	varianceL.append(u)
#c(meanL)
c("length of meanL prior to update", len(meanL))
#c(varianceL)
stub= {'meanL': meanL, 'varianceL': varianceL}

anotherNonexistent= "anotherNon"
x.update_model(anotherNonexistent, stub)
val1= x.get_model(anotherNonexistent)
c("len(val1)", len(val1))

x.update_model(station, stub)

z= x.get_model(station)
#c(z['meanL'])
#c(z['varianceL'])
c("type of a given value in varianceL ",type(z['varianceL'][4]))

problem= 'false'
for i in range(0, 500):
	if (  (meanL[i] != z['meanL'][i]) or (varianceL[i] != z['varianceL'][i])):
		c('problem')
		problem= 'true'

if (problem == 'true'):
	c('there was an error in transcription')
else:
	c("the arrays outputed are the same as those inputed! ALL GOOD!")

# now test to verify that nonexistent or station without model should return none

