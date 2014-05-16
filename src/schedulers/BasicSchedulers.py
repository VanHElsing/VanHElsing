'''
Created on May 15, 2014

@author: Daniel Kuehlwein
'''

import numpy as np
from src.schedulers.SchedulerTemplate import StrategyScheduler


class EAutoScheduler(StrategyScheduler):
    '''
    Basic scheduler for Eprover that just runs E's Auto mode.
    '''

    def __init__(self, config=None):
        StrategyScheduler.__init__(self, config)
        pass

    def fit(self, data_set):
        pass

    def predict(self, time_left):
        return '--auto-schedule', time_left

    def set_problem(self, problem_file):
        pass

    def update(self):
        pass


class SingleStrategyScheduler(StrategyScheduler):
    '''
    Basic scheduler that runs the first strategy in the dataset
    for its average time.
    '''

    def __init__(self, config=None):
        StrategyScheduler.__init__(self, config)
        if config == None:
            self.strategy_index = 0
        else:
            self.strategy_index = config.get("SingleStrategyScheduler", "strategy_index")
        self.data_set = None
        self.problem_file = None

    def fit(self, data_set):
        self.data_set = data_set

    def predict(self, time_left):
        strat_col = self.data_set.strategy_matrix[:, self.strategy_index]
        mask_invalid_times = strat_col != -1
        avg_time = np.average(strat_col, axis=0, weights=mask_invalid_times)
        strategy = self.data_set.strategies[self.strategy_index]
        return strategy, avg_time

    def set_problem(self, problem_file):
        self.problem_file = problem_file

    def update(self):
        pass
