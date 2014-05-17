"""
The metaclass for all StrategySchedulers.

Created on May 14, 2014

@author: Sil van de Leemput
"""

from abc import ABCMeta, abstractmethod


class StrategyScheduler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, config):
        """
        config: Load settings from a SafeConfigParser instance
        """
        pass

    @abstractmethod
    def fit(self, data_set, max_time):
        """
        data_set: As defined in DataSet.py
        max_time: Maximum time for scheduling
        """
        pass

    @abstractmethod
    def predict(self, time_left):
        """
        This method is to be called to determining the next best (strat, t)
        pair for solving the problem

        return (strategy, time)
            strategy: strategy string,
            time: time strategy should run (sec)
        """
        pass

    @abstractmethod
    def set_problem(self, problem_file):
        """
        problem_file: absolute path to the problem
        """
        pass

    @abstractmethod
    def set_problem_and_features(self, problem_file, problem_features):
        """
        problem_file: absolute path to the problem
        problem_features: features of the problem as numpy.array
        """
        pass

    @abstractmethod
    def update(self):
        """
        This method is to be called if the predicted (strat, t) pair from
        predict failed to solve the problem in order to update a possible
        internal model
        """
        pass
