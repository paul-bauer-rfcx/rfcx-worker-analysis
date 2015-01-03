import nose
import os
import sys
import nose
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from modules import db_layer
from modules.domain_modules import anomaly_detection 
import numpy as np 
import uuid
import unittest
import redis

class TestAnomalyDetectionRepo(unittest.TestCase):
    def setUp(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.repo = db_layer.AnomalyDetectionRepo()
        self.model = self.create_Gaussian() 
        self.key = "test:" + str(uuid.uuid4())
        self.station = "test:" + str(uuid.uuid4())

    def tearDown(self):
        # remove test data from db 
        if self.r.exists(self.key):
            self.r.delete(self.key)

    def create_Gaussian(self): 
        mean = np.array([1.2,2.3,3.4,4.2])
        var = np.array([2.1,902.1,23.1,5.1])
        sumSquareDif = np.array([23.1,23.5,1.3,52.1,412.1])
        n = 4
        return anomaly_detection.Gaussian(mean, var, sumSquareDif, n)

    def persist(self): 
        self.repo.update_model(self.station, self.model)

    def get(self):
        return self.repo.get_model(self.station)

    def test_create(self): 
        self.persist() 
        db_model = self.get()
        assert db_model == self.model

    def test_create(self): 
        self.persist() 
        db_model = self.get()
        assert db_model == self.model

if __name__ == "__main__": 
    unittest.main()