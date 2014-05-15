import unittest
import os

from src import DataSet
from src import GlobalVars
from src.schedulers import init_scheduler


class IOTestCase(unittest.TestCase):
    def setUp(self):  # NOQA, pylint: disable=C0103
        self.problem_file = 'PUZ001+1.p'
        self.p_file_extended = os.path.join(GlobalVars.PATH, 'data',
                                            self.problem_file)
        self.data_set = DataSet.DataSet('E')

    def test_E_features_work(self):  # NOQA, pylint: disable=C0103
        scheduler = init_scheduler(self.p_file_extended, 3, 'Single')
        scheduler.fit(self.data_set)
        """
        features = ef_obj.get(self.p_file_extended)
        real_features = [5.0, 10.0, 15.0, 24.0, 68.0, 3.0, 5.0, 5.0, 7.0, 3.0,
                         1.0, 5.0, 2.0, 5.0, 7.0, 0.0, 0.714286, 1.0, 1.0, 1.0,
                         2.0, 1.0]
        self.assertEqual(features, real_features)
        """
