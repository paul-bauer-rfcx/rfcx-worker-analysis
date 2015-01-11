'''
Detects anomalies in sounds
'''
import numpy as np
import unittest
from numpy.testing import assert_array_almost_equal,assert_almost_equal, assert_equal
from abc import ABCMeta, abstractmethod
import math

class AnomalyDetector(object):
    # basic dependency injection
    def __init__(self, logger, repository):
        self.logger = logger
        self.repo = repository

    '''Classifies sounds to categories'''
    def determine_anomaly(self, profile):
        '''
        determines the probability for anomalies
        '''
        guardian_id = profile.guardian_id # just for convenience
        # Todo: make it thread-safe
        model = self.repo.get_model(guardian_id)

        if model == None:
            model = Gaussian()
            self.logger.info("""Created new anomaly detection model for guardian_id %s""" % (guardian_id))

        spectrum = profile.spectrum.complex_arr

        # learn features for later modelling
        for column in spectrum.T:
            model.train(column)

        self.repo.update_model(guardian_id, model)
        self.logger.info("""Updated anomaly detection model for guardian_id %s""" % (guardian_id))

        profile.anomaly_prob = 0.0
        for column in spectrum.T:
            profile.anomaly_prob = max(model.calculate_prob(column), profile.anomaly_prob)

        self.logger.info("""Anomaly probability at guardian_id %s is %f""" % (guardian_id, profile.anomaly_prob))


"""
Models the ambient audio scenery. Based on that model
the object can distinguish between the ambient sounds
and sounds that are unlikely to occur naturally.
This class is abstract and both methods need to be
overriden in the actual implementations.
"""
class SignalLikelihood:
    __metaclass__ = ABCMeta

    @abstractmethod
    def train(self, features):
        """
        Use the supplied features to train a model for the ambient
        audio scenery. This will allow for the calculdation of the
        probability that a signal is different from the abient sound.
        """

    @abstractmethod
    def calculate_prob(self, features):
        """
        Calculates the probability that the signal described by the
        features is an ambient sound.
        """
        return 1.0

"""
Models the ambient audio scenery with multiple, independent
Gaussian distributions. Based on that model we can distinguish
between the ambient sounds and sounds that are
unlikely to occur naturally.
This model requires the assumption that the amplitudes
of frequencies are independent. Most likely we will need
to use a model that allows for correlations (multivariate
gaussian). For now, this is the simplest solution to the
problem.
Under the assumption of independence, we model each frequency
amplitude with a gaussian. We just need to save the mean
and variance of each frequency amplitude indepdently.
To test a signal, we calculate the probability of each of the
tested signal's frequency amplitude. Their product (independence)
will be  our meassure of the overall probability of hte signal
being ambient noise.
"""
class Gaussian(SignalLikelihood):
    def __init__(self, mean = None, var = None, sumSquareDif=None, n=0):
        self.mean = mean
        self.var = var
        self.sumSquareDif = sumSquareDif
        self.n = n

    def __eq__(self, other):
        return other != None and np.allclose(self.mean, other.mean) and np.allclose(self.var, other.var) and np.allclose(self.sumSquareDif,other.sumSquareDif) and self.n == other.n

    def train(self, features):
        """
        Updates the mean and variance of the gaussian model capturing the
        ambient sound scenery.
        """
        features = np.absolute(features)
        if self.mean is None:
            # no previous mean or variance exist
            self.mean = features

            # we need a zero vector with the size of the feature vector
            self.sumSquareDif = np.zeros_like(features)
            self.var = np.zeros_like(features)
            self.n = 1
        else:
            # previous mean is old_sum / old_n => new_sum = (old_sum * old_n) + new values
            old_mean = self.mean
            old_sum = old_mean * self.n
            new_sum = old_sum + features
            self.n = self.n + 1
            self.mean = new_sum / self.n

            # our vectorized adaption of Knuth's online variance algorithm
            # the original algorithm can be found here:
            # Donald E. Knuth (1998). The Art of Computer Programming, volume 2:
            # Seminumerical Algorithms, 3rd edn., p. 232. Boston: Addison-Wesley.

            # update sum of square differences
            self.sumSquareDif = self.sumSquareDif + (features - old_mean) * (features - self.mean)

            # update variance
            self.var = self.sumSquareDif / (self.n - 1)

    def calculate_prob(self, features):
        """
        Calculates the probability that the signal described by the
        features is an ambient sound.
        """
        features = np.absolute(features)
        if np.any(self.var == 0):
            return 0

        # this is a vectorized version of the pdf of a normal distribution for each frequency amplitude
        # it returns one probability for each of the signal's frequency amplitudes
        probs = np.exp(-(features-self.mean)**2/(2.*self.var**2)) / (math.sqrt(math.pi * 2.) * self.var)

        # simplificaiton: assumption of independent frequencies => product
        return np.prod(probs)


class GaussianTests(unittest.TestCase):
    def train(self, data):
        gaussian = Gaussian()

        for datum in data:
            gaussian.train(datum)

        return gaussian

    def checkMean(self, data, expectedMean):
        gaussian = self.train(data)
        assert_almost_equal(gaussian.mean, expectedMean)

    def checkVariance(self, data, exptectedVar):
        gaussian = self.train(data)
        assert_almost_equal(gaussian.var, exptectedVar)


    def test_mean_for_one_feature(self):
        data = [np.array([0.]), np.array([6.]), np.array([10.]), np.array([8.])]
        expectedMean = np.array([6.])

        self.checkMean(data, expectedMean)

    def test_mean_for_multiple_features(self):
        data = [np.array([0., 3.]), np.array([6., 8.]), np.array([10., 4.]), np.array([8., 7.])]
        expectedMean = np.array([6., 5.5])

        self.checkMean(data, expectedMean)

    def test_variance_for_one_feature(self):
        data = [np.array([1.]), np.array([0.]), np.array([2.]), np.array([1.]), np.array([0.])]
        expectedVariance = np.array([0.7])

        self.checkVariance(data, expectedVariance)

    def test_variance_for_one_feature(self):
        data = [np.array([1., 0.]), np.array([0., 2.]), np.array([2., 1.]), np.array([1., 0.]), np.array([0., 1.])]
        expectedVariance = np.array([0.7, 0.7])

        self.checkVariance(data, expectedVariance)

    def test_probability_calculation(self):
        gaussian = Gaussian()
        gaussian.mean = np.array([5., 3.])
        gaussian.var = np.array([2., 1.])
        x = np.array([4.,4.])

        expected = 0.0426
        actual = gaussian.calculate_prob(x)
        assert_almost_equal(actual,expected, decimal=4)
