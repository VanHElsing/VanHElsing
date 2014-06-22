'''
Created on May 15, 2014

@author: Daniel Kuehlwein
'''

import copy
import numpy as np
import operator
from sklearn.neighbors import NearestNeighbors
from src.data_util import not_solved_by_strat, remove_unsolveable_problems, load_dataset_from_config
from src.schedulers.SchedulerTemplate import StrategyScheduler


class NearestNeighborScheduler(StrategyScheduler):
    '''
    Basic scheduler that runs the first strategy in the dataset
    for its average time.
    '''

    def __init__(self, config=None):
        StrategyScheduler.__init__(self, config)
        try:
            self.min_neighbors = config.getint('Learner', 'min_neighbors')
        except:
            self.min_neighbors = 5
        try:
            self.mul_factor = config.getfloat('Learner', 'mul_factor')
        except:
            self.mul_factor = 1.1
        self.nr_of_neighbors = 2000
        self.model = NearestNeighbors(n_neighbors=self.nr_of_neighbors)
        self._data_set = None
        self.data_set = None
        self.last_strategy = None
        self.last_time = None
        self.local_strat_times = None
        self.max_time = None
        self.problem = None
        self.features = None
        self.config = config

    def fit(self, data_set, max_time, good_problems=None):
        self.max_time = max_time
        #self._data_set = remove_unsolveable_problems(data_set)
        self.data_set = data_set
        self.model.fit(self.data_set.feature_matrix)

    def predict(self, time_left):
        if self.data_set is None:
            # TODO: need Default mode
            return 'xx', time_left
        s_nr = self.data_set.strategy_matrix.shape[1]
        local_avg_times = [0.0] * s_nr
        local_max_times = [self.max_time] * s_nr
        local_solved = [0.0] * s_nr

        # Find similar problems
        if self.local_strat_times is None:
            neighbors = self.model.kneighbors(self.features)
            # Find close neighbours
            n_distances = neighbors[0][0]
            nr_index = min(len(n_distances)-1,self.min_neighbors)
            max_dist = n_distances[nr_index] * self.mul_factor
            for cut_off_index, dist in enumerate(n_distances):
                if dist > max_dist:
                    break
            n_indices = neighbors[1][0][:cut_off_index]
            self.local_strat_times = self.data_set.strategy_matrix[np.ix_(n_indices, range(s_nr))]
        # Get runtimes for similar problems
        for i in range(self.local_strat_times.shape[0]):
            for j in range(self.local_strat_times.shape[1]):
                val = self.local_strat_times[i, j]
                if val == -1:
                    continue
                local_avg_times[j] += val
                local_solved[j] += 1
                if val > local_max_times[j] or local_max_times[j] == self.max_time:
                    local_max_times[j] = val

        max_local_solved = max(local_solved)
        best_local_strategies = [i for i, i_solved in enumerate(local_solved) if i_solved == max_local_solved]
        best_local_strategies_max_times = [local_max_times[i] for i in best_local_strategies]
        self.last_strategy, self.last_time = min(zip(best_local_strategies, best_local_strategies_max_times), key=operator.itemgetter(1))
        assert self.last_time > 0
        strategy = self.data_set.strategies[self.last_strategy]
        return strategy, self.last_time

    def reset(self):
        if self._data_set is None:
            self._data_set = load_dataset_from_config(self.config)
        self.data_set = copy.deepcopy(self._data_set)
        self.model.fit(self.data_set.feature_matrix)
        self.local_strat_times = None

    def set_problem(self, problem_file):
        self.problem = problem_file
        self.features = self.feature_parser.get(problem_file)

    def set_problem_and_features(self, problem_file, problem_features):
        self.problem = problem_file
        self.features = problem_features

    def update(self):
        # Global Update
        good_problems = not_solved_by_strat(self.data_set, self.last_strategy, self.last_time)
        # Have to check that we do not run out of options
        if len(good_problems) == 0:
            self.model = None
            self.data_set = None
            self.local_strat_times = None
            return
        else:
            self.data_set = self.data_set.mask(good_problems)
        # Local Update
        s_nr = self.data_set.strategy_matrix.shape[1]
        lp_nr = self.local_strat_times.shape[0]
        local_good_problems = [i for i in range(lp_nr) if (self.local_strat_times[i, self.last_strategy] > self.last_time)]
        if len(local_good_problems) == 0:
            self.local_strat_times = None
            self.model.fit(self.data_set.feature_matrix)
        else:
            self.local_strat_times = self.local_strat_times[np.ix_(local_good_problems, range(s_nr))]

"""
# Test
from src import DataSet
from src.GlobalVars import LOGGER
d = DataSet.DataSet()
d.parse_E_data()

p_features = d.feature_matrix[0, :]

m = NearestNeighborScheduler()
m.set_problem_and_features('xx', p_features)
m.fit(d, 300)
LOGGER.info('Starting pred')
m.predict(10)
print m.data_set.strategy_matrix.shape
print m.local_strat_times.shape
LOGGER.info('ending pred')
m.update()
print m.data_set.strategy_matrix.shape
try:
    print m.local_strat_times.shape
except:
    print m.local_strat_times
LOGGER.info('ending update 1')
m.predict(10)
m.update()
print m.data_set.strategy_matrix.shape
try:
    print m.local_strat_times.shape
except:
    print m.local_strat_times
LOGGER.info('ending update 2')
m.predict(10)
m.update()
try:
    print m.data_set.strategy_matrix.shape
except:
    print m.data_set
try:
    print m.local_strat_times.shape
except:
    print m.local_strat_times
LOGGER.info('ending update 3')
m.reset()
LOGGER.info('Starting pred')
m.predict(10)
#"""
