import numpy as np
import matplotlib.pyplot as pl
import IO
import DataSet

# def load_feature_times():
#     feature_times_temp = []
#     feature_problems_temp = []
#     with open('feature_times.csv','r') as f:
#         for l in f:
#             line_split = l.strip().split(',')
#             feature_problems_temp.append(line_split[0])
#             feature_times_temp.append(float(line_split[1]))
#     return np.array(feature_times_temp), np.array(feature_problems_temp)
#  
#  
# times, problems = load_feature_times()
# 
# def get_prob_path(prob):
#     return IO.expand_filename('Problems/{}/{}'.format(prob[:3], prob))
# 
# def parse_inputs(line):
#     temp_split = line.split("'")
#     amount = 0
#     with open(IO.expand_filename(temp_split[1]),'r') as f2:
#         for l2 in f2:
#             amount += 1
#     return amount

# file_lengths = []
# for i,p in enumerate(problems):
#     print i
#     amount_of_lines = 0
#     with open(get_prob_path(p),'r') as f:
#         for l in f:
#             amount_of_lines += 1
#             if l.startswith('include'):
#                 amount_of_lines += parse_inputs(l)
#     file_lengths.append(amount_of_lines)
#     
# with open('length_results.csv','w') as f:
#     for l in file_lengths:
#         f.write('{}\n'.format(l))
# 
# with open('prob_time_length_results.csv','w') as f:
#     for p,t,l in zip(list(problems),list(times),file_lengths):
#         f.write('{},{},{}\n'.format(p,t,l))
# 
# file_lengths_array = np.array(file_lengths)
# 
# pl.scatter(file_lengths_array,times)
# pl.show()

def read_prob_time_length():
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
    mask = np.sum((f_strat_matrix != -1.), axis = 1) != 0
    f_strat_matrix = f_strat_matrix[mask]
    f_problems = f_problems[mask]
    return f_strat_matrix, f_problems

def remove_unused_strats(f_strat_matrix, f_strategies):
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
