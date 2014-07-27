'''
Used to generate feature calculation times for all problems
'''

from multiprocessing import Pool
import DataSet
import time
import IO


def get_all_problems():
    '''
    Get all problem names for the E dataset

    Returns
    -------
    result : 1 x N Numpy array
        All problem names
    '''
    ds = DataSet.DataSet()
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
    return IO.expand_filename('Problems/{}/{}'.format(prob[:3], prob))


def solve_problem(prob):
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
    cmd = '../contrib/E/PROVER/classify_problem -caaaaaaaaaaaaa --tstp-in {}'
    curr_time = time.clock()
    print IO.run_command(cmd.format(get_prob_path(prob)), 30)
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
#     m_problems = ['AGT001+1.p','AGT001+2.p','AGT002+1.p','SWB005+2.p','SET013+4.p']
    pool = Pool(processes=cores)
    results = pool.map_async(solve_problem, m_problems)
    pool.close()
    pool.join()
    results.wait()
    results = results.get()
    with open('feature_times.csv', 'w') as f:
        for prob, tm in results:
            f.write('{},{}\n'.format(prob, tm))
    print 'Done'
