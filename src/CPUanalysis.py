import numpy as np
import os
import sys

import matplotlib.pylab as pl
import multiprocessing as mp

from src.DataSet import DataSet
from src.data_util import remove_unsolveable_problems
from src.CPU import CPU
from src.GlobalVars import PATH, EPATH, LOGGER

try:
   import cPickle as pickle
except:
   import pickle

def gen_benchmark_tasks(cpu, problems_per_bin):
    dataset = DataSet()
    dataset.load('E')
    dataset = remove_unsolveable_problems(dataset)
    
    TPTPPath = os.getenv('TPTP')
    if TPTPPath is None:
        raise IOError('$TPTP is not defined.')
    
    strategy_i = list(dataset.strategies).index("--definitional-cnf=24 --tstp-in --condense --simul-paramod --forward-context-sr --strong-destructive-er --destructive-er-aggressive --destructive-er --prefer-initial-clauses -tKBO6 -winvfreqrank -c1 -Ginvfreq -F1 -s --delete-bad-limit=1024000000 -WSelectNewComplexAHPNS -H'(10*ConjectureRelativeSymbolWeight(ConstPrio,0.1, 100, 100, 100, 100, 1.5, 1.5, 1.5),1*FIFOWeight(ConstPrio))'")
    
    bin_borders = [1.0, 10.0, 30.0, 60.0, 100.0, 150.0, 200.0, 250.0, 300.0] # Must be sorted
    bins = dict()
    
    for bin_border in bin_borders:
        bins[bin_border] = []
    
    problem_is = range(dataset.problems.size)
    np.random.shuffle(problem_is)
    
    result = []
    for problem_i in problem_is:
        pred_time = dataset.strategy_matrix[problem_i][strategy_i]
        if pred_time == -1.0:
            continue
            
        if pred_time < 0.5:
            continue
        
        # Find the correct bin
        current_bin = None
        for bin_border in bin_borders:
            if pred_time < bin_border:
                if len(bins[bin_border]) < problems_per_bin:
                    current_bin = bin_border
                break
        
        if current_bin is None:
            continue
        
        p_name = dataset.problems[problem_i]
        strategy = dataset.strategies[strategy_i]
        scaled_time = pred_time * cpu.get_ratio(pred_time)
        
        bins[current_bin].append((p_name, strategy, pred_time, scaled_time))
    
    for problems in bins.values():
        result.extend(problems)
    
    return result

def benchmark_task(args):
    cpu, strategy, p_path, p_name, strategy, pred_time, scaled_time = args
    real_time = cpu.measure(strategy, p_path)
    print 'Finished %s in %f' % (p_path, real_time)
    return (p_name, strategy, pred_time, scaled_time, real_time)

def compute_benchmark(cpu, dataset):
    TPTPPath = os.getenv('TPTP')

    result = []
    for p_name, strategy, pred_time, scaled_time in dataset:
        p_path = os.path.join(TPTPPath, 'Problems', p_name[:3], p_name)
        
        result.append(benchmark_task((cpu, strategy, p_path, p_name, strategy, pred_time, scaled_time)))
        
    return result

def compute_benchmark_concurrent(cpu, dataset, cores=None):
    TPTPPath = os.getenv('TPTP')
    
    if cores is None:
        cores = mp.cpu_count()
    
    pool = mp.Pool(processes=cores)
    args = [(cpu, strategy, os.path.join(TPTPPath, 'Problems', p_name[:3], p_name), p_name, strategy, pred_time, scaled_time) for p_name, strategy, pred_time, scaled_time in dataset]
    results = pool.map_async(benchmark_task, args)
    pool.close()
    pool.join()
    results.wait()
    
    return results.get()
    
def show_dataset(dataset, name, color):
    X = []
    y = []
    for row in dataset:
        p_name, strategy, pred_time, scaled_time, real_time = row
    
        print "----"
        print p_name
        print strategy
        print pred_time
        print scaled_time
        print real_time
        
        X.append(pred_time)
        y.append(scaled_time / real_time)
    
    X = np.array(X)
    y = np.array(y)
    
    return pl.scatter(X, y, c=color)

def execute_benchmark(cpu):
    path = os.path.join(PATH, 'tuning_benchmark')
    
    print path
    if os.path.isfile(path):
        with open(path, 'rb') as in_s:
            dataset = pickle.load(in_s)
    else:
        tasks = gen_benchmark_tasks(cpu, 3)
        
        LOGGER.info("Executing single core series, first")
        dataset_single_first = compute_benchmark(cpu, tasks)
        
        LOGGER.info("Executing single core series, second")
        dataset_single_second = compute_benchmark(cpu, tasks)
        
        LOGGER.info("Executing multicore series")
        dataset_concurrent = compute_benchmark_concurrent(cpu, tasks, mp.cpu_count())
        
        LOGGER.info("Executing oversaturation series")
        dataset_oversat = compute_benchmark_concurrent(cpu, tasks, mp.cpu_count()*2)
        
        dataset = (dataset_single_first, dataset_single_second, dataset_concurrent, dataset_oversat)
        with open(path, 'wb') as out_s:
            pickle.dump(dataset, out_s)
    
    dataset_single_first, dataset_single_second, dataset_concurrent, dataset_oversat = dataset
    
    pl.figure("Composed")
    
    p1 = show_dataset(dataset_single_first, "Single core, first", "r")
    p2 = show_dataset(dataset_single_second, "Single core, second", "g")
    p3 = show_dataset(dataset_concurrent, "Concurrent, fitting", "b")
    p4 = show_dataset(dataset_oversat, "Concurrent, oversaturation", "y")
    
    pl.legend([p1, p2, p3, p4], ["Single core, first", "Single core, second", "Concurrent, fitting", "Concurrent, oversaturation"])
    pl.show()
    
    pass
    
if __name__ == '__main__':
    cpu = CPU()
    
    LOGGER.info("Tuning CPU on dataset... (or getting from cache)")
    cpu.load_or_gen_data()
    
    LOGGER.info("Tuning completed, executing benchmark")
    execute_benchmark(cpu)

    sys.exit(0)
