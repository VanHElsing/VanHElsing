'''
Created on May 15, 2014

@author: Daniel Kuehlwein
'''

import numpy as np
import operator
from sklearn.neighbors import NearestNeighbors
from src.schedulers.SchedulerTemplate import StrategyScheduler

class NearestNeighborScheduler(StrategyScheduler):
    '''
    Basic scheduler that runs the first strategy in the dataset
    for its average time.
    '''

    def __init__(self, config=None):
        self.nr_of_neighbors = 2000
        self.model = NearestNeighbors(n_neighbors=self.nr_of_neighbors)
        self.deleted_neigbors = set([])
        self.last_strategy = None
        self.last_time = None

    def fit(self, data_set, max_time):
        self.max_time = max_time
        self.data_set = data_set
        nr_of_problems = self.data_set.strategy_matrix.shape[0]
        nr_of_strats = self.data_set.strategy_matrix.shape[1]
        nr_of_features = self.data_set.feature_matrix.shape[1]
        s_m = self.data_set.strategy_matrix 
        solvable = [i for i in range(nr_of_problems) if (not max(s_m[i,:]) == -1)]     
        self.data_set.feature_matrix = self.data_set.feature_matrix[np.ix_(solvable,range(nr_of_features))] 
        self.data_set.strategy_matrix = self.data_set.strategy_matrix[np.ix_(solvable,range(nr_of_strats))]
        self.data_set.problems = self.data_set.problems[solvable]
        self.model.fit(data_set.feature_matrix)

    def predict(self, time_left):
        neighbors = self.model.kneighbors(self.features)
        n_indices = neighbors[1][0][:10]
        s_nr = self.data_set.strategy_matrix.shape[1]
        strat_times = self.data_set.strategy_matrix[np.ix_(n_indices,range(s_nr))]
        med_times = [0.0] * s_nr
        max_times = [300.0] * s_nr
        local_solved = [0.0] * s_nr
        for i in range(strat_times.shape[0]):
            for j in range(strat_times.shape[1]):
                val = strat_times[i,j]
                if val == -1:
                    continue
                med_times[j] += val 
                local_solved[j] += 1
                if val > max_times[j] or max_times[j] == 300:
                    max_times[j] = val
        s_index, s_time = min(enumerate(max_times), key=operator.itemgetter(1))
        print s_index,s_time
        assert s_time > 0
        strategy = self.data_set.strategies[s_index]
        return strategy, s_time

    def set_problem(self, problem_file):
        self.problem = problem_file

    def set_problem_and_features(self, problem_file, problem_features):
        self.set_problem(problem_file)
        self.features = problem_features

    def update(self):
        # NEED UPDATE IF IT DID NOT SOLVE!!
        pass

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
print m.predict(10)
LOGGER.info('ending pred')
#"""