'''
Used for some simple feature time analysis.

The data file should be in the format:
    problem_name,feature_calculation_time,number_of_lines
'''

import numpy as np
import matplotlib.pyplot as pl
import DataSet


def read_prob_time_length():
    '''
    Reads the problem name, calculation time and number of lines
    from a file

    Returns
    -------
    probs : 1 x N Numpy array
        Contains all problem names
    data : N x 2 Numpy array
        Contains the times and lengths for each problem
    '''
    probs = []
    data = []
    with open('../data/E/prob_time_length_results.csv','r') as f:
        for l in f:
            l_split = l.strip().split(',')
            probs.append(l_split[0])
            data.append((float(l_split[1]),float(l_split[2])))
    return np.array(probs), np.array(data)

ds = DataSet.DataSet()
ds.load('E')

t_problems, t_data = read_prob_time_length()

print (t_problems == ds.problems).all()

# Everything is unsolvable starting at 3.000.000

# Set the limit and whether you want time (0) or amount of lines (1)
limit = 200000
col = 1

# Remove anything that falls below the limit
problems = t_problems[t_data[:,col]>limit]
strategy_matrix = np.copy(ds.strategy_matrix[t_data[:,col]>limit])
strategies = ds.strategies

print 'Amount of problems: {}'.format(problems.shape)
print 'Amount of probs v strats: {}'.format(strategy_matrix.shape)

def remove_unsolvable_probs(f_strat_matrix, f_problems):
    '''
    Removes unsolvable problems from the problem array and 
    strategy matrix array

    Parameters
    ----------
    f_strat_matrix : Numpy array
        Contains all strategy times
    f_problems : Numpy array
        Contains all problem names

    Returns
    -------
    f_strat_matrix : Numpy array
        Contains all remaining strategy times for problems that
        are left after removing unsolvable problems
    f_problems : Numpy array
        Contains all problem names after removing unsolvable probs
    '''
    mask = np.sum((f_strat_matrix != -1.), axis = 1) != 0
    f_strat_matrix = f_strat_matrix[mask]
    f_problems = f_problems[mask]
    return f_strat_matrix, f_problems

def remove_unused_strats(f_strat_matrix, f_strategies):
    '''
    Removes unused strategies from the strategy name array and 
    strategy matrix array

    Parameters
    ----------
    f_strat_matrix : Numpy array
        Contains problem times and lengths for all problems
    f_strategies : Numpy array
        Contains all strategy names

    Returns
    -------
    f_strat_matrix : Numpy array
        Contains all remaining strategy times for strategies that
        are left after removing unused strategies
    f_strategies : Numpy array
        Contains all strategies after removing unsolvable probs
    '''
    mask = np.sum((f_strat_matrix != -1.), axis = 0) != 0
    f_strategies = f_strategies[mask]
    f_strat_matrix = f_strat_matrix[:,mask]
    return f_strat_matrix, f_strategies

strategy_matrix, problems = remove_unsolvable_probs(strategy_matrix, problems)
print 'Amount of probs after removing unsolved: {}'.format(strategy_matrix.shape)

strategy_matrix, strategies = remove_unused_strats(strategy_matrix, strategies)
print 'Amount of strats after removing unused: {}'.format(strategy_matrix.shape)

# Sort matrix based on amount of problems a strategy solves
sorted_strategies = strategies[np.sum((strategy_matrix != -1.), axis = 0).argsort()[::-1]]
sorted_strategy_matrix = strategy_matrix[:,np.sum((strategy_matrix != -1.), axis = 0).argsort()[::-1]]

print 'Best strat solves {}/{} problems'.format(np.max(np.sum((strategy_matrix != -1.), axis = 0)), strategy_matrix.shape[0]) 

# Amount of problems to show times on
n = 5
print 'Means for first {} best strats: {}'.format(n, np.mean(sorted_strategy_matrix,axis=0)[:n])
print 'Medians for first {} best strats: {}'.format(n, np.median(sorted_strategy_matrix,axis=0)[:n])
print 'Maximums for first {} best strats: {}'.format(n, np.max(sorted_strategy_matrix,axis=0)[:n])

pl.hist(sorted_strategy_matrix[:,0], bins = 12)
pl.xlabel('Time in seconds')
pl.ylabel('Amount of solves')
pl.xlim((0,300))
pl.title('Best strategy for files with at least 200000 lines')
pl.show()