import unittest
import os
import Features
import globalVars


class IOTestCase(unittest.TestCase):
    def setUp(self):  # NOQA
        self.problem_file = 'PUZ001+1.p'
        self.p_file_extended = os.path.join(globalVars.PATH, 'data',
                                            self.problem_file)

    def test_E_features_work(self):  # NOQA
        ef = Features.EFeatures()
        features = ef.get(self.p_file_extended)
        real_features = [5.0, 10.0, 15.0, 24.0, 68.0, 3.0, 5.0, 5.0, 7.0, 3.0,
                         1.0, 5.0, 2.0, 5.0, 7.0, 0.0, 0.714286, 1.0, 1.0, 1.0,
                         2.0, 1.0]
        self.assertEqual(features, real_features)
