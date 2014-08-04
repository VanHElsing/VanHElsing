'''
Contains the GreedyPlus scheduler, a mixture of Greedy and NN.
'''

from src.GlobalVars import LOGGER
from src.schedulers.GreedyScheduler import GreedyScheduler
from src.schedulers.NearestNeighbor import NearestNeighborScheduler
from src.schedulers.SchedulerTemplate import StrategyScheduler
# pylint: disable=R0902


class GreedyPlusScheduler(StrategyScheduler):
    '''
    GreedyNN combines the Greedy and the NN schedulers.
    First, Greedy is run until the percentage of newly solved problems is lower
    than a threshold. Afterwards, the normal NN is used.
    '''
    def __init__(self, config):
        StrategyScheduler.__init__(self, config)
        # IMPROVEMENT: Read Runtime from config
        self.inititial_predictions = []
        self.plus_scheduler = NearestNeighborScheduler(config)
        self.newly_solved_threshold = .05  # 5 % need to be solved
        self.greedy_run_time = 0.5
        self.problem = None
        self.features = None
        self.config = config
        self.prediction_counter = 0

    def fit(self, data_set, max_time):
        '''
        Fits the model to a certain dataset with a certain maximum amount
        of time that can be used for solving problems

        Parameters
        ----------
        data_set : DataSet
            The dataset that the scheduler has to be fitted to
        max_time : int
            The total amount of time that can be used to solve problems
        '''
        greedy_scheduler = GreedyScheduler(self.config)
        greedy_scheduler.fit(data_set, max_time)
        while True:
            problem_nr = greedy_scheduler.data_set.strategy_matrix.shape[0]
            prediction = greedy_scheduler.predict(max_time,
                                                  self.greedy_run_time)
            greedy_scheduler.update()
            new_problems_solved = problem_nr - greedy_scheduler.data_set.strategy_matrix.shape[0]  # NOQA, pylint: disable=C0301
            self.inititial_predictions.append(prediction)
            # i += 1
            solved_ratio = new_problems_solved / float(problem_nr)
            if solved_ratio < self.newly_solved_threshold:
                break
        data_set = greedy_scheduler.data_set
        LOGGER.info('Picked %s strategies for initial greedy run',
                    len(self.inititial_predictions))
        LOGGER.info('Reduced the data set to %s',
                    data_set.strategy_matrix.shape)
        self.plus_scheduler.fit(data_set, max_time)

    def predict(self, time_left):
        '''
        Predicts the current problem based on a certain amount of time left
        
        Parameters
        ----------
        time_left : int
            The amount of time that is left for solving problems
        '''
        if self.prediction_counter < len(self.inititial_predictions):
            return self.inititial_predictions[self.prediction_counter]
        if self.prediction_counter == len(self.inititial_predictions):
            if self.features is None:
                self.plus_scheduler.set_problem(self.problem)
            else:
                self.plus_scheduler.set_problem_and_features(self.problem,
                                                             self.features)
        return self.plus_scheduler.predict(time_left)

    def reset(self):
        '''
        Resets the prediction counter and the plus scheduler
        '''
        self.prediction_counter = 0
        self.plus_scheduler.reset()

    def set_problem(self, problem_file):
        '''
        Changes the problem to a specific problem that will be solved

        Parameters
        ----------
        problem_file : string
            The new problem that should be solved
        '''
        self.problem = problem_file

    def set_problem_and_features(self, problem_file, problem_features):
        '''
        Changes the problem to a specific problem and its features that will be solved

        Parameters
        ----------
        problem_file : string
            The new problem that should be solved
        self.problem_features : Numpy array
            The features of the new problems
        '''
        self.problem = problem_file
        self.features = problem_features

    def update(self):
        '''
        Updates the prediction counter by one
        '''
        if self.prediction_counter < len(self.inititial_predictions):
            self.prediction_counter += 1
            return
        self.plus_scheduler.update()
