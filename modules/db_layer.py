'''
Contains repositories for domain modules 
''' 

class AnomalyDetectionRepo: 
	'''
	Todo: replace the mock by a reddis implementation 
		  with the same signatures 
	'''
	def __init__(self):
		self.model = None

	def get_model(self, station): 
		''' returns the current model or None, if
		no model exists'''
		# Todo: get model from redis
		return self.model 

	def udpate_model(self, station, model): 
		# Todo: save model to redis 
		self.model = model 
