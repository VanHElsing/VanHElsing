'''
Strategy Scheduler based on the work of the Group1 student project.
'''

import numpy as np

from src.GlobalVars import LOGGER
from src.schedulers.SchedulerTemplate import StrategyScheduler
import src.schedulers.group1.preprocessing as pp
from src.schedulers.group1.strategy_selector_time_knn \
    import StrategySelectorTimeKNN as StrategySelector
from src.schedulers.group1.timeregression import TimeRegression
from src.schedulers.group1.strategy_solvable_in_time_rf \
    import StrategySolvableInTimeRF


class Group1Scheduler(StrategyScheduler):
    '''
    Scheduler designed by Group1
    '''

    def __init__(self, config=None):
        '''
        Constructor - loads settings from config object
        The config should have a "Group1Scheduler" group
        '''
        StrategyScheduler.__init__(self, config)
        self._config = config

        self._pcas = [int(i) for i in config.get('Group1Scheduler', 'pcas').split()]
        self._standardize = config.getboolean('Group1Scheduler', 'standardize')
        self._stdcap = float(config.getfloat('Group1Scheduler', 'stdcap'))

        self._alpha = float(config.getfloat('Group1Scheduler', 'alpha'))
        self._beta = float(config.getfloat('Group1Scheduler', 'beta'))
        self._gamma = float(config.getfloat('Group1Scheduler', 'gamma'))
        self._delta = float(config.getfloat('Group1Scheduler', 'delta'))
        self._tmultiplier = float(config.getfloat('Group1Scheduler', 'tmultiplier'))
        self._tadder = float(config.getfloat('Group1Scheduler', 'tadder'))
        self._use_optimizer = config.getboolean('Group1Scheduler', 'toptimizer')
        self._opt_t = float(config.getfloat('Group1Scheduler', 'topt'))

        self._log = config.getboolean('Group1Scheduler', 'log')
        self._max_time = 0

        self._stratselector = None
        self._strattimereg = None
        self._stratsolvesint = None

        self._stratnames = None
        self._Y = None
        self._mat_pred = None
        self._mat_cover = None
        self._stds = None
        self._means = None
        self._V = None
        self._mins = None
        self._maxs = None

        self._stratsleft = None
        self._regtimes = None
        self._weightconst = None
        self._probs = None
        self._sel = None
        self._yt = None
        self._cover = None

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
            X, self._means, self._stds = pp.standardize_features(X, True,
                                                                 self._stdcap)
        # apply PCAs
        if len(self._pcas) > 0:
            LOGGER.info("applying PCAs")
            self._V = pp.determine_pca(X)
            X = pp.add_pca_features(X, self._V, self._pcas)

        # fit models
        if self._log:
            LOGGER.info("Fit selection")
        self._stratselector = StrategySelector(self._max_time)
        self._stratselector.fit(X, Y)
        if self._log:
            LOGGER.info("Fit regression")
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
        self._mat_pred = np.array((self._stratselector.predict(X) > 0))
        self._Y = Y
        self._mat_cover = (self._Y > -1)
        temp = self._Y * self._mat_cover
        temp = temp + np.invert(self._mat_cover) * self._max_time * 2
        self._mins = np.min(temp, axis=0)
        self._maxs = np.max(self._Y, axis=0)

    def set_problem(self, problem_file):
        features = self.feature_parser.get(problem_file)
        self.set_problem_and_features(problem_file, features)

    def set_problem_and_features(self, problem_file, features):
        # Convert np.array to [1 x features] dims
        x = np.zeros((1, len(features)))
        x[0, :] = features

        if self._standardize:
            x = pp.standardize_features_means_stds(x, self._means, self._stds,
                                                   True, self._stdcap)
        if len(self._pcas) > 0:
            x = pp.add_pca_features(x, self._V, self._pcas)

        ys = self._stratselector.predict(x)[0, :]
        if self._use_optimizer:
            yo = self._stratsolvesint.predict(x)
        else:
            yo = 0
        yt = self._strattimereg.predict(x)

        # PREPROCESS time regression values fit them between values
        yt = self.__process_regression_vector(yt, yo)

        self._regtimes = (np.ones((len(yt))) - (yt / float(self._max_time)))
        self._cover = self._mat_cover & (self._Y <= yt)
        self._probs = self._mat_pred & self._cover
        self._weightconst = self._regtimes * self._gamma + ys * self._delta + 10
        self._yt = yt

        # administration vars for looping
        self._stratsleft = np.ones((yt.shape[0]))

    def __process_regression_vector(self, Yt, yo):
        '''
        This function preprocesses the regression vector Yt based on
        optimization estimates from yo. If yo predicts the problem to
        be hard, times are at least higher than _opt_t otherwise the
        values cannot be higher than _opt_t

        Variables
        ---------
        Yt : numpy array (problems x strats)
            Regression vector for the problems
        yo : numpy array (problems)
            Boolean vector if the problem is a hard problem

        Returns
        -------
        Yt' : numpy array (problems x strats)
            Modified regression vector with more sensible values
        '''
        temp = Yt < self._opt_t
        # if it is a hard problem (yo) and regression value is below
        # threshold set it to threshold
        if self._use_optimizer:
            targets = (temp.T & yo).T
            Yt = Yt * np.invert(targets) + self._opt_t * targets

        # clamp and fix all predicted t values to sensible times
        # get time from regression prediction and multiply it so that it
        # overestimates a little
        Yt = np.maximum(Yt, np.maximum(self._mins, 0))
        Yt = Yt * self._tmultiplier + np.ones(Yt.shape) * self._tadder
        Yt = np.minimum(Yt, np.minimum(self._maxs, self._max_time))

        # if self._use_optimizer and not yo and t > 10: # original
        # with t > 10 opt10diff without opt10
        # if it is an easy problem and time is higher than threshold
        # set to threshold
        if self._use_optimizer:
            targets = (np.invert(temp).T & np.invert(yo)).T
            Yt = Yt * np.invert(targets) + self._opt_t * targets
        return Yt

    def predict(self, time_left):
        # while time_left > 0 and np.sum(self._stratsleft) > 0:
        # calculate COVERAGE VECTOR - percentage of problems covered
        # by the current strategies
        ycover = np.sum(self._cover, axis=0) / float(self._cover.shape[0])
        # calculate PROB VECTOR - probs that a strategy within the strategy
        # selector predicts the problem correctly given the pruned problems
        # & predictions
        probs = np.sum(self._probs, axis=0) / float(self._probs.shape[0])

        # calculate weights (should always be values > 0)
        weights = probs * self._alpha + ycover * self._beta + self._weightconst

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
        pass  # TODO: At least print a warning. All ML evals will fail.
