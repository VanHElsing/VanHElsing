'''
Created on May 22, 2014

@author: Daniel Kuehlwein
'''

import copy
import numpy as np
from src.schedulers.SchedulerTemplate import StrategyScheduler
from src.data_util import remove_unsolveable_problems, not_solved_by_strat


class GreedyScheduler(StrategyScheduler):

    def __init__(self, config):
        StrategyScheduler.__init__(self, config)
        self.data_set = None
        self._data_set = None
        self.problem = None
        self.features = None
        self.last_strategy = None
        self.last_time = None

    def fit(self, data_set, max_time):
        self._data_set = remove_unsolveable_problems(data_set)
        self.data_set = copy.deepcopy(self._data_set)

    def predict(self, time_left, run_time=None):
        if run_time is None:
            run_time = 1.0
        solveable_problems = (-1 < self.data_set.strategy_matrix) & (self.data_set.strategy_matrix < run_time)
        solved_in_run_time = np.sum(solveable_problems, axis=0)
        self.last_strategy = solved_in_run_time.argmax()
        self.last_time = run_time
        strategy = self.data_set.strategies[self.last_strategy]
        return strategy, run_time

    def reset(self):
        self.data_set = copy.deepcopy(self._data_set)

    def set_problem(self, problem_file):
        self.problem = problem_file

    def set_problem_and_features(self, problem_file, problem_features):
        self.problem = problem_file
        self.features = problem_features

    def update(self):
        good_problems = not_solved_by_strat(self.data_set, self.last_strategy, self.last_time)
        # TODO: Have to check that we do not run out of options
        self.data_set = self.data_set.mask(good_problems)


