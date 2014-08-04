# -*- coding: utf-8 -*-
'''
Created on Wed Apr  9 15:19:17 2014

@author: Wouter Bulten, Sil van de Leemput

Support vector regression
'''
from sklearn import linear_model
import numpy as np


class TimeRegression():
    '''
    Trains a regression model for every search strategy,
    which is used for predicting the time a strategy needs to solve a problem
    '''

    def __init__(self, alpha=1.5, solver='auto', t_min=-1, t_max=300):
        '''
        General time regression class for estimating the time
        a strategy needs to solve a problem

        Variables
        ---------
        alpha  : ridge model parameter
        solver : ridge model parameter
        t_min  : only data points with at least this value will be used
        t_max  : only data points with a value below this will be used
        '''
        self._models = []
        self._alpha = alpha
        self._solver = solver
        self._t_min = t_min
        self._t_max = t_max

    def fit(self, X, Y):
        '''
        Function for training the linear regression model

        Parameters
        ----------
        X : numpy array
            feature matrix          (problems x features)
        Y : numpy array
            target timing matrix    (problems x strategies)
        '''
        # Reset model list
        self._models = []
        for strat in Y.T:
            linr = linear_model.Ridge(alpha=self._alpha, solver=self._solver,
                                      fit_intercept=True, normalize=True)
            # Only use problems that can be solved
            mask = (strat > self._t_min) & (strat <= self._t_max)
            linr.fit(X[mask, :], (strat.T)[mask])
            self._models.append(linr)

    def predict(self, X):
        '''
        Predicts the time each strategy needs to solve the problem
        using the trained model

        Parameters
        ---------
        X : numpy array
            feature matrix          (problems x features)

        Returns
        -------
        result : numpy array
            with time estimates for each strategy (problems x strategies)
        '''
        prediction = np.zeros([len(self._models)])
        for i, model in enumerate(self._models):
            prediction[i] = model.predict(X)
        return prediction

    def score(self, X, Y):
        '''
        Predicts the time each strategy needs to solve the problem
        using the trained model

        Parameters
        ----------
        X : numpy array
            feature matrix          (problems x features)
        Y : numpy array
            target timing matrix    (problems x strategies)

        Returns
        -------
        result : list               (strategies)
            with scores for each strategy based on how well the model
            estimates the true time values (Y)
        '''
        score = []
        for i, model in enumerate(self._models):
            mask = (Y[:, i] > self._t_min) & (Y[:, i] <= self._t_max)
            score.append(model.score(X[mask], (Y[:, i])[mask]))
        return score
