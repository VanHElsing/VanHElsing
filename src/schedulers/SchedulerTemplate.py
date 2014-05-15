"""
The metaclass for all StrategySchedulers.

Created on May 14, 2014

@author: Sil van de Leemput
"""

from abc import ABCMeta, abstractmethod


class StrategyScheduler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def fit(self, data_set):
        """
        data_set: As defined in DataSet.py
        """
        # TODO implement Pickable model
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
    def update(self):
        """
        This method is to be called if the predicted (strat, t) pair from
        predict failed to solve the problem in order to update a possible
        internal model
        """
        pass
