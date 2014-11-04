import numpy as np
import os
import sys
import operator

try:
    import cPickle as pickle
except ImportError:
    import pickle
    

def main():
    with open(os.path.join(PATH, 'tuning_benchmark_crookshanks'), 'rb') as in_s:
        dataset1 = pickle.load(in_s)
    
    with open(os.path.join(PATH, 'tuning_benchmark_cn79'), 'rb') as in_s:
        dataset2 = pickle.load(in_s)
    
    assert len(dataset1) == len(dataset2)
    
    print "Pred	MinRatio MaxRatio"
    dataset_structured = dict()
    for dataset_i in range(len(dataset1)):
        X = []
        y = []
        for j in range(len(dataset1[dataset_i][1])):
            _p_name, _strategy, pred_time1, real_time1 = dataset1[dataset_i][1][j]
            _p_name, _strategy, pred_time2, real_time2 = dataset2[dataset_i][1][j]
            
            assert pred_time1 == pred_time2
            X.append(pred_time1)
            y.append(real_time2 / real_time1)
        
        X = np.array(X)
        y = np.array(y)
        
        # tups = zip(X, y)
        # tups.sort(key=operator.itemgetter(0))
        # X, y = zip(*tups)
        
        for xi, yi in zip(X, y):
            if xi not in dataset_structured:
                dataset_structured[xi] = []
            dataset_structured[xi].append(yi)
    
    result = []
    for xi, yis in dataset_structured.iteritems():
        result.append((xi, min(yis), max(yis)))
    
    result.sort(key=operator.itemgetter(0))
    for xi, minyis, maxyis in result:
        print "%f	%f	%f" % (xi, minyis, maxyis)
    
    return 0

if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    from src.GlobalVars import PATH
    
    sys.exit(main())
