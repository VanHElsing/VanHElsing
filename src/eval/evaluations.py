'''
Created on May 17, 2014

@author: Daniel Kuehlwein
'''

import numpy as np


def eval_against_dataset(dataset, scheduler, max_time=300):
    problems_solved = 0.0
    problems_solvable = 0.0

    for p_index, problem in enumerate(dataset.problems):
        p_time = max_time
        p_features = dataset.feature_matrix[p_index, :]
        p_times = dataset.strategy_matrix[p_index, :]
        min_strat_time = np.ma.masked_equal(p_times, -1, copy=False).min()
        if min_strat_time < max_time:
            problems_solvable += 1
        scheduler.set_problem_and_features(problem, p_features)
        while p_time > 0:
            strat, strat_time = scheduler.predict(p_time)
            run_time = min(strat_time, p_time)
            p_time -= run_time
            strat_index = np.where(dataset.strategies == strat)[0][0]
            strat_time = dataset.strategy_matrix[p_index, strat_index]
            if strat_time == -1:
                continue
            if run_time >= strat_time:
                problems_solved += 1
                break
    return problems_solved / problems_solvable
