'''
Created on May 18, 2014

@author: Daniel Kuehlwein
'''

import numpy as np


def can_be_solved(data_set):
    """
    Returns a list of the indices of all problems that can be solved  
    """
    nr_of_problems = data_set.strategy_matrix.shape[0]
    s_m = data_set.strategy_matrix 
    solveable = [i for i in range(nr_of_problems) if (not max(s_m[i, :]) == -1)]
    return solveable


def delete_problems(data_set, good_problems):
    """
    Deletes all problems that are not 'good' from the dataset.
    By default, it deletes all problems that cannot be solved
    
    In:
    - dataset: See DataSet.py
    - good_problems: list of problems to keep
    """
    nr_of_strats = data_set.strategy_matrix.shape[1]
    nr_of_features = data_set.feature_matrix.shape[1]
    data_set.feature_matrix = data_set.feature_matrix[np.ix_(good_problems, range(nr_of_features))] 
    data_set.strategy_matrix = data_set.strategy_matrix[np.ix_(good_problems, range(nr_of_strats))]
    data_set.problems = data_set.problems[good_problems]
    return data_set


def not_solved_by_strat(data_set, s_index, s_time):
    """
    Returns a list of the indices of all problems are not solved by strategy s_index in s_time.  
    """
    nr_of_problems = data_set.strategy_matrix.shape[0]
    s_m = data_set.strategy_matrix 
    not_solved_by_strats = [i for i in range(nr_of_problems) if (s_m[i, s_index] >= s_time)]
    return not_solved_by_strats