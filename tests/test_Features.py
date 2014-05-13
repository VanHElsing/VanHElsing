import unittest
import os
import Features
import GlobalVars


class IOTestCase(unittest.TestCase):
    def setUp(self):  # NOQA, pylint: disable=C0103
        self.problem_file = 'PUZ001+1.p'
        self.p_file_extended = os.path.join(GlobalVars.PATH, 'data',
                                            self.problem_file)

    def test_E_features_work(self):  # NOQA, pylint: disable=C0103
        ef_obj = Features.EFeatures()
        features = ef_obj.get(self.p_file_extended)
        real_features = [5.0, 10.0, 15.0, 24.0, 68.0, 3.0, 5.0, 5.0, 7.0, 3.0,
                         1.0, 5.0, 2.0, 5.0, 7.0, 0.0, 0.714286, 1.0, 1.0, 1.0,
                         2.0, 1.0]
        self.assertEqual(features, real_features)
