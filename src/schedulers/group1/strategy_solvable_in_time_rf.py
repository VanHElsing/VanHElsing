"""
StrategySolvableInTimeRF
Optimization classifier class that predicts if a problem is solvable
within a given period of time

@author: Sil van de Leemput
"""

import numpy as np

from src.schedulers.group1.bin_classifier_ensemble import BinClassifierEnsemble
from sklearn.linear_model import LogisticRegression
import sklearn.ensemble as ens


class StrategySolvableInTimeRF(object):
    """Optimization classifier, that predicts if a problem is solvable
    in t time.
    Uses RF and bagging
    """
    def __init__(self, t=10, L=10):
        # time constraint
        self._t = t
        # rounds of bagging
        self._L = L
        pass

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
        unsolvemask = (Y == -1)
        Y = Y * np.invert(unsolvemask) + unsolvemask * 2 * self._t
        y = np.min(Y, axis=1) > self._t
        # hardFilter = np.array([np.min(y[y!=-1]) > self._t for y in Y])
        # y = np.array(hardFilter)

        N, M = X.shape

        # Fit model using bootstrap aggregation (bagging):
        y = np.mat(y).T

        # Number of rounds of bagging
        self._L = 10

        # Weights for selecting samples in each bootstrap
        weights = np.ones((N, 1), dtype=float) / N

        # Storage of trained log.reg. classifiers fitted in each bootstrap
        self._logits = [0] * self._L

        # For each round of bagging
        for l in range(self._L):

            # Extract training set by random sampling with replacement
            # from X and y
            X_train, y_train = self.bootstrap(X, y, N, weights)

            # Fit logistic regression model to training data and save result
            forest_classifier = ens.RandomForestClassifier()
            forest_classifier.fit(X_train, y_train.A.ravel())
            self._logits[l] = forest_classifier
        pass

    def predict(self, X):
        """Predict class for X.

        The predicted class depends on the model

        Parameters
        ----------
        X : array-like of shape = [n_samples, n_features]
            The input samples.

        Returns
        -------
        y : array of shape = [n_samples, n_strategies]
            The predicted classes.
        """
        N = 1  # X.shape[0]
        votes = np.zeros((N, 1))
        for l in range(self._L):
            y = np.array(self._logits[l].predict(X)).T
            votes = votes + y
        return np.array((votes > (self._L / 2)).T)[0]

    def bootstrap(self, X, y, N, weights='auto'):
        '''
        function: X_bs, y_bs = bootstrap(X, y, N, weights)
        The function extracts the bootstrap set from given matrices X and y.
        The distribution of samples is determined by weights parameter
        (default: 'auto', equal weights).

        Usage:
            X_bs, y_bs = bootstrap(X, y, N, weights)

         Input:
             X: Estimated probability of class 1. (Between 0 and 1.)
             y: True class indices. (Equal to 0 or 1.)
             N: number of samples to be drawn
             weights: probability of occurence of samples (default: equal)

        Output:
            X_bs: Matrix with rows drawn randomly from X wrt given distribution
            y_bs: Matrix with rows drawn randomly from y wrt given distribution
        '''
        if weights == 'auto':
            weights = np.ones((X.shape[0], 1), dtype=float) / X.shape[0]
        else:
            weights = np.array(weights, dtype=float)
            weights = (weights / weights.sum()).ravel().tolist()
        bc = np.random.multinomial(N, weights, 1).ravel()
        selected_indices = []
        while bc.sum() > 0:
            selected_indices += np.where(bc > 0)[0].tolist()
            bc[bc > 0] -= 1
        np.random.shuffle(selected_indices)
        return X[selected_indices, :], y[selected_indices, :]
