# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 15:19:17 2014

@author: Wouter Bulten

support vector regression
makkelijk vs moeilijk, mask over y < 10
"""
from sklearn import linear_model
from sklearn import ensemble
import numpy as np

class TimeRegression():
    """
        Trains a regression model for every search strategy
    """

    def __init__(self, esitmators=400, loss='lad', t_min=-1, t_max=300):
        """
            t_min: only data points with at least this value will be used
            t_max: only data points with a value below this will be used
        """
        self._models = []
        self._estimators = 400
        self._loss = loss
        self._t_min = t_min
        self._t_max = t_max

    def fit(self, X, y):

        # Reset model list
        self._models = []

        for i, strat in enumerate(y.T):
#             lr = linear_model.Ridge (alpha = self._alpha,
#                                      solver = self._solver,
#                                      fit_intercept = True,
#                                      normalize = True)
            params = {'n_estimators': self._estimators, 'max_depth': 4,
                      'min_samples_split': 2, 'learning_rate': 0.01,
                      'loss': self._loss, 'verbose': 0}
            lr = ensemble.GradientBoostingRegressor(**params)
            #Only use problems that can be solved
            mask = (strat > self._t_min) & (strat <= self._t_max)

            lr.fit(X[mask, :], (strat.T)[mask].A.ravel())

            self._models.append(lr)

    def predict(self, X):

        prediction = np.zeros([X.shape[0], len(self._models)])
        print prediction.shape

        for i, m in enumerate(self._models):
            prediction[:, i] = m.predict(X)

        return prediction

    def score(self, X, y):

        score = []

        for i, m in enumerate(self._models):

            mask = (y[:, i] > self._t_min) & (y[:, i] <= self._t_max)

            score.append(m.score(X[mask], (y[:, i])[mask]))

        return score

"""
Example use
"""
if __name__ == '__main__':

    close('all')
    from data_util import *
    from cross_validation_util import *
    from sklearn.metrics import r2_score

    # Read train data from file
    X, Y, problemNames, strategyNames = read_train_data('MLiP_train')

    nFolds = 4
    folds = create_fold(X, nFolds)


    currentFold = 1

    # Prune strategies
    stratprune = True
    if stratprune:
        stratfilter = [10, 21, 24, 35, 46, 48, 56, 63, 69, 72, 73, 75, 91, 101, 102, 107, 110, 111, 113, 120, 121, 125, 138, 152, 154, 155, 160, 170, 174, 176, 178, 185, 192, 197, 203, 208, 218, 221, 222, 229, 237, 238, 239, 242, 246, 251, 252, 258, 260, 264, 266, 267, 271, 272, 273, 275, 279, 280, 281, 282, 284, 285, 287, 293, 294, 297, 298, 302, 309, 311, 312, 316, 325, 328, 334, 338, 341, 342, 344, 347, 350, 351, 352, 353, 357, 359, 362, 369, 370, 372, 379, 381, 382, 384, 386, 387, 389, 390, 392, 393, 394, 395, 399, 404, 408, 411, 413, 414, 416, 419, 420, 430, 434, 440, 444, 448, 449, 451, 454, 478, 479, 480, 481, 483, 484, 485]
        Y = Y[:, stratfilter]
        #strategyNames = strategyNames[stratfilter]

    solvers = ['auto', 'svd', 'dense_cholesky', 'lsqr', 'sparse_cg']
    alphas = np.arange(10, 1000, 100)

    sum_score = np.zeros(len(alphas))
    sum_diff = np.zeros(len(alphas))
    means = np.zeros(Y.shape[1])

    for train, test in folds:

        x_train, y_train, x_test, y_test = X[train], Y[train], X[test], Y[test]

        # Loop through all possible values of alpha
        for i, a in enumerate(alphas):
            lm = TimeRegression(a)

            lm.fit(x_train, y_train)

            prediction = lm.predict(x_test)

            r2score = r2_score(y_test, prediction)
            mean_score = mean(lm.score(x_test, y_test))

            sum_score[i] += mean_score
            sum_diff[i] += mean(abs(prediction - y_test))

            # set all negative predictions to 0
            cappedPrediction = np.copy(prediction)
            cappedPrediction[prediction < 0] = 0

            means = means + np.mean(abs(np.asarray(prediction - y_test)), 0)

            print "Fold #{}".format(currentFold)
            print "\tMean diff {0}, total diff {1}".format(mean(abs(prediction - y_test)), sum(abs(prediction - y_test)))
            #print "\t(p) Mean diff {0}, total diff {1}".format(mean(abs(cappedPrediction - y_test)), sum(abs(cappedPrediction - y_test)))
            print "\tScore {1}, r^2 score {2}".format(mean(abs(prediction) - abs(y_test)), mean_score, r2score)

            currentFold += 1

    means /= (currentFold - 1)

    figure()
    plot(means)

    figure()
    plot(alphas, sum_score / nFolds)
    figure()
    plot(alphas, sum_diff / nFolds)
