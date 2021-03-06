'''
Contains the FirstNScheduler
'''

from src.schedulers.SchedulerTemplate import StrategyScheduler
import random


class FirstNScheduler(StrategyScheduler):
    '''
    Basic scheduler that just divides the total time in slices
    and returns the first N strategies (optionally at random)
    '''

    def __init__(self, config=None):
        StrategyScheduler.__init__(self, config)
        if config is None:
            self._nstrats = 10
            self._random = False
        else:
            self._nstrats = int(config.get('FirstNScheduler', 'n'))
            self._random = config.get('FirstNScheduler', 'n').lower() == 'true'
        self._count = self._timeslice = self._maxruntime = 0
        self.strategies = None
        random.seed()

    def fit(self, data_set, max_time):
        self.strategies = data_set.strategies
        self._maxruntime = max_time
        self._timeslice = max_time / float(self._nstrats)

    def predict(self, time_left):
        if self._random:
            strategy = self.strategies[random.randint(0, len(self.strategies))]
        else:
            strategy = self.strategies[self._count]
        return strategy, self._timeslice

    def set_problem_and_features(self, problem_file, dummy_features):
        self.set_problem(problem_file)

    def set_problem(self, problem_file):
        self._count = 0

    def update(self):
        self._count = (self._count + 1) % len(self.strategies)

    def reset(self):
        self._count = 0
