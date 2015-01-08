'''
Contains repositories for domain modules
'''
import random
import uuid
import redis
import numpy as np
from domain_modules import anomaly_detection

def c(*s):
    print s

class AnomalyDetectionRepo:
    '''
    Now working with Redis,...
    '''
    def __init__(self):
        self.model = None
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.baseH= "baseHash"

    def register_station(self, station):
        ''' registers a new guardian/station into the system'''
        # lets assume station is simply a string.
        stationHZ= uuid.uuid4()
        meanLZ= uuid.uuid4()
        varianceLZ= uuid.uuid4()
        sumSquareDifZ = uuid.uuid4()
        nZ = uuid.uuid4()
        self.r.hset(self.baseH, station, stationHZ)
        stationH = {'varianceLZ': varianceLZ,
                    'meanLZ': meanLZ,
                    'sumSquareDifZ': sumSquareDifZ,
                    'nZ': nZ
                    }
        self.r.hmset(stationHZ, stationH)

    def toNumpy(self, array):
        np_array = np.array(array)
        return np_array.astype(np.float)

    def get_model(self, station):
        ''' returns the current model or None, if
        no model exists'''
        exists= self.r.hexists(self.baseH, station)

        if not exists:
            return None

        # get keys
        stationHZ= self.r.hget(self.baseH, station)
        stationH= self.r.hgetall(stationHZ)
        meanLZ= stationH['meanLZ']
        varianceLZ= stationH['varianceLZ']
        sumSquareDifZ = stationH['sumSquareDifZ']
        nZ = stationH['nZ']

        # model variables
        m_mean = self.toNumpy( self.r.lrange(meanLZ, 0, -1) )
        m_var = self.toNumpy( self.r.lrange(varianceLZ, 0, -1) )
        m_sumSquareDif = self.toNumpy( self.r.lrange(sumSquareDifZ, 0,-1) )
        m_n = float( self.r.get(nZ) )
        return anomaly_detection.Gaussian( m_mean, m_var, m_sumSquareDif, m_n)


    def update_model(self, station, model):
        exists= self.r.hexists(self.baseH, station)
        if not(exists):
            c("need to register it first")
            self.register_station(station)
        stationHZ= self.r.hget(self.baseH, station)
        stationH= self.r.hgetall(stationHZ)
        meanLZ= stationH['meanLZ']
        varianceLZ= stationH['varianceLZ']
        sumSquareDifLZ = stationH['sumSquareDifZ']
        nLZ = stationH['nZ']

        self.r.delete(meanLZ)
        self.r.delete(varianceLZ)
        self.r.delete(sumSquareDifLZ)
        self.r.rpush(meanLZ, *model.mean)
        self.r.rpush(varianceLZ, *model.var)
        self.r.rpush(sumSquareDifLZ, *model.sumSquareDif)
        self.r.set(nLZ, model.n)
