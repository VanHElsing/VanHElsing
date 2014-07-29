'''
Created on May 17, 2014

@author: Sil van de Leemput
'''

from sklearn.neighbors import KNeighborsClassifier 
import numpy as np


class StrategySelectorTimeKNN(object):
    """A random forest model

    A classifier that uses a combination of random forests. One random forest
    for each classifier.

    Attributes
    ----------
    `classifiers_` : list of random forests
        The collection of random forests for all strategies

    """

    def __init__(self, time, n_neighbors = 5):
        self.classifier_ = KNeighborsClassifier(n_neighbors= n_neighbors)
        self._time = time


    def fit(self, X, Y):
        """Build the model from the training set (X, y).

        Parameters
        ----------
        X : array-like of shape = [n_samples, n_features]
            The training input samples.

        y : array-like, shape = [n_samples, n_strategies]
            The target values (integers that correspond to classes in
            classification, real numbers in regression).

        Returns
        -------
        self : object
            Returns self.
        """
        temp = (Y > -1) & (Y <= self._time)
        self.classifier_.fit(X, temp)


    def predict(self, X):
        """Predict class for X.

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
        """
        return np.array(self.classifier_.predict(X))
