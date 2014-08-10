'''
Module for scheduler machine learning evaluation

Created on May 17, 2014

@author: Daniel Kuehlwein, Wouter Geraedts
'''

import numpy as np
import os
import sys
import multiprocessing as mp
import ConfigParser
from argparse import ArgumentParser
from sklearn.cross_validation import KFold
# pylint: disable=R0913


def eval_against_dataset(dataset, scheduler, max_time=300, save_schedule_file='ml_eval'):
    '''
    Evaluates a scheduler against a dataset and appends results to a file

    Parameters
    ----------
    dataset : DataSet
        A dataset object containing problems to evaluate
    scheduler : Scheduler
        The scheduler to be used
    max_time : double
        The maximum time the scheduler can take for solving a problem
    save_schedule_file : String
        Filename for the output file

    Returns
    -------
    result : schedule_solved, schedule_score
        Amount of solved problems and score relative to the best score possible
    '''
    schedule_solved = 0.0
    schedule_score = 0.0
    best_score = 0.0

    if save_schedule_file is not None:
        # append mode, because we might be appending with Cross Validation
        out_stream = open(save_schedule_file, 'a+')

    for p_index, problem in enumerate(dataset.problems):
        time_left = max_time
        p_features = dataset.feature_matrix[p_index, :]
        p_times = dataset.strategy_matrix[p_index, :]
        min_strat_time = np.ma.masked_equal(p_times, -1, copy=False).min()

        # Only consider solvable problems
        if min_strat_time >= max_time or str(min_strat_time) == '--':
            continue

        best_score += (max_time - min_strat_time)

        scheduler.set_problem_and_features(problem, p_features)
        scheduler.reset()

        while time_left > 0:
            strat, pred_time = scheduler.predict(time_left)
            run_time = min(pred_time, time_left)
            strat_index = np.where(dataset.strategies == strat)[0][0]
            strat_time = dataset.strategy_matrix[p_index, strat_index]

            if strat_time > -1 and run_time >= strat_time:
                schedule_solved += 1
                schedule_score += (time_left - strat_time)

                if save_schedule_file is not None:
                    used_time = max_time - time_left + strat_time
                    out_stream.write('%s,%s\n' % (problem, str(used_time)))

                break

            time_left -= run_time
            scheduler.update()

    if save_schedule_file is not None:
        out_stream.close()

    return schedule_solved, schedule_score / best_score


def ml_cv_eval(configuration, dataset, folds, max_time=300, save_schedule_file='ml_eval'):
    '''
    Evaluates a scheduler against a dataset using cross-validation

    Parameters
    ----------
    configuration : String
        Filename of the configuration file for the scheduler settings
    dataset : DataSet
        A dataset object containing problems to evaluate
    folds : list [kfolds x problems]
        List of masks with indices for each problem
    max_time : double
        The maximum time the scheduler can take for solving a problem
    save_schedule_file : String
        Filename for the output file
    
    Returns
    -------
    result : sumsolved, avgscore
        Amount of solved problems and score relative to the best score possible,
        averaged over all the folds.
    '''
    scheduler_id = configuration.get('Learner', 'scheduler')

    scheduler_class = choose_scheduler(scheduler_id)
    scheduler = scheduler_class(configuration)

    LOGGER.info("TRAINING + PREDICTION (Cross-validation folds %i)", len(folds))
    sumsolved = 0
    sumscore = 0
    for i, (train_idx, test_idx) in enumerate(folds):
        train_dataset = dataset.mask(train_idx)
        test_dataset = dataset.mask(test_idx)

        LOGGER.info("Fold: %i -- #train: %i/%i",
                    i + 1, len(train_dataset.problems),
                    len(dataset.problems))

        LOGGER.info("Fitting model.")
        scheduler.fit(train_dataset, max_time)

        LOGGER.info("Evaluating model.")
        solved, score = eval_against_dataset(test_dataset, scheduler, max_time, save_schedule_file)

        try:
            sumsolved += solved
            sumscore += score
        except TypeError:
            LOGGER.warn("Evaluation score is not a number.")
            solved = 0

        LOGGER.info("Solved: {}".format(solved))
        
    avgscore = sumscore / len(folds)
    LOGGER.info("Average score: {}".format(avgscore))
    
    return sumsolved, avgscore


def ml_cv_eval_async(args):
    '''
    Evaluates a scheduler against a dataset and appends results to a file using cross-validation
    this specific function is suitable for running cross validation for multiple configurations
    divided over multiple processor cores

    Parameters
    ----------
    args : (env=(dataset, folds), config=(neighbors, max_time, negscore_func))
        Composite arguments tuple of triplets

    dataset : DataSet
        A dataset object containing problems to evaluate
    folds : list [kfolds x problems]
        List of masks with indices for each problem

    neighbors : integer
        amount of neighbors to use for NearestNeighborScheduler
    max_time : double
        The maximum time the scheduler can take for solving a problem
    negscore_func : String
        NearestNeighborScheduler classifier parameter
    '''
    env, config = args

    # unpack environment and configuration
    dataset, folds = env
    neighbors, max_time, negscore_func = config

    configuration = ConfigParser.SafeConfigParser()
    configuration.add_section('Learner')
    configuration.set('Learner', 'scheduler', 'NN')
    configuration.set('Learner', 'min_neighbors', str(neighbors))
    configuration.set('Learner', 'negscore_func', negscore_func)

    configuration.add_section('ATP Settings')
    configuration.set('ATP Settings', 'features', 'E')

    result_file = 'CV' + str(len(folds)) + '_NN' + negscore_func + str(neighbors) + "_" + str(max_time)
    schedule_path = os.path.join(PATH, 'runs', 'theory', 'E', result_file)

    if os.path.isfile(schedule_path):
        os.remove(schedule_path)

    ml_cv_eval(configuration, dataset, folds, max_time, schedule_path)


def set_up_parser():
    '''
    Initializes parser.
    '''
    parser = ArgumentParser(description='Run cross-validation for multiple Scheduler configurations.\n')
    parser.add_argument('-d', '--dataset',
                        help='The dataset file to fit and evaluate the Schedulers on.',
                        default=None)
    return parser
    

def main(argv):
    '''
    Initiates cross-validation tests over several processor cores.
    The tests are only for specific NearestNeighborSchedulers, code should be
    added or changed when executing different tests.
    '''
    parser = set_up_parser()
    args = parser.parse_args(argv)

    kfolds = 4
    configs = [
        (1, 300, 'mean'), (2, 300, 'mean'), (5, 300, 'mean'),
        (1, 300, 'meanmedian'), (2, 300, 'meanmedian'), (5, 300, 'meanmedian'), (10, 300, 'meanmedian')
    ]

    # Load dataset
    if args.dataset is None:
        print "Error: please set the datafile commandline parameter. (See -h)"
        return 1
    
    dataset = load_dataset_from_file(args.dataset)
    folds = KFold(len(dataset.problems), n_folds=kfolds, indices=False)  # pylint: disable=unexpected-keyword-arg, no-value-for-parameter

    env = (dataset, folds)
    args = [(env, x) for x in configs]

    # Run jobs async
    pool = mp.Pool()

    pool.map_async(ml_cv_eval_async, args)
    pool.close()
    pool.join()

    return 0


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.data_util import load_dataset_from_file
    from src.schedulers.util import choose_scheduler
    from src.GlobalVars import PATH, LOGGER
    sys.exit(main(sys.argv[1:]))
