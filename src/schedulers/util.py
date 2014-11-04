'''
Contains utility functions for schedulers
'''

import src.schedulers.BasicSchedulers as bs
from src.schedulers.FirstNScheduler import FirstNScheduler
from src.schedulers.NearestNeighbor import NearestNeighborScheduler
from src.schedulers.GreedyPlusScheduler import GreedyPlusScheduler
from src.schedulers.GreedyScheduler import GreedyScheduler
from src.schedulers.Group1Scheduler import Group1Scheduler
from src.schedulers.StaticScheduler import StaticScheduler
from src.schedulers.SchedulerTemplate import StrategyScheduler
from src.IO import load_object, save_object


def load_scheduler(scheduler_file):
    '''
    Loads a strategy scheduler from a file.
    '''
    scheduler = load_object(scheduler_file)
    if not isinstance(scheduler, StrategyScheduler):
        raise IOError(99, "file: {} is not of type StrategyScheduler"
                      .format(scheduler_file))
    return scheduler


def save_scheduler(scheduler, scheduler_file):
    '''
    Saves a strategy scheduler to a file.
    '''
    if not isinstance(scheduler, StrategyScheduler):
        raise IOError(99, "Input object is not of type StrategyScheduler")
    save_object(scheduler, scheduler_file)
    return


def init_scheduler(problem, scheduler_file):
    '''
    Loads a strategy scheduler from a file and initializes it to a problem.
    '''
    scheduler = load_scheduler(scheduler_file)
    scheduler.set_problem(problem)
    return scheduler


def choose_scheduler(scheduler_id):
    '''
    Switch for strategy schedulers.
    '''
    schedulers = {'EAuto': bs.EAutoScheduler,
                  'Single': bs.SingleStrategyScheduler,
                  'FirstN': FirstNScheduler,
                  'NN': NearestNeighborScheduler,
                  'Group1': Group1Scheduler,
                  'Greedy': GreedyScheduler,
                  'GreedyPlus': GreedyPlusScheduler,
                  'Static' : StaticScheduler
                 }
    try:
        return schedulers[scheduler_id]
    except KeyError:
        raise IOError(99, 'Unknown scheduler ID %s ' % scheduler_id)
