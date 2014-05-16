'''
Created on May 15, 2014

@author: daniel
'''

import os
import sys
from time import time
import numpy as np
from sklearn.cross_validation import KFold
from argparse import ArgumentParser

from src.GlobalVars import PATH, LOGGER
from src.IO import load_config, load_object, save_object
from src.RunATP import get_ATP_from_config
from src.schedulers.util import choose_scheduler
from src.schedulers.util import save_scheduler
from src.DataSet import DataSet


def set_up_parser():
    parser = ArgumentParser(description='Van HElsing strategy scheduler learner and tester 0.1 --- May 2014.')
    parser.add_argument('-d', '--dataset', 
                        help='The dataset file to fit/train the model on.',
                        default=os.path.join(PATH, 'data/train.data'))
    parser.add_argument('-o', '--outputfile', 
                        help='The file to save the trained model to.',
                        default=os.path.join(PATH, 'models/export.ss'))
    parser.add_argument('-c', '--configuration',
                        help='Which configuration file to use.',
                        default=os.path.join(PATH, 'config.ini'))
    return parser


def load_dataset(args, configuration):
    dataset = None
    if not os.path.isfile(args.dataset):
        print "No dataset found for {}.".format(args.dataset)
        if is_option_enabled(configuration, 'generatedataset'):
            print "Generating dataset...".format(args.dataset)
            dataset = DataSet(configuration.get('Scheduler', 'datatype'))
            save_object(dataset, args.dataset)
            print "Dataset generated and saved to: {}.".format(args.dataset)
        else:
            print "Warning: continuing without dataset!"
    else:
        dataset = load_object(args.dataset)
        if not isinstance(dataset, DataSet):
            raise "file: {} is not of type DataSet".format(args.dataset)
        print "Dataset: {} loaded.".format(args.dataset)           
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



    # init strategy scheduler model using a preset (class & config) 
    scheduler_class = choose_scheduler(scheduler_id)
    scheduler = scheduler_class(configuration)

    # load dataset 
    dataset = load_dataset(args, configuration)
    # TODO execute model / dataset preprocessing options 
    
    if eval_kfolds:
        kfolds = max(int(configuration.get('Learner', 'kfolds')), 2)
        folds = KFold(len(dataset.problems), n_folds = kfolds, indices = False)
        print "TRAINING & PREDICTION (Cross-validation folds:", kfolds, "):"
        for i, fold in enumerate(folds):
            print "fold: ", (i + 1)
            train_idx, test_idx = fold
            train_features = dataset.feature_matrix[train_idx]
            test_features = dataset.feature_matrix[test_idx]
            train_labels = dataset.strategy_matrix[train_idx]
            #scheduler.fit(train_features, train_labels)

            # TODO evaluation of scheduler

    if eval_whole or export_model:
        # fit scheduler on complete dataset
        # TODO perform preprocessing 
        scheduler.fit(dataset)
        if eval_whole:
            # TODO eval scheduler on complete dataset
            print 'eval whole'
        if export_model:
            save_scheduler(scheduler, args.outputfile)
            print 'Scheduler with id {} exported to {}'.format(scheduler_id, args.outputfile)

    pass

if __name__ == '__main__':
    sys.exit(main())