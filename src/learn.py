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
    if not os.path.isfile(datasetfile):
        print "No dataset found for {}.".format(datasetfile)
        if is_option_enabled(configuration, 'generatedataset'):
            print "Generating dataset...".format(datasetfile)
            dataset.load(configuration.get('Scheduler', 'datatype'))
            save_object(dataset, datasetfile)
            print "Dataset generated and saved to: {}.".format(datasetfile)
        else:
            print "Warning: continuing without dataset!"
    else:
        dataset = load_object(datasetfile)
        if not isinstance(dataset, DataSet):
            raise "file: {} is not of type DataSet".format(datasetfile)
        print "Dataset: {} loaded.".format(datasetfile)           
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
    # TODO execute model / dataset preprocessing options 
    
    if eval_kfolds:
        kfolds = max(int(configuration.get('Learner', 'kfolds')), 2)
        folds = KFold(len(dataset.problems), n_folds = kfolds, indices = False)
        print "TRAINING & PREDICTION (Cross-validation folds:", kfolds, "):"
        for i, (train_idx, test_idx) in enumerate(folds):
            train_dataset = dataset.mask(train_idx)
            test_dataset = dataset.mask(test_idx)
            print "Fold: {} -- #train: {}/{}".format(
                i + 1, len(train_dataset.problems), len(dataset.problems))
            print "Fitting model."
            scheduler.fit(train_dataset, max_time)

            # TODO evaluation of scheduler

    if eval_whole or export_model:
        # fit scheduler on complete dataset
        # TODO perform preprocessing 
        scheduler.fit(dataset, max_time)
        if eval_whole:
            # TODO eval scheduler on complete dataset
            print 'eval whole'
        if export_model:
            exportfile = args.outputfile
            if exportfile == '':
                exportfile = configuration.get('Learner', 'exportfile')            
            save_scheduler(scheduler, exportfile)
            print 'Scheduler with id {} exported to {}'.format(
                scheduler_id, exportfile)

    pass

if __name__ == '__main__':
    sys.exit(main())