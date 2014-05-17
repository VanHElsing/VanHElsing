import unittest
import os

from src import DataSet
from src import GlobalVars
from src.eval.evaluations import eval_against_dataset
from src.schedulers.BasicSchedulers import SingleStrategyScheduler


class IOTestCase(unittest.TestCase):
    def setUp(self):  # NOQA, pylint: disable=C0103
        self.problem_file = 'PUZ001+1.p'
        self.p_file_extended = os.path.join(GlobalVars.PATH, 'data',
                                            self.problem_file)
        self.dataset = DataSet.DataSet()
        self.dataset.parse_E_data()

    def test_single_strategy_scheduler(self):  # NOQA, pylint: disable=C0103
        scheduler = SingleStrategyScheduler()
        scheduler.fit(self.dataset,300)
        assert scheduler._strategy == 'protokoll_G-E--_107_B03_F1_PI_AE_Q4_CS_SP_PS_S0Y'
        solved = eval_against_dataset(self.dataset, scheduler, 300)
        self.assertAlmostEqual(solved, 0.619848695998)  
