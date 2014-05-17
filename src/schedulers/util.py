'''
Contains utility functions for schedulers

Created on May 15, 2014

@author: daniel
'''

import src.schedulers.BasicSchedulers as bs
from src.schedulers.FirstNScheduler import FirstNScheduler
from src.schedulers.SchedulerTemplate import StrategyScheduler
from src.IO import load_object, save_object


def load_scheduler(scheduler_file):
    scheduler = load_object(scheduler_file)
    if not isinstance(scheduler, StrategyScheduler):
        raise IOError(99, "file: {} is not of type StrategyScheduler"
                      .format(scheduler_file))
    return scheduler


def save_scheduler(scheduler, scheduler_file):
    if not isinstance(scheduler, StrategyScheduler):
        raise IOError(99, "Input object is not of type StrategyScheduler")
    save_object(scheduler, scheduler_file)
    return


def init_scheduler(problem, scheduler_file):
    scheduler = load_scheduler(scheduler_file)
    scheduler.set_problem(problem)
    return scheduler


def choose_scheduler(scheduler_id):
    if scheduler_id == 'EAuto':
        return bs.EAutoScheduler
    if scheduler_id == 'Single':
        return bs.SingleStrategyScheduler
    if scheduler_id == 'FirstN':
        return FirstNScheduler
    else:
        raise IOError(99, 'Unknown scheduler ID %s ' % scheduler_id)
