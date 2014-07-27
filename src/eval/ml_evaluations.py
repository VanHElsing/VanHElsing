import numpy as np
import os
import sys
import multiprocessing as mp
import ConfigParser
from src.data_util import load_dataset_from_config
from src.schedulers.util import choose_scheduler
from sklearn.cross_validation import KFold
from src.GlobalVars import PATH, LOGGER


def eval_against_dataset(dataset, scheduler, max_time=300, save_schedule_file='ml_eval'):
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


def ml_cv_eval(configuration, dataset, kfolds, folds, max_time=300, save_schedule_file='ml_eval'):
    scheduler_id = configuration.get('Learner', 'scheduler')
    
    scheduler_class = choose_scheduler(scheduler_id)
    scheduler = scheduler_class(configuration)

    LOGGER.info("TRAINING + PREDICTION (Cross-validation folds %i)", kfolds)
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
        solved, _score = eval_against_dataset(test_dataset, scheduler, max_time, save_schedule_file)
        
        try:
            sumscore += solved
        except TypeError:
            LOGGER.warn("Evaluation score is not a number.")
            solved = 0
        
        LOGGER.info("Solved: {}".format(solved))
    LOGGER.info("Total score: {}".format(sumscore / kfolds))


def ml_cv_eval_async(args):
    env, config = args
    
    # unpack environment and configuration
    dataset, kfolds, folds = env
    neighbors, max_time, negscore_func = config
    
    configuration = ConfigParser.SafeConfigParser()
    configuration.add_section('Learner')
    configuration.set('Learner', 'scheduler', 'NN')
    configuration.set('Learner', 'min_neighbors', str(neighbors))
    configuration.set('Learner', 'negscore_func', negscore_func)
    configuration.set('Learner', 'datasetfile', '/home/wgeraedts/tmp/train_solvable.data')
    
    configuration.add_section('ATP Settings')
    configuration.set('ATP Settings', 'features', 'E')
    
    result_file = 'CV' + str(kfolds) + '_NN' + negscore_func + str(neighbors) + "_" + str(max_time)
    schedule_path = os.path.join(PATH, 'runs', 'theory', 'E', result_file)
    
    if os.path.isfile(schedule_path):
        os.remove(schedule_path)
        
    ml_cv_eval(configuration, dataset, kfolds, folds, max_time, schedule_path)


def main():
    kfolds = 4
    configs = [
        (1, 300, 'mean'), (2, 300, 'mean'), (5, 300, 'mean'),
        (1, 300, 'meanmedian'), (2, 300, 'meanmedian'), (5, 300, 'meanmedian'), (10, 300, 'meanmedian')
    ]
    
    configuration = ConfigParser.SafeConfigParser()
    configuration.add_section('Learner')
    configuration.set('Learner', 'datasetfile', '/home/wgeraedts/tmp/train_solvable.data')
    
    # load dataset
    dataset = load_dataset_from_config(configuration)
    folds = KFold(len(dataset.problems), n_folds=kfolds, indices=False)  # pylint: disable=unexpected-keyword-arg, no-value-for-parameter
    
    env = (dataset, kfolds, folds)
    args = [(env, x) for x in configs]
    
    # run jobs async
    pool = mp.Pool()
        
    pool.map_async(ml_cv_eval_async, args)
    pool.close()
    pool.join()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
