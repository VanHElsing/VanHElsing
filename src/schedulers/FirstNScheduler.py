'''
Created on May 17, 2014

@author: Sil van de Leemput
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
        if config == None:
            self._maxruntime = 300
            self._nstrats = 10
            self._random = False
        else:
            maxrt = float(config.get('FirstNScheduler', 'maxruntime'))
            self._maxruntime = maxrt
            self._nstrats = int(config.get('FirstNScheduler', 'n'))
            self._random = config.get('FirstNScheduler', 'n').lower() == 'true'
        self._timeslice = self._maxruntime / float(self._nstrats)
        self._count = 0
        self.strategies = None
        random.seed()
        pass


    def fit(self, data_set):
        self.strategies = data_set.strategies
        pass

    def predict(self, time_left):
        if (self._random):
            strategy = self.strategies[random.randint(0, len(self.strategies))]
        else:
            strategy = self.strategies[self._count]
        return strategy, min(time_left, self._timeslice)

    def set_problem(self, problem_file):
        self._count = 0
        pass

    def update(self):
        self._count += 1        
        pass