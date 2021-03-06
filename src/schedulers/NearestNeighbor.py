'''
Contains the nearest neighbor scheduler.
'''

import ConfigParser
import copy
import numpy as np
import operator
from sklearn.neighbors import NearestNeighbors
from src.data_util import not_solved_by_strat,\
    remove_unsolveable_problems,\
    load_dataset_from_config
from src.schedulers.SchedulerTemplate import StrategyScheduler


class NearestNeighborScheduler(StrategyScheduler):  # pylint: disable=too-many-instance-attributes
    '''
    Uses the nearest neighbor algorithm to predict which strategy to run next.
    The strategy that solves most of the neighboring problems in the least
    amount of time is picked.
    '''
    def __init__(self, config=None):
        StrategyScheduler.__init__(self, config)
        try:
            self.min_neighbors = config.getint('Learner', 'min_neighbors')
        except ConfigParser.NoOptionError:
            self.min_neighbors = 5
        try:
            self.mul_factor = config.getfloat('Learner', 'mul_factor')
        except ConfigParser.NoOptionError:
            self.mul_factor = 1.1
        try:
            self.negscore_func = config.get('Learner', 'negscore_func')
        except ConfigParser.NoOptionError:
            self.negscore_func = 'max'
        try:
            self.try_auto = config.get('Learner', 'try_auto')
        except ConfigParser.NoOptionError:
            self.try_auto = False
        self.nr_of_neighbors = 2000
        self.model = NearestNeighbors(n_neighbors=self.nr_of_neighbors)  # pylint: disable=unexpected-keyword-arg, no-value-for-parameter
        self._data_set = None
        self.data_set = None
        self.last_strategy = None
        self.last_time = None
        self.local_strat_times = None
        self.max_time = None
        self.problem = None
        self.features = None
        self.config = config

    def fit(self, data_set, max_time):
        self.max_time = max_time
        self._data_set = remove_unsolveable_problems(data_set)
        self.data_set = remove_unsolveable_problems(data_set)
        self.model.fit(self.data_set.feature_matrix)

    def predict(self, time_left):
        if self.data_set is None:
            # IMPROVEMENT: Make default mode an option of the config file.
            return '', time_left
        s_nr = self.data_set.strategy_matrix.shape[1]
        local_avg_times = [0.0] * s_nr
        local_solved = [0.0] * s_nr

        # Find similar problems, and get the strategy times for those problems
        if self.local_strat_times is None:
            neighbors = self.model.kneighbors(self.features)
            # Find close neighbors
            n_distances = neighbors[0][0]
            nr_index = min(len(n_distances), self.min_neighbors) - 1
            max_dist = n_distances[nr_index] * self.mul_factor
            cut_off_index = None
            for loc_cut_off_index, dist in enumerate(n_distances):
                if dist > max_dist:
                    cut_off_index = loc_cut_off_index
                    break

            # List of similar problems
            n_indices = neighbors[1][0][:cut_off_index]
            # Get strategy times for similar problems
            idx = np.ix_(n_indices, range(s_nr))  # NOQA, pylint: disable=E1101
            self.local_strat_times = self.data_set.strategy_matrix[idx]

        # Get runtimes for similar problems
        for i in range(self.local_strat_times.shape[0]):
            for j in range(self.local_strat_times.shape[1]):
                val = self.local_strat_times[i, j]
                if val == -1:
                    continue
                local_avg_times[j] += val
                local_solved[j] += 1

        max_local_solved = max(local_solved)
        best_local_strategies = [i for i, i_solved in enumerate(local_solved)
                                 if i_solved == max_local_solved]

        best_local_strategies_times = [[time for time in self.local_strat_times.T[j] if time != -1] for j in best_local_strategies]
        best_local_strategies_max_times = [max(times) for times in best_local_strategies_times]

        if self.negscore_func == 'max':
            best_local_strategies_negscore = best_local_strategies_max_times
        elif self.negscore_func == 'median':
            best_local_strategies_negscore = [np.median(times) for times in best_local_strategies_times]
        elif self.negscore_func == 'mean':
            best_local_strategies_negscore = [np.mean(times) for times in best_local_strategies_times]
        elif self.negscore_func == 'meanmedian':
            best_local_strategies_negscore = [np.mean(times) for times in best_local_strategies_times]
            best_local_strategies_max_times = [np.median(times) for times in best_local_strategies_times]

        zipped = zip(best_local_strategies, best_local_strategies_max_times,
                     best_local_strategies_negscore)

        # IMPROVEMENT: Use median/mean times instead of max.
        self.last_strategy, self.last_time, _s = min(zipped, key=operator.itemgetter(2))  # NOQA, pylint: disable=C0301
        assert self.last_time > 0
        strategy = self.data_set.strategies[self.last_strategy]
        
        if self.last_time <= time_left:
            return strategy, self.last_time
        elif self.try_auto:
            return "protokoll_X----_schedauto_300", time_left
        else:
            return strategy, time_left

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
        good_problems = not_solved_by_strat(self.data_set,
                                            self.last_strategy,
                                            self.last_time)
        # Check that we do not run out of options
        if len(good_problems) == 0:
            self.model = None
            self.data_set = None
            self.local_strat_times = None
            return
        else:
            self.data_set = self.data_set.mask(good_problems)
        # Local Update
        lp_nr = self.local_strat_times.shape[0]
        local_good_problems = [i for i in range(lp_nr) if (self.local_strat_times[i, self.last_strategy] > self.last_time)]
        if len(local_good_problems) == 0:
            self.local_strat_times = None
            self.nr_of_neighbors = min(self.nr_of_neighbors, len(good_problems))
            self.model = NearestNeighbors(n_neighbors=self.nr_of_neighbors)  # pylint: disable=unexpected-keyword-arg, no-value-for-parameter
            self.model.fit(self.data_set.feature_matrix)
        else:
            s_nr = self.data_set.strategy_matrix.shape[1]
            idx = np.ix_(local_good_problems, range(s_nr))  # NOQA, pylint: disable=E1101
            self.local_strat_times = self.local_strat_times[idx]
