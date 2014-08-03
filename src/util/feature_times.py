'''
Used to generate feature calculation times for all problems
'''

from multiprocessing import Pool
import time
import sys
import os


def get_all_problems():
    '''
    Get all problem names for the E dataset

    Returns
    -------
    result : 1 x N Numpy array
        All problem names
    '''
    ds = DataSet()
    ds.load('E')
    return ds.problems


def get_prob_path(prob):
    '''
    Generates the path for a certain problem

    Parameters
    ----------
    prob : string
        The name of a certain problem

    Returns
    -------
    result : tuple
        Contains the problem name (1) and the time (2)
    '''
    return expand_filename('Problems/{}/{}'.format(prob[:3], prob))


def calculate_feature_time(prob):
    '''
    Classifies a problem and measures the elapsed time

    Parameters
    ----------
    prob : string
        The name of a certain problem

    Returns
    -------
    result : tuple
        Contains the problem name (1) and the time (2)
    '''
    feature_obj = EFeatures()
    
    curr_time = time.clock()
    print feature_obj.get(get_prob_path(prob), 30)
    return (prob, (time.clock() - curr_time))


def calculate_feature_times(cores=2):
    '''
    Calculate the time needed to classify a problem for all problems and
    stores it in a file

    Parameters
    ----------
    cores : int
        The amount of cores that can be used for calculations
    '''
    m_problems = get_all_problems()
    pool = Pool(processes=cores)
    results = pool.map_async(calculate_feature_time, m_problems)
    pool.close()
    pool.join()
    results.wait()
    results = results.get()
    with open('feature_times.csv', 'w') as f:
        for prob, tm in results:
            f.write('{},{}\n'.format(prob, tm))
    print 'Done'

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.Features import EFeatures
    from src.DataSet import DataSet
    from src.IO import expand_filename
    
    calculate_feature_times()
