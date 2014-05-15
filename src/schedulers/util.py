'''
Contains utility functions for schedulers

Created on May 15, 2014

@author: daniel
'''

import src.schedulers.BasicSchedulers as bs


def load_scheduler(scheduler_file):
    raise NotImplementedError


def save_scheduler(scheduler, scheduler_file):
    raise NotImplementedError


def init_scheduler(problem, scheduler_file):
    scheduler = load_scheduler(scheduler_file)
    scheduler.set_problem(problem)
    return scheduler


def choose_scheduler(scheduler_id):
    if scheduler_id == 'EAuto':
        return bs.EAutoScheduler
    if scheduler_id == 'Single':
        return bs.SingleStrategyScheduler
    else:
        raise IOError(99, 'Unknown scheduler ID %s ' % scheduler_id)
