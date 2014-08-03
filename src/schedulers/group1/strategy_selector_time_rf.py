'''
A StrategySelector class based on multiple random forests
'''

from sklearn.ensemble import RandomForestClassifier
import numpy as np


class StrategySelectorTimeRF(object):
    '''
    A classifier that uses a combination of random forests. One random forest
    for each classifier.

    Attributes
    ----------
    `_classifiers` : list of random forests
        The collection of random forests for all strategies
    `_time` : double
        Maximum amount of time available for solving problems
    '''

    def __init__(self, time):
        '''
        Parameters
        ----------
        time : double
            Maximum amount of time available for solving problems
        '''
        self._classifiers = []
        self._time = time

    def _fit_classifiers(self, X, Y):
        '''
        Build the model from the training set (X, Y).

        Iterate through all strategies and fit a classifier to them

        Parameters
        ----------
        X : array-like of shape = [n_samples, n_features]
            The training input samples.

        Y : array-like, shape = [n_samples, n_strategies]
            The target values (integers that correspond to classes in
            classification, real numbers in regression).

        Returns
        -------
        classifiers : list of classifiers of shape = [n_strategies]
            Returns a list of the classifiers fitted to the strategies.
        '''
        Y = np.array(Y)
        temp = (Y > -1) & (Y <= self._time)
        classifiers = []
        for y in temp.T:
            clf = RandomForestClassifier()  # pylint: disable=no-value-for-parameter
            clf.fit(X, y)
            classifiers.append(clf)
        return classifiers

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
        self._classifiers = self._fit_classifiers(X, Y)

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
        y_pred = []
        for classifier in self._classifiers:
            y_pred.append(classifier.predict(X))
        return np.array(y_pred).T
