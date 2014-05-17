import unittest
import os

from src import DataSet
from src import GlobalVars
from src.schedulers.BasicSchedulers import SingleStrategyScheduler


class IOTestCase(unittest.TestCase):
    def setUp(self):  # NOQA, pylint: disable=C0103
        self.problem_file = 'PUZ001+1.p'
        self.p_file_extended = os.path.join(GlobalVars.PATH, 'data',
                                            self.problem_file)
        self.data_set = DataSet.DataSet()
        self.data_set.parse_E_data()

    def test_single_strategy_scheduler(self):  # NOQA, pylint: disable=C0103
        strategy_index = 0
        self.assertEqual(self.data_set.strategies[0],
                         'protokoll_G-E--_107_B03_F1_PI_AE_Q4_CS_SP_PS_S0Y')
        scheduler = SingleStrategyScheduler(strategy_index)
        scheduler.set_problem(self.p_file_extended)
        scheduler.fit(self.data_set)
        strat, strat_time = scheduler.predict(10)
        self.assertEqual(strat,
                         'protokoll_G-E--_107_B03_F1_PI_AE_Q4_CS_SP_PS_S0Y')
        self.assertAlmostEqual(strat_time, 10.4048506749)
