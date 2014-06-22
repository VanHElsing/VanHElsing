#! /usr/bin/env python
'''
Created on May 15, 2014

@author: Daniel Kuehlwein, Sil van de Leemput
'''

import os, sys
from sklearn.cross_validation import KFold
from argparse import ArgumentParser

from src.data_util import load_dataset_from_config
from src.GlobalVars import PATH, LOGGER
from src.IO import load_config
from src.schedulers.util import choose_scheduler
from src.schedulers.util import save_scheduler
from src.eval.ml_evaluations import eval_against_dataset


def set_up_parser():
    parser = ArgumentParser(description='Van HElsing ' +
                            'strategy scheduler learner and tester 0.1 --- May 2014.')
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


def learn(argv=sys.argv[1:]):
    """
    input: Config file, dataset
    output: stores model in modelfile
    """
    # load config
    parser = set_up_parser()
    args = parser.parse_args(argv)
    configuration = load_config(args.configuration)

    eval_kfolds = configuration.getboolean('Learner', 'evalkfolds')
    eval_whole = configuration.getboolean('Learner', 'evalwhole')
    export_model = configuration.getboolean('Learner', 'exportmodel')
    scheduler_id = configuration.get('Learner', 'scheduler')
    max_time = float(configuration.get('Learner', 'maxruntime'))

    # init strategy scheduler model using a preset (class & config)
    scheduler_class = choose_scheduler(scheduler_id)
    scheduler = scheduler_class(configuration)

    # load dataset
    dataset = load_dataset_from_config(configuration)

    if eval_kfolds:
        kfolds = max(int(configuration.get('Learner', 'kfolds')), 2)
        folds = KFold(len(dataset.problems), n_folds=kfolds, indices=False)
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
            solved, _score = eval_against_dataset(test_dataset, scheduler)
            try:
                sumscore += solved
            except TypeError:
                LOGGER.warn("Evaluation score is not a number.")
                solved = 0
            LOGGER.info("Solved: {}".format(solved))
        LOGGER.info("Total score: {}".format(sumscore / kfolds))
    if eval_whole or export_model:
        LOGGER.info("TRAINING (Whole dataset):")
        scheduler.fit(dataset, max_time)
        if eval_whole:
            LOGGER.info("EVALUATING (Whole dataset):.")
            solved, score = eval_against_dataset(dataset, scheduler)
            try:
                solved += 0
            except TypeError:
                LOGGER.warn("Evaluation score is not a number.")
                solved = 0
            LOGGER.info("Solved: {}".format(solved))
            LOGGER.info("Score: {}".format(score))
        if export_model:
            exportfile = args.outputfile
            if exportfile == '':
                exportfile = configuration.get('Learner', 'exportfile')
            LOGGER.info("EXPORTING to: %s", exportfile)
            save_scheduler(scheduler, exportfile)
            LOGGER.info('Scheduler with id %s exported to %s',
                        scheduler_id, exportfile)

if __name__ == '__main__':
    #args = ['-c','satallax.ini']
    args = ['-c','e.ini']
    learn(args)        
    #sys.exit(learn())
