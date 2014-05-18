'''
Created on May 17, 2014

@author: Daniel Kuehlwein
'''

import numpy as np


def eval_against_dataset(dataset, scheduler, max_time=300):
    schedule_solved = 0.0
    problems_solvable = 0.0
    schedule_score = 0.0
    best_score = 0.0

    for p_index, problem in enumerate(dataset.problems):
        time_left = max_time
        p_features = dataset.feature_matrix[p_index, :]
        p_times = dataset.strategy_matrix[p_index, :]
        min_strat_time = np.ma.masked_equal(p_times, -1, copy=False).min()
        if min_strat_time < max_time:
            problems_solvable += 1
            best_score += (max_time - min_strat_time)
        scheduler.set_problem_and_features(problem, p_features)
        scheduler.reset()
        while time_left > 0:
            strat, pred_time = scheduler.predict(time_left)
            run_time = min(pred_time, time_left)
            time_left -= run_time
            strat_index = np.where(dataset.strategies == strat)[0][0]
            strat_time = dataset.strategy_matrix[p_index, strat_index]
            if strat_time > -1 and run_time >= strat_time:
                schedule_solved += 1
                schedule_score += (time_left + run_time - strat_time)                
                break   
            scheduler.update()
    return schedule_solved / problems_solvable, schedule_score / best_score
