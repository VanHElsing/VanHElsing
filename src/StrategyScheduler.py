"""
Basic StrategyScheduler for solving ATP problems

Created on May 14, 2014

@author: Sil van de Leemput
"""

class StrategyScheduler(object):
    def __init__(self, problem, time_limit, model = None):
        """
        problem - input problem features
        timeLimit - time limit for solving the problem
        model - input trained model 
        """
        self._x = problem
        self._tlimit = time_limit
        self._model = model
        pass

    def predict(self, time_left):
        """
        This method is to be called to determining the next best (strat, t) pair for 
        solving the problem

        return (strat, t) strat: strategy_id, t: time strat should run (sec)
        """
        return strat, t

    def update(self):
        """
        This method is to be called if the predicted (strat, t) pair from predict
        failed to solve the problem in order to update a possible internal model
        """
        pass