import sys
import os
import re
import math
import ConfigParser


REGEX_FILE = re.compile('CV_([0-9]+)_([0-9]+)_([0-9]+)_(train|test)')


def read_file(fpath, dataset):
    problems = dataset.problems.tolist()
    result = []
    
    with open(fpath, 'r') as in_s:
        for l in in_s:
            filename = l.split('/')[-1].strip()
            result.append(problems.index(filename))
    
    return result


def init_default_config():
    config = ConfigParser.SafeConfigParser()
    config.add_section('Learner')
    config.add_section('ATP Settings')
    config.set('ATP Settings', 'features', 'E')
    return config
    

def init_2NNmax_config():
    config = init_default_config()
    config.set('Learner', 'scheduler', 'NN')
    config.set('Learner', 'min_neighbors', '2')
    config.set('Learner', 'negscore_func', 'max')
    return ('2NNmax', config)
    

def init_group1_config():
    config = init_default_config()
    config.set('Learner', 'scheduler', 'Group1')
    
    config.add_section('Group1Scheduler')
    config.set('Group1Scheduler', 'pcas', '')
    config.set('Group1Scheduler', 'standardize', 'True')
    config.set('Group1Scheduler', 'stdcap', '2.5')
    config.set('Group1Scheduler', 'alpha', '1')
    config.set('Group1Scheduler', 'beta', '5')
    config.set('Group1Scheduler', 'gamma', '7')
    config.set('Group1Scheduler', 'delta', '50')
    config.set('Group1Scheduler', 'tmultiplier', '1.1')
    config.set('Group1Scheduler', 'tadder', '0')
    config.set('Group1Scheduler', 'toptimizer', 'True')
    config.set('Group1Scheduler', 'topt', '10')
    config.set('Group1Scheduler', 'boosting', 'False')
    config.set('Group1Scheduler', 'log', 'True')
    
    return ('group1', config)


def init_greedy_config():
    config = init_default_config()
    config.set('Learner', 'scheduler', 'Greedy')
    return ('greedy', config)
    
    
def init_smt_config():
    config = init_default_config()
    config.set('Learner', 'scheduler', 'Static')
    return ('smt', config)


def main(argv):
    data_path = os.path.join(PATH, "data", "E", "CV")
    files = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f)) ]
    
    # The current run is for these parameters only
    n = 10
    r = 7
    
    combination_count = math.factorial(n) / (math.factorial(n - r) * math.factorial(r))
    
    train_test_folds = []
    train_train_folds = []
    
    dataset = DataSet()
    dataset.load('E')
    dataset = remove_unsolveable_problems(dataset)
    
    for i in range(combination_count):
        train_file = 'CV_%d_%d_%d_train' % (n, r, i)
        test_file = 'CV_%d_%d_%d_test' % (n, r, i)
        
        if not os.path.isfile(os.path.join(data_path, train_file)):
            sys.stderr.write("ERROR Missing file '%s'\n" % train_file)
            assert False
        
        if not os.path.isfile(os.path.join(data_path, test_file)):
            sys.stderr.write("ERROR Missing file '%s'\n" % test_file)
            assert False
        
        print "Reading %s" % train_file
        train_mask = read_file(os.path.join(data_path, train_file), dataset)
        
        print "Reading %s" % test_file
        test_mask = read_file(os.path.join(data_path, test_file), dataset)
        
        train_test_folds.append((i, (train_mask, test_mask)))
        train_train_folds.append((i, (train_mask, train_mask)))
    
    schedule_path = os.path.join(PATH, 'runs', 'theory', 'E')
    
    # Greedy, SMT, KNN max 2, Group1
    configs = [init_greedy_config(), init_2NNmax_config(), init_smt_config()]
    limits = [10, 60, 300]
    
    for name, config in configs:
        for limit in limits:
            filename = "CV_%d_%d_train_test_%s_%d" % (n, r, name, limit)
            filepath = os.path.join(schedule_path, filename)
            
            if os.path.isfile(filepath):
                print "Skipping %s" % filename
                continue
            
            ml_cv_eval_superasync(config, dataset, train_test_folds, limit, filepath)
    
    for name, config in configs:
        for limit in limits:
            filename = "CV_%d_%d_train_train_%s_%d" % (n, r, name, limit)
            filepath = os.path.join(schedule_path, filename)
            
            if os.path.isfile(filepath):
                print "Skipping %s" % filename
                continue
            
            ml_cv_eval_superasync(config, dataset, train_train_folds, limit, filepath)
    return

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.data_util import load_dataset_from_file
    from src.data_util import remove_unsolveable_problems
    from src.schedulers.util import choose_scheduler
    from src.GlobalVars import PATH, LOGGER
    from src.DataSet import DataSet
    from src.schedulers.StaticScheduler import StaticScheduler
    from src.eval.ml_evaluations import ml_cv_eval_superasync
    sys.exit(main(sys.argv[1:]))
