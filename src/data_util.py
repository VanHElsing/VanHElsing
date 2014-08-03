'''
Auxiliary functions for data.
'''

import numpy as np
import os
from src.DataSet import DataSet
from src.GlobalVars import LOGGER
from src.IO import load_object


def remove_unsolveable_problems(data_set):
    """
    Deletes all problems that cannot be solved.
    """
    problem_filter = np.max(data_set.strategy_matrix, axis=1) > -1
    return data_set.mask(problem_filter)


def not_solved_by_strat(data_set, s_index, s_time):
    """
    Returns a list of the indices of all problems are not solved
    by strategy s_index in s_time.
    """
    nr_of_problems = data_set.strategy_matrix.shape[0]
    s_matrix = data_set.strategy_matrix
    not_solved_by_strats = [i for i in range(nr_of_problems) if
                            (s_matrix[i, s_index] > s_time or
                             s_matrix[i, s_index] == -1)]
    return not_solved_by_strats


def load_dataset_from_config(configuration):
    '''
    Load dataset from configuration.
    '''
    dataset = configuration.get('Learner', 'datasetfile')
    return load_dataset_from_file(dataset)


def load_dataset_from_file(datasetfile):
    '''
    Load dataset from file.
    '''
    dataset = DataSet()
    if not os.path.isfile(datasetfile):
        msg = "No dataset found for %s." % datasetfile
        LOGGER.error(msg)
        raise IOError(99, msg)
    else:
        dataset = load_object(datasetfile)
        if not isinstance(dataset, DataSet):
            msg = "File: %s is not of type DataSet" % datasetfile
            LOGGER.error(msg)
            raise IOError(99, msg)
        LOGGER.info("Dataset: %s loaded  prob x strats: %i x %i",
                    datasetfile, len(dataset.problems),
                    len(dataset.strategies))
    return dataset


def load_or_generate_dataset(datasetfile, configuration):
    '''
    Depending on the configuration settings either
    loads or generated a dataset.
    '''
    if datasetfile == '':
        datasetfile = configuration.get('DataUtil', 'infile')
    if configuration.getboolean('DataUtil', 'generatedataset'):
        datatype = configuration.get('DataUtil', 'datatype')
        LOGGER.info("Generating dataset from type: %s.", datatype)
        dataset = DataSet()
        dataset.load(datatype)
        LOGGER.info("Dataset generated.")
    else:
        dataset = load_dataset_from_file(datasetfile)
    return dataset
