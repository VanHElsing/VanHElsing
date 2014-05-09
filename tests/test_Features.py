import unittest
import os
from src import Features
from src import globalVars

class IOTestCase(unittest.TestCase):
    def setUp(self):
        self.problemFile = 'PUZ001+1.p'
        self.pFileExtended = os.path.join(globalVars.PATH,'data',self.problemFile)
        
    def test_E_features_work(self):
        ef = Features.EFeatures()
        features = ef.get(self.pFileExtended)
        realFeatures = [5.0, 10.0, 15.0, 24.0, 68.0, 3.0, 5.0, 5.0, 7.0, 3.0, 1.0, 5.0, 2.0, 5.0, 7.0, 0.0, 0.714286, 1.0, 1.0, 1.0, 2.0, 1.0]
        self.assertEqual(features, realFeatures)


