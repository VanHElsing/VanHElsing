'''
Created on May 15, 2014

@author: daniel
'''

import os
import sys
from time import time

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
        if configuration.get('Learner', 'generatedataset') == 'True':
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


def main(argv=sys.argv[1:]):
    """
    input: Config file, dataset
    output: stores model in modelfile 
    """
    # load config
    parser = set_up_parser()
    args = parser.parse_args(argv)
    configuration = load_config(args.configuration)
    eval_kfolds = configuration.get('Learner', 'evalkfolds') == 'True'
    eval_whole = configuration.get('Learner', 'evalwhole') == 'True'
    export_model = configuration.get('Learner', 'exportmodel') == 'True'
    scheduler_id = configuration.get('Learner', 'scheduler')

    # load dataset 
    dataset = load_dataset(args, configuration)

    # init_model(config) TODO pass config
    scheduler_class = choose_scheduler(scheduler_id)
    scheduler = scheduler_class()
    # load model params/preprocessing options TODO
    
    if eval_kfolds:
        kfolds = int(configuration.get('Learner', 'kfolds'))
        # TODO partition dataset

        # TODO cross validation loop 
            #scheduler.fit(dataset[kfoldpartition,:])
            # evaluate scheduler 
           # scheduler.predict()

    if eval_whole or export_model:
        # fit scheduler on complete dataset
        # TODO perform preprocessing 
        scheduler.fit(dataset)
        if eval_whole:
            # eval scheduler on complete dataset
            print 'eval whole'
        if export_model:
            save_scheduler(scheduler, args.outputfile)
            print 'Scheduler with id {} exported to {}'.format(scheduler_id, args.outputfile)

    pass

if __name__ == '__main__':
    sys.exit(main())