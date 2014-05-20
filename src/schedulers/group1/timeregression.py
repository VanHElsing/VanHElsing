# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 15:19:17 2014

@author: Wouter Bulten

support vector regression
makkelijk vs moeilijk, mask over y < 10
"""
from sklearn import linear_model
import numpy as np


class TimeRegression():
    """
        Trains a regression model for every search strategy
    """

    def __init__(self, alpha=1.5, solver='auto', t_min=-1, t_max=300):
        """
            t_min: only data points with at least this value will be used
            t_max: only data points with a value below this will be used
        """
        self._models = []
        self._alpha = alpha
        self._solver = solver
        self._t_min = t_min
        self._t_max = t_max

    def fit(self, X, y):

        # Reset model list
        self._models = []

        for i, strat in enumerate(y.T):
            lr = linear_model.Ridge(alpha=self._alpha, solver=self._solver, fit_intercept=True, normalize=True)

            #Only use problems that can be solved
            mask = (strat > self._t_min) & (strat <= self._t_max)

            lr.fit(X[mask, :], (strat.T)[mask])

            self._models.append(lr)

    def predict(self, X):

        prediction = np.zeros([len(self._models)])

        for i, m in enumerate(self._models):
            prediction[i] = m.predict(X)

        return prediction

    def score(self, X, y):

        score = []

        for i, m in enumerate(self._models):

            mask = (y[:, i] > self._t_min) & (y[:, i] <= self._t_max)

            score.append(m.score(X[mask], (y[:, i])[mask]))

        return score
