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

    def fit(self, data_set, max_time):
        pass

    def predict(self, time_left):
        return '--auto-schedule', time_left

    def set_problem(self, problem_file):
        pass

    def set_problem_and_features(self, problem_file, problem_features):
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
            idx = int(config.get("SingleStrategyScheduler", "strategy_index"))
            self.strategy_index = idx
        self._avg_time = self._strategy = 0
        pass

    def fit(self, data_set, max_time):
        strat_col = data_set.strategy_matrix[:, self.strategy_index]
        mask_invalid_times = strat_col != -1
        avg = np.average(strat_col, axis=0, weights=mask_invalid_times)
        self._avg_time = avg
        self._strategy = data_set.strategies[self.strategy_index]
        pass

    def predict(self, time_left):
        return self._strategy, self._avg_time

    def set_problem(self, problem_file):
        pass

    def set_problem_and_features(self, problem_file, problem_features):
        pass

    def update(self):
        pass
