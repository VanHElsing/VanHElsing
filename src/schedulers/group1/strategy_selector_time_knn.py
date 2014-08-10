'''
A StrategySelector class based on a KNN model

Created on May 17, 2014

@author: Sil van de Leemput
'''

from sklearn.neighbors import KNeighborsClassifier
import numpy as np


class StrategySelectorTimeKNN(object):
    '''
    A strategy selector class based on a nearest neighbor model (KNN)

    Attributes
    ----------
    `_classifier` : KNN model
    `_time` : double
        Maximum amount of time available for solving problems
    '''

    def __init__(self, time, n_neighbors=5):
        '''
        Parameters
        ----------
        time : double
            Maximum amount of time available for solving problems
        n_neighbors : integer
            KNN model parameter, amount of neighbors considered
        '''
        self._classifier = KNeighborsClassifier(n_neighbors=n_neighbors)  # pylint: disable=unexpected-keyword-arg,no-value-for-parameter
        self._time = time

    def fit(self, X, Y):
        '''
        Build the model from the training set (X, Y).

        Parameters
        ----------
        X : array-like of shape = [n_samples, n_features]
            The training input samples.

        Y : array-like, shape = [n_samples, n_strategies]
            The target values (integers that correspond to classes in
            classification, real numbers in regression).

        Returns
        -------
        self : object
            Returns self.
        '''
        temp = (Y > -1) & (Y <= self._time)
        self._classifier.fit(X, temp)

    def predict(self, X):
        '''
        Predict class for X.

        Predicts all strategies based on the previously generated list of
        classifiers

        Parameters
        ----------
        X : array-like of shape = [n_samples, n_features]
            The input samples.

        Returns
        -------
        y : array of shape = [n_samples, n_strategies]
            The predicted classes.
        '''
        return np.array(self._classifier.predict(X))
