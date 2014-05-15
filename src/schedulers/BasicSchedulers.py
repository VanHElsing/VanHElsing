'''
Created on May 15, 2014

@author: Daniel Kuehlwein
'''

from src.schedulers.SchedulerTemplate import StrategyScheduler


class EAutoScheduler(StrategyScheduler):
    '''
    Basic scheduler for Eprover that just runs E's Auto mode.
    '''

    def __init__(self, problem, time_limit, model=None):
        pass

    def fit(self, data_set):
        pass

    def predict(self, time_left):
        return '--auto-schedule', time_left

    def update(self):
        pass


class SingleStrategyScheduler(StrategyScheduler):
    '''
    Basic scheduler that runs the first strategy in the dataset
    for its average time.
    '''

    def __init__(self, problem, time_limit, model=None, strategy_index=None):
        if strategy_index is None:
            self.strategy_index = 0
        else:
            self.strategy_index = strategy_index

    def fit(self, data_set):
        self.data_set = data_set

    def predict(self, time_left):
        strat_col = self.data_set.strategy_matrix[:, self.strategy_index]
        mask_invalid_times = ((strat_col != -1).T).tolist()[0]
        avg_times = strat_col.mean(axis=0, weigths=mask_invalid_times)
        strategy = self.data_set.strategies[0]
        strategy_time = avg_times[0, 0]
        return strategy, strategy_time

    def update(self):
        pass