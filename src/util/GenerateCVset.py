import numpy as np
import math
import os
import sys
import operator
import random
import itertools


def random_slice(dataset, n):
    problem_count, strat_count = dataset.strategy_matrix.shape
    
    part_size = problem_count / n
    
    # Set the folds for 10046 problems to random lists of length [1005, 1005, 1005, 1005, 1005, 1005, 1004, 1004, 1004, 1004]
    dreflist = list(range(problem_count))
    random.shuffle(dreflist)

    slices_with_extra = problem_count - part_size * n

    folds = []
    i = 0
    for f in range(n):
        tmp_part_size = part_size
        if f < slices_with_extra:
            tmp_part_size += 1
        
        folds.append([dataset.problems[dreflist[i + j]] for j in range(tmp_part_size)])
        i += tmp_part_size
    
    return folds

def combkfold_gen(n, r):
    fold_is = range(n)
    return [(
            list(xs),
            list(itertools.ifilter(lambda i: i not in xs, fold_is))
        ) for xs in itertools.combinations(fold_is, r)]

def main():
    result_path = os.path.join(PATH, 'data', 'E', 'CV')

    n = 10 # Number of folds
    r = 7 # Number of slices for training
    
    combination_count = math.factorial(n) / (math.factorial(n - r) * math.factorial(r))
    
    dataset = DataSet()
    dataset.load('E')
    dataset = remove_unsolveable_problems(dataset)
    
    slices = random_slice(dataset, n)
    
    folds = combkfold_gen(n, r)
    assert len(folds) is combination_count

    for i in range(len(folds)):
        train_is, test_is = folds[i]
        train_set = []
        test_set = []
        
        for train_i in train_is:
            train_set.extend(slices[train_i])
        
        for test_i in test_is:
            test_set.extend(slices[test_i])
        
        with open(os.path.join(result_path, 'CV_%d_%d_%d_train' % (n, r, i)), 'w') as out_s:
            for train_e in train_set:
                out_s.write('Problems/%s/%s\n' % (train_e[:3], train_e))
        
        with open(os.path.join(result_path, 'CV_%d_%d_%d_test' % (n, r, i)), 'w') as out_s:
            for test_e in test_set:
                out_s.write('Problems/%s/%s\n' % (test_e[:3], test_e))
        
    return 0


if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    from src.GlobalVars import PATH
    from src.DataSet import DataSet
    from src.data_util import remove_unsolveable_problems
    
    sys.exit(main())
