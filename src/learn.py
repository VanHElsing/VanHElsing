#! /usr/bin/env python
'''
Contains the learning interface of VanHElsing.
'''

import os
import sys
from sklearn.cross_validation import KFold
from argparse import ArgumentParser

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data_util import load_dataset_from_config
from src.GlobalVars import PATH, LOGGER
from src.IO import load_config
from src.schedulers.util import choose_scheduler
from src.schedulers.util import save_scheduler
from src.eval.ml_evaluations import eval_against_dataset


def set_up_parser():
    '''
    Initializes parser.
    '''
    parser = ArgumentParser(description='Learning strategy prediction '
                            'models from training data. --- June 2014.\n')
    parser.add_argument('-d', '--dataset',
                        help='The dataset file to fit/train the model on.',
                        default='')
    parser.add_argument('-o', '--outputfile',
                        help='The file to save the trained model to.',
                        default='')
    parser.add_argument('-c', '--configuration',
                        help='Which configuration file to use.',
                        default=os.path.join(PATH, 'config.ini'))
    return parser


def eval_sched_cv(kfolds, dataset, scheduler, max_time):
    folds = KFold(len(dataset.problems), n_folds=kfolds, indices=False)  # pylint: disable=unexpected-keyword-arg, no-value-for-parameter
    LOGGER.info("TRAINING + PREDICTION (Cross-validation folds %i)",
                kfolds)
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
        solved, _dummy_score = eval_against_dataset(test_dataset,
                                                    scheduler, max_time)
        try:
            sumscore += solved
        except TypeError:
            LOGGER.warn("Evaluation score is not a number.")
            solved = 0
        LOGGER.info("Solved: %s", solved)
    LOGGER.info("Total score: %s", sumscore / kfolds)


def eval_sched_whole(dataset, scheduler, max_time):
    LOGGER.info("EVALUATING (Whole dataset):.")
    solved, score = eval_against_dataset(dataset, scheduler, max_time)
    try:
        solved += 0
    except TypeError:
        LOGGER.warn("Evaluation score is not a number.")
        solved = 0
    LOGGER.info("Solved: %s", solved)
    LOGGER.info("Score: %s", score)


def learn(argv):
    """
    Learns and saves a model for predicting the best strategy for the dataset.
    The configuration file defines the type of model being learned.
    input: Config file, dataset
    output: stores model in modelfile
    """
    parser = set_up_parser()
    args = parser.parse_args(argv)
    configuration = load_config(args.configuration)

    eval_kfolds = configuration.getboolean('Learner', 'evalkfolds')
    eval_whole = configuration.getboolean('Learner', 'evalwhole')
    export_model = configuration.getboolean('Learner', 'exportmodel')
    scheduler_id = configuration.get('Learner', 'scheduler')
    max_time = float(configuration.get('Learner', 'maxruntime'))
    scheduler_class = choose_scheduler(scheduler_id)
    scheduler = scheduler_class(configuration)
    dataset = load_dataset_from_config(configuration)

    if eval_kfolds:
        kfolds = max(int(configuration.get('Learner', 'kfolds')), 2)
        eval_sched_cv(kfolds, dataset, scheduler, max_time)
    
    if eval_whole or export_model:
        LOGGER.info("TRAINING (Whole dataset):")
        scheduler.fit(dataset, max_time)
        if eval_whole:
            eval_sched_whole(dataset, scheduler, max_time)
        if export_model:
            exportfile = args.outputfile
            if exportfile == '':
                exportfile = configuration.get('Learner', 'exportfile')
            LOGGER.info("EXPORTING to: %s", exportfile)
            save_scheduler(scheduler, exportfile)
            LOGGER.info('Scheduler with id %s exported to %s',
                        scheduler_id, exportfile)

if __name__ == '__main__':
    sys.exit(learn(sys.argv[1:]))
