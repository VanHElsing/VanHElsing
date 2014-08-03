'''
Contains several simple strategy schedulers.
'''

import numpy as np
from src.schedulers.SchedulerTemplate import StrategyScheduler


class EAutoScheduler(StrategyScheduler):
    '''
    Basic scheduler for Eprover that just runs E's Auto mode.
    '''

    def __init__(self, config=None):
        StrategyScheduler.__init__(self, config)

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

    def reset(self):
        pass


class SingleStrategyScheduler(StrategyScheduler):
    '''
    Basic scheduler that runs the first strategy in the dataset
    for its average time, or a specific strategy specified by
    SingleStrategyScheduler.strategy_index.
    '''

    def __init__(self, config=None):
        StrategyScheduler.__init__(self, config)
        if config is None:
            self.strategy_index = 0
        else:
            idx = config.getint("SingleStrategyScheduler", "strategy_index")
            self.strategy_index = idx
        self._avg_time = self._strategy = 0

    def fit(self, data_set, max_time):
        strat_col = data_set.strategy_matrix[:, self.strategy_index]
        mask_invalid_times = strat_col != -1
        avg = np.average(strat_col, axis=0, weights=mask_invalid_times)  # NOQA, pylint: disable=E1101
        self._avg_time = avg
        self._strategy = data_set.strategies[self.strategy_index]

    def predict(self, time_left):
        return self._strategy, self._avg_time

    def set_problem(self, problem_file):
        pass

    def set_problem_and_features(self, problem_file, problem_features):
        pass

    def update(self):
        pass

    def reset(self):
        pass
