import sys
import os
import re
import math
import ConfigParser
import tempfile
import multiprocessing as mp
from shutil import rmtree


REGEX_FILE = re.compile('CV_([0-9]+)_([0-9]+)_([0-9]+)_(train|test)')


def init_default_config():
    config = ConfigParser.SafeConfigParser()
    config.add_section('Learner')
    config.add_section('Scheduler')
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


def read_file(fpath, dataset):
    problems = dataset.problems.tolist()
    result = []
    
    with open(fpath, 'r') as in_s:
        for l in in_s:
            filename = l.split('/')[-1].strip()
            result.append(problems.index(filename))
    
    return result


def load_folds(n, r, dataset, data_path):
    combination_count = math.factorial(n) / (math.factorial(n - r) * math.factorial(r))
    
    train_test_folds = []
    train_train_folds = []

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
    
    return train_test_folds, train_train_folds


def combo_cv_eval_ml(configs, limits, dataset, folds, prefix, schedule_path):
    for name, config in configs:
        for limit in limits:
            filename = "%s_%s_%d" % (prefix, name, limit)
            filepath = os.path.join(schedule_path, filename)
            
            if os.path.isfile(filepath):
                print "Skipping %s" % filename
                continue
            
            ml_cv_eval_superasync(config, dataset, folds, limit, filepath)


def combo_cv_eval_atp_job(args):
    try:
        common_args, job_args = args
        
        (TPTP_path, config_file, limit, filepath) = common_args
        (p_name) = job_args
        
        p_path = os.path.join(TPTP_path, 'Problems', p_name[:3], p_name)
                            
        proof_found, time_used = helsing(argv=['-c', config_file, '-t', str(limit), '-p', p_path])
        LOGGER.info('%s: %s (%s)' % (p_name, proof_found, time_used))
        
        if proof_found:
            with open(filepath, 'a+') as result_fs:
                result_fs.write("%s,%f\n" % (p_name, time_used))
    except:
        print "Error in thread"
        pass


# Warning: the following function will modify configs
# Make fresh copies if you want to reuse them
def combo_cv_eval_atp(configs, limits, dataset, folds, prefix, schedule_path):
    TPTP_path = os.getenv('TPTP')
    assert TPTP_path is not None
    
    for name, config in configs:
        for limit in limits:
            filename = "%s_%s_%d" % (prefix, name, limit)
            filepath = os.path.join(schedule_path, filename)
            
            if os.path.isfile(filepath):
                print "Skipping %s" % filename
                continue
            
            for i, (train_idx, test_idx) in folds:
                config_path = tempfile.mkdtemp(prefix="helsing")
                try:
                    # Step 1: make configuration file
                    export_file = os.path.join(config_path, "export.ss")
                    data_file = os.path.join(config_path, "train.data")
                    
                    # Populate with specific paths and options
                    config.set("Scheduler", "modelfile", export_file)
                    config.set("Learner", "generatedataset", "True")
                    config.set("Learner", "datasetfile", data_file)
                    config.set("Learner", "exportmodel", "True")
                    config.set("Learner", "exportfile", export_file)
                    config.set("Learner", "evalkfolds", "False")  # We do this ourselves
                    config.set("Learner", "evalwhole", "False")  # We do this ourselves
                    config.set("Learner", "maxruntime", "300")  # Different from the eval runtime
                    config.set("ATP Settings", "binary", "contrib/E/PROVER/eprover")  # TODO fetch this from the real config
                    config.set("ATP Settings", "time", "--cpu-limit=")
                    config.set("ATP Settings", "default", "-s --memory-limit=Auto --tstp-format --proof-object")
                    
                    config_file = os.path.join(config_path, "config.ini")
                    with open(config_file, 'wb') as config_fs:
                        config.write(config_fs)
                    
                    # Step 2: dump data
                    save_object(dataset.mask(train_idx), data_file)
                    
                    # Step 3: learn data
                    learn(argv=['-c', config_file])
                    
                    # Step 4: execute eval
                    jobs = []
                    
                    common_args = (TPTP_path, config_file, limit, filepath)
                    for p_idx in test_idx:
                        p_name = dataset.problems[p_idx]
                        job_args = (p_name)
                        
                        jobs.append((common_args, job_args))
                    
                    pool = mp.Pool()

                    result = pool.map(combo_cv_eval_atp_job, jobs)
                    pool.close()
                    pool.join()
                    
                    LOGGER.info("All jobs have joined main thread")
                finally:
                    rmtree(config_path) #TODO: add again
            

def main(argv):
    data_path = os.path.join(PATH, "data", "E", "CV")
    
    # The current run is for these parameters only
    n = 10
    r = 7
    
    dataset = DataSet()
    dataset.load('E')
    dataset = remove_unsolveable_problems(dataset)
    
    train_test_folds, train_train_folds = load_folds(n, r, dataset, data_path)
    
    schedule_ml_path = os.path.join(PATH, 'runs', 'theory', 'E')
    schedule_atp_path = os.path.join(PATH, 'runs', 'real', 'E')
    
    # Greedy, SMT, KNN max 2, Group1
    configs = [init_greedy_config(), init_2NNmax_config(), init_smt_config()]
    limits = [10, 60, 300]
    
    #combo_cv_eval_ml(configs, limits, dataset, train_test_folds, "CV_%d_%d_train_test" % (n, r), schedule_ml_path)
    #combo_cv_eval_ml(configs, limits, dataset, train_train_folds, "CV_%d_%d_train_train" % (n, r), schedule_ml_path)
    
    combo_cv_eval_atp(configs, limits, dataset, train_test_folds, "CV_%d_%d_train_test" % (n, r), schedule_atp_path)
    combo_cv_eval_atp(configs, limits, dataset, train_train_folds, "CV_%d_%d_train_train" % (n, r), schedule_atp_path)

    return 0

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.data_util import remove_unsolveable_problems
    from src.GlobalVars import PATH
    from src.DataSet import DataSet
    from src.eval.ml_evaluations import ml_cv_eval_superasync
    from src.IO import save_object
    from src.learn import learn
    from src.helsing import helsing
    from src.GlobalVars import LOGGER
    sys.exit(main(sys.argv[1:]))
