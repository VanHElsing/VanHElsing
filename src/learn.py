'''
Created on May 15, 2014

@author: daniel
'''

import os
import sys
import numpy as np
from sklearn.cross_validation import KFold
from argparse import ArgumentParser

from src.GlobalVars import PATH, LOGGER
from src.IO import load_config, load_object, save_object
from src.schedulers.util import choose_scheduler
from src.schedulers.util import save_scheduler
from src.DataSet import DataSet
from src.data_util import remove_unsolveable_problems
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
    parser.add_argument('-lp', '--limitprobs',
                        help='Limit the amount of problems in the dataset for testing.',
                        default=-1)
    return parser


def load_dataset(args, configuration):
    dataset = DataSet()
    datasetfile = args.dataset
    if datasetfile == '':
        datasetfile = configuration.get('Learner', 'datasetfile')
    if configuration.getboolean('Learner', 'generatedataset'): 
        LOGGER.info("Generating dataset...")
        dataset.load(configuration.get('Learner', 'datatype'))
        save_object(dataset, datasetfile)
        LOGGER.info("Dataset generated and saved to: %s.", datasetfile)
    elif not os.path.isfile(datasetfile):
        LOGGER.warn("No dataset found for %s.", datasetfile)
        LOGGER.warn("Continuing without dataset!")
    else:
        dataset = load_object(datasetfile)
        if not isinstance(dataset, DataSet):
            msg = "file: %s is not of type DataSet" % datasetfile
            LOGGER.error(msg)
            raise IOError(99, msg)
        LOGGER.info("Dataset: %s loaded  prob x strats: %i x %i",
                    datasetfile, len(dataset.problems), len(dataset.strategies))
    return dataset


def main(argv=sys.argv[1:]):
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
    dataset = load_dataset(args, configuration)
    dataset = remove_unsolveable_problems(dataset) 
    # retain only a few problems if option set
    if args.limitprobs > -1:
        dataset = dataset.mask(range(int(args.limitprobs)))
        LOGGER.info("Dataset limiting problems - prob x strats: %i x %i",
                    len(dataset.problems), len(dataset.strategies))

    # TODO dataset preprocessing options

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
    pass

if __name__ == '__main__':
    sys.exit(main())
