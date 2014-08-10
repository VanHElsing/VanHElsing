'''
StrategySolvableInTimeRF
Optimization classifier class that predicts if a problem is solvable
within a given period of time
'''

import numpy as np
import sklearn.ensemble as ens
# pylint: disable=C0103


class StrategySolvableInTimeRF(object):
    '''
    Optimization classifier, that predicts if a problem is solvable
    in t time. Uses RF and bagging.

    Attributes
    ----------
    `_bag_rounds` : integer
            Amount of random forests to use. Each random forests classifier
            uses a new bootstrapped population.
    `_time` : double
        Maximum amount of time available for solving problems
    `_logits` : list of random forest classifiers, shape = [_bag_rounds]
        List for storing the random forest classifiers
    '''

    def __init__(self, time=10, bag_rounds=10):
        '''
        Parameters
        ----------
        time : double
            Maximum amount of time available for solving problems
        bag_rounds : integer
            Amount of random forests to use. Each random forests classifier
            uses a new bootstrapped population.
        '''
        # time constraint
        self._time = time
        # rounds of bagging
        self._bag_rounds = bag_rounds
        self._logits = None

    def fit(self, X, Y):
        '''
        Build the model from the training set (X, y).

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
        '''
        unsolvemask = (Y == -1)
        Y = Y * np.invert(unsolvemask) + unsolvemask * 2 * self._time
        y = np.min(Y, axis=1) > self._time
        # hardFilter = np.array([np.min(y[y!=-1]) > self._time for y in Y])
        # y = np.array(hardFilter)

        N = X.shape[0]

        # Fit model using bootstrap aggregation (bagging):
        y = np.mat(y).T

        # Weights for selecting samples in each bootstrap
        weights = np.ones((N, 1), dtype=float) / N

        # Storage of trained log.reg. classifiers fitted in each bootstrap
        self._logits = [0] * self._bag_rounds

        # For each round of bagging
        for i in range(self._bag_rounds):

            # Extract training set by random sampling with replacement
            # from X and y
            x_train, y_train = bootstrap(X, y, N, weights)

            # Fit logistic regression model to training data and save result
            forest_classifier = ens.RandomForestClassifier()
            forest_classifier.fit(x_train, y_train.A.ravel())
            self._logits[i] = forest_classifier

    def predict(self, X):
        '''
        Predict class for X.

        The predicted class depends on the model

        Parameters
        ----------
        X : array-like of shape = [1, n_features]
            The input samples.

        Returns
        -------
        y : array of shape = [1, n_strategies]
            The predicted classes.
        '''
        votes = np.zeros((1, 1))
        for i in range(self._bag_rounds):
            y = np.array(self._logits[i].predict(X)).T
            votes = votes + y
        return np.array((votes > (self._bag_rounds / 2)).T)[0]


def bootstrap(X, y, N, weights='auto'):
    '''
    function: X_bs, y_bs = bootstrap(X, y, N, weights)
    The function extracts the bootstrap set from given matrices X and y.
    The distribution of samples is determined by weights parameter
    (default: 'auto', equal weights).

    Usage
    -----
    X_bs, y_bs = bootstrap(X, y, N, weights)

    Parameters
    ----------
    X       : Estimated probability of class 1. (Between 0 and 1.)
    y       : True class indices. (Equal to 0 or 1.)
    N       : number of samples to be drawn
    weights : probability of occurence of samples (default: equal)

    Returns
    -------
    X_bs : Matrix with rows drawn randomly from X wrt given distribution
    y_bs : Matrix with rows drawn randomly from y wrt given distribution
    '''
    if weights == 'auto':
        weights = np.ones((X.shape[0], 1), dtype=float) / X.shape[0]
    else:
        weights = np.array(weights, dtype=float)
        weights = (weights / weights.sum()).ravel().tolist()
    bnc = np.random.multinomial(N, weights, 1).ravel()
    selected_indices = []
    while bnc.sum() > 0:
        selected_indices += np.where(bnc > 0)[0].tolist()
        bnc[bnc > 0] -= 1
    np.random.shuffle(selected_indices)
    return X[selected_indices, :], y[selected_indices, :]
