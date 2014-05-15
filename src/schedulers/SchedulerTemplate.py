"""
The metaclass for all StrategySchedulers.

Created on May 14, 2014

@author: Sil van de Leemput
"""

from src.DataSet import DataSet


class StrategyScheduler(object):
    def __init__(self, problem, time_limit, model=None):
        """
        problem - input problem features
        timeLimit - time limit for solving the problem
        model - input trained model
        """
        self.x = problem
        self.time_limit = time_limit
        self.model = model
        raise NotImplementedError
        pass

    def fit(self, DataSet):  # NOQA
        """
        feature_matrix - input problem features (problems x features)
        strategy_matrix - strategy times (problems x strategies)
        """
        # TODO implement Pickable model
        model = None
        raise NotImplementedError
        return model

    def predict(self, time_left):
        """
        This method is to be called to determining the next best (strat, t)
        pair for solving the problem

        return (strategy, time)
            strategy: strategy_id,
            time: time strategy should run (sec)
        """
        raise NotImplementedError
        strategy = ""
        time = 0
        return strategy, time

    def update(self):
        """
        This method is to be called if the predicted (strat, t) pair from
        predict failed to solve the problem in order to update a possible
        internal model
        """
        raise NotImplementedError
