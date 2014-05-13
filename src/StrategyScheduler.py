"""
Basic StrategyScheduler for solving ATP problems

Created on May 14, 2014

@author: Sil van de Leemput
"""


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
        pass

    def fit(self, X, Y):  # NOQA
        """
        X - input problem features (problems x features)
        Y - label strategy times (problems x strategies)
        """
        # TODO implement Pickable model
        model = None
        return model

    def predict(self, time_left):
        """
        This method is to be called to determining the next best (strat, t)
        pair for solving the problem

        return (strategy, time)
            strategy: strategy_id,
            time: time strategy should run (sec)
        """
        strategy = ""
        time = 0
        return strategy, time

    def update(self):
        """
        This method is to be called if the predicted (strat, t) pair from
        predict failed to solve the problem in order to update a possible
        internal model
        """
        pass
