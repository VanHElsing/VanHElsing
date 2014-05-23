'''
GreedyNN combines the Greedy and the NN schedulers.
First, Greedy is run until the percentage of newly solved problems is lower
than a threshold. Afterwards, the normal NN is used.

Created on May 23, 2014

@author: Daniel Kuehlwein
'''

from src.GlobalVars import LOGGER
from src.schedulers.GreedyScheduler import GreedyScheduler
from src.schedulers.NearestNeighbor import NearestNeighborScheduler
from src.schedulers.SchedulerTemplate import StrategyScheduler


class GreedyPlusScheduler(StrategyScheduler):

    def __init__(self, config):
        # TODO: Read Runtime from config
        self.inititial_predictions = []
        self.plus_scheduler = NearestNeighborScheduler(config) # TODO: Cannot use util.choose_scheduler because of self - reference :/
        self.newly_solved_threshold = .05 # 5 % need to be solved
        self.greedy_run_time = 1.0
        self.data_set = None
        self.problem = None
        self.features = None
        self.config = config
        self.prediction_counter = 0

    def fit(self, data_set, max_time):
        self.data_set = data_set
        greedy_scheduler = GreedyScheduler(self.config)
        greedy_scheduler.fit(data_set, max_time)
        solved_enough = True
        while solved_enough:
            unsolved_problems = greedy_scheduler.data_set.strategy_matrix.shape[0]
            prediction = greedy_scheduler.predict(max_time, self.greedy_run_time)
            greedy_scheduler.update()
            new_problems_solved = float(unsolved_problems - greedy_scheduler.data_set.strategy_matrix.shape[0])
            if (new_problems_solved / unsolved_problems) < self.newly_solved_threshold:
                solved_enough = False
            self.inititial_predictions.append(prediction)
            self.data_set = greedy_scheduler.data_set
        LOGGER.info('Picked %s strategies for initial greedy run', len(self.inititial_predictions))
        LOGGER.info('Reduced the data set to %s', self.data_set.strategy_matrix.shape)
        self.plus_scheduler.fit(data_set, max_time)

    def predict(self, time_left):
        if self.prediction_counter < len(self.inititial_predictions):
            return self.inititial_predictions[self.prediction_counter]
        if self.prediction_counter == len(self.inititial_predictions):
            if self.features is None:
                self.plus_scheduler.set_problem(self.problem)
            else:
                self.plus_scheduler.set_problem_and_features(self.problem, self.features)
        return self.plus_scheduler.predict(time_left)

    def reset(self):
        self.prediction_counter = 0
        self.plus_scheduler.reset()

    def set_problem(self, problem_file):
        self.problem = problem_file

    def set_problem_and_features(self, problem_file, problem_features):
        self.problem = problem_file
        self.features = problem_features

    def update(self):
        if self.prediction_counter < len(self.inititial_predictions):
            self.prediction_counter += 1
            return
        self.plus_scheduler.update()
