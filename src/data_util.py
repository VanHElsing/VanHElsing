'''
Created on May 18, 2014

@author: Daniel Kuehlwein
'''

import numpy as np
from src.GlobalVars import LOGGER


def remove_unsolveable_problems(data_set):
    """
    Deletes all problems that cannot be solved.
    """
    problem_filter = np.max(data_set.strategy_matrix, axis=1) > -1
    ret = data_set.mask(problem_filter)
    LOGGER.info("Dataset removing unsolvable problems - prob x strats: %i x %i",
                len(ret.problems), len(ret.strategies))
    return ret


def not_solved_by_strat(data_set, s_index, s_time):
    """
    Returns a list of the indices of all problems are not solved
    by strategy s_index in s_time.
    """
    nr_of_problems = data_set.strategy_matrix.shape[0]
    s_m = data_set.strategy_matrix
    not_solved_by_strats = [i for i in range(nr_of_problems) if
                            (s_m[i, s_index] > s_time or s_m[i, s_index] == -1)]
    return not_solved_by_strats
