'''
Created on May 15, 2014

@author: daniel
'''

import os
import sys
from sklearn.cross_validation import KFold
from argparse import ArgumentParser

from src.GlobalVars import PATH, LOGGER
from src.IO import load_config, load_object, save_object
from src.schedulers.util import choose_scheduler
from src.schedulers.util import save_scheduler
from src.DataSet import DataSet
from src.eval.evaluations import eval_against_dataset


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


def load_dataset(args, configuration):
    dataset = DataSet()
    datasetfile = args.dataset
    if datasetfile == '':
        datasetfile = configuration.get('Learner', 'datasetfile')
    if is_option_enabled(configuration, 'generatedataset'):
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
        LOGGER.info("Dataset: %s loaded.", datasetfile)        
    return dataset


def is_option_enabled(configuration, option):
    return configuration.get('Learner', option).lower() == 'true'


def main(argv=sys.argv[1:]):
    """
    input: Config file, dataset
    output: stores model in modelfile 
    """
    # load config
    parser = set_up_parser()
    args = parser.parse_args(argv)
    configuration = load_config(args.configuration)

    eval_kfolds = is_option_enabled(configuration, 'evalkfolds')
    eval_whole = is_option_enabled(configuration, 'evalwhole')
    export_model = is_option_enabled(configuration, 'exportmodel')
    scheduler_id = configuration.get('Learner', 'scheduler')
    max_time = float(configuration.get('Learner', 'maxruntime'))


    # init strategy scheduler model using a preset (class & config) 
    scheduler_class = choose_scheduler(scheduler_id)
    scheduler = scheduler_class(configuration)

    # load dataset 
    dataset = load_dataset(args, configuration)
    # TODO dataset preprocessing options 
    
    if eval_kfolds:
        kfolds = max(int(configuration.get('Learner', 'kfolds')), 2)
        folds = KFold(len(dataset.problems), n_folds = kfolds, indices = False)
        LOGGER.info("TRAINING + PREDICTION (Cross-validation folds %i)", kfolds)
        sumscore = 0
        for i, (train_idx, test_idx) in enumerate(folds):
            train_dataset = dataset.mask(train_idx)
            test_dataset = dataset.mask(test_idx)
            LOGGER.info("Fold: %i -- #train: %i/%i",
                i + 1, len(train_dataset.problems), len(dataset.problems))
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