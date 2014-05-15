'''
Created on May 15, 2014

@author: Daniel Kuehlwein
'''

from src.DataSet import DataSet
from src.schedulers.SchedulerTemplate import StrategyScheduler

class EAutoScheduler(StrategyScheduler):
    '''
    Basic scheduler for Eprover that just runs E's Auto mode.
    '''

    def __init__(self, problem, time_limit, model=None):
        """
        problem - input problem features
        timeLimit - time limit for solving the problem
        model - input trained model
        """
        pass

    def fit(self, DataSet):
        pass

    def predict(self, time_left):
        """
        This method is to be called to determining the next best (strat, t)
        pair for solving the problem

        return (strategy, time)
            strategy: strategy_id,
            time: time strategy should run (sec)
        """
        return '--auto-schedule', time_left

    def update(self):
        """
        This method is to be called if the predicted (strat, t) pair from
        predict failed to solve the problem in order to update a possible
        internal model
        """
        pass