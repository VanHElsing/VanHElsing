'''
Created on May 17, 2014

@author: Sil van de Leemput
'''

import numpy as np

from src.GlobalVars import LOGGER
from src.schedulers.SchedulerTemplate import StrategyScheduler
import src.Preprocessing as pp


# TODO import right classifiers
from src.schedulers.group1.strategy_selector_time_rf import StrategySelectorTimeRF
from src.schedulers.group1.timeregression_boost import TimeRegression as TimeRegressionBoost
from src.schedulers.group1.timeregression import TimeRegression
from src.schedulers.group1.strategy_solvable_in_time_rf import StrategySolvableInTimeRF


class Group1Scheduler(StrategyScheduler):
    '''
    Scheduler designed by Group1
    '''

    def __init__(self, config=None):
        StrategyScheduler.__init__(self, config)
        self._config = config

        self._pcas = map(int, list(self.cfg_get('pcas').split()))
        self._standardize = self.cfg_get('standardize', True)
        self._stdcap = float(self.cfg_get('stdcap'))

        self._alpha = float(self.cfg_get('alpha'))
        self._beta = float(self.cfg_get('beta'))
        self._gamma = float(self.cfg_get('gamma'))
        self._delta = float(self.cfg_get('delta'))
        self._tmultiplier = float(self.cfg_get('tmultiplier'))
        self._tadder = float(self.cfg_get('tadder'))
        self._use_optimizer = self.cfg_get('toptimizer', True)
        self._opt_t = float(self.cfg_get('topt'))
        self._boosting = self.cfg_get('boosting', True)

        self._log = self.cfg_get('log', True)
        self._max_time = 0

        self._stratselector = None
        self._strattimereg = None
        self._stratsolvesint = None

    def cfg_get(self, prop, boolean=False):
        if boolean:
            return self._config.get("Group1Scheduler", prop).lower() == "true"
        return self._config.get("Group1Scheduler", prop)

    def fit(self, data_set, max_time):

        X = data_set.feature_matrix
        Y = data_set.strategy_matrix
        self._stratnames = data_set.strategies
        self._max_time = max_time

        # PREPROCESSING
        if self._log:
            LOGGER.info("PREPROCESS features")
        # sanitize features - standardization
        if self._standardize:
            LOGGER.info("standardization")
            X, self._means, self._stds = pp.standardizeFeatures(X, True, self._stdcap)
        # apply PCAs
        if len(self._pcas) > 0:
            LOGGER.info("applying PCAs")
        self._pca_V = pp.determinePCA(X)
        X = pp.addPCAFeatures(X, self._pca_V, self._pcas)

        # fit models
        if self._log:
            LOGGER.info("Fit selection")
        self._stratselector = StrategySelectorTimeRF(self._max_time)
        self._stratselector.fit(X, Y)
        if self._log:
            LOGGER.info("Fit regression")
        if self._boosting:
            self._strattimereg = TimeRegressionBoost()
        else:
            self._strattimereg = TimeRegression()
        self._strattimereg.fit(X, Y)
        if self._use_optimizer:
            if self._log:
                LOGGER.info("Fit optimizer")
            self._stratsolvesint = StrategySolvableInTimeRF(t=self._opt_t)
            self._stratsolvesint.fit(X, Y)
        if self._log:
            LOGGER.info("Calculate statistics")

        # precalculate statistics that are used for calculating
        # the scheduling order
        self._Ypred = np.array((self._stratselector.predict(X) > 0))
        self._Y = Y
        self._CoverMat = (self._Y > -1)
        Ytemp = self._Y * self._CoverMat + np.invert(self._CoverMat) * self._max_time * 2
        self._mins = np.min(Ytemp, axis=0)
        self._maxs = np.max(self._Y, axis=0)

    def set_problem(self, problem_file):
        # TODO calculate problem_file features
        features = self.feature_parser.get(problem_file)
        self.set_problem_and_features(problem_file, features)

    def set_problem_and_features(self, problem_file, features):
        # Convert np.array to [1 x features] dims
        x = np.zeros((1, len(features)))
        x[0, :] = features

        if self._standardize:
            x = pp.standardizeFeaturesWithMeansStds(x, self._means, self._stds,
                                                    True, self._stdcap)
        x = pp.addPCAFeatures(x, self._pca_V, self._pcas)

        ys = self._stratselector.predict(x)[0, :]
        if self._use_optimizer:
            yo = self._stratsolvesint.predict(x)
        else:
            yo = 0
        yt = self._strattimereg.predict(x)
        #print yt.shape, ys.shape, x.shape, yo
        # PREPROCESS time regression values fit them between values
        yt = self.__processRegressionVector(yt, yo)

        self._regtimes = (np.ones((len(yt))) - (yt / float(self._max_time)))
        self._cover = self._CoverMat & (self._Y <= yt)
        self._probs = self._Ypred & self._cover
        self._weightconst = self._regtimes * self._gamma + ys * self._delta + 10
        self._yt = yt

        # administration vars for looping
        self._stratsleft = np.ones((yt.shape[0]))

    def __processRegressionVector(self, Yt, yo):
        Ytsmaller = Yt < self._opt_t
        # if it is a hard problem (yo) and regression value is below
        # threshold set it to threshold
        if self._use_optimizer:
            Targets = (Ytsmaller.T & yo).T
            Yt = Yt * np.invert(Targets) + self._opt_t * Targets

        # clamp and fix all predicted t values to sensible times
        # get time from regression prediction and multiply it so that it
        # overestimates a little
        Yt = np.maximum(Yt, np.maximum(self._mins, 0)) * self._tmultiplier + np.ones(Yt.shape) * self._tadder
        Yt = np.minimum(Yt, np.minimum(self._maxs, self._max_time))

        # if self._use_optimizer and not yo and t > 10: # original
        # with t > 10 opt10diff without opt10
        # if it is an easy problem and time is higher than threshold
        # set to threshold
        if self._use_optimizer:
            Targets = (np.invert(Ytsmaller).T & np.invert(yo)).T
            Yt = Yt * np.invert(Targets) + self._opt_t * Targets
        return Yt

    def predict(self, time_left):
        # while time_left > 0 and np.sum(self._stratsleft) > 0:
        # calculate COVERAGE VECTOR - percentage of problems covered
        # by the current strategies
        yc = np.sum(self._cover, axis=0) / float(self._cover.shape[0])
        # calculate PROB VECTOR - probs that a strategy within the strategy
        # selector predicts the problem correctly given the pruned problems
        # & predictions
        probs = np.sum(self._probs, axis=0) / float(self._probs.shape[0])

        # calculate weights (should always be values > 0)
        weights = probs * self._alpha + yc * self._beta + self._weightconst

        # set weight of done strats to 0
        weights = weights * self._stratsleft

        # select the strategy with the highest weight
        self._sel = np.argmax(weights)

        # Update administration and schedule
        time = self._yt[self._sel]

        strategy = self._stratnames[self._sel]
        return strategy, time

    def update(self):
        sel = self._sel
        # Prune solved/covered problems
        mask = np.invert(self._cover[:, sel])
        self._cover = self._cover[mask, :]
        self._probs = self._probs[mask, :]
        # Prune used strat
        self._stratsleft[sel] = 0

    def reset(self):
        pass
