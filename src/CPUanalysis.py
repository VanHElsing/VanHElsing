import numpy as np
import os
import sys

import matplotlib.pylab as pl
import multiprocessing as mp

from src.DataSet import DataSet
from src.CPU import CPU
from src.GlobalVars import PATH, EPATH, LOGGER

try:
   import cPickle as pickle
except:
   import pickle

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
    '''
    if os.path.isfile(path):
        with open(path, 'rb') as in_s:
            dataset = pickle.load(in_s)
    else:
        strategies = ['protokoll_G-E--_107_C45_F1_PI_AE_Q7_CS_SP_PS_S0Y', 'protokoll_H----_102_C18_F1_PI_AE_Q4_CS_SP_S1S', 'protokoll_H----_047_C18_F1_AE_R8_CS_SP_S2S', 'protokoll_G-E--_042_C45_F1_PI_AE_Q4_CS_SP_PS_S4S']
        
        tasks = []
        for strategy in strategies:
            tasks.extend(gen_tasks(cpu, 3, strategy))
        
        LOGGER.info("Executing single core series, first")
        dataset_single_first = compute_benchmark(cpu, tasks)
        
        #LOGGER.info("Executing single core series, second")
        #dataset_single_second = compute_benchmark(cpu, tasks)
        
        #LOGGER.info("Executing multicore series")
        #dataset_concurrent = compute_benchmark_concurrent(cpu, tasks, mp.cpu_count())
        
        #LOGGER.info("Executing oversaturation series")
        #dataset_oversat = compute_benchmark_concurrent(cpu, tasks, mp.cpu_count()*2)
        
        dataset = dataset_single_first #, dataset_single_second, dataset_concurrent, dataset_oversat)
        with open(path, 'wb') as out_s:
            pickle.dump(dataset, out_s)
    
    dataset_single_first = dataset
    
    pl.figure("Composed")
    
    p1 = show_dataset(dataset_single_first, "Single core, first", "r")
    #p2 = show_dataset(dataset_single_second, "Single core, second", "g")
    #p3 = show_dataset(dataset_concurrent, "Concurrent, fitting", "b")
    #p4 = show_dataset(dataset_oversat, "Concurrent, oversaturation", "y")
    
    #pl.legend([p1, p2, p3, p4], ["Single core, first", "Single core, second", "Concurrent, fitting", "Concurrent, oversaturation"])
    '''
    cpu.ratios.sort(key=lambda x : x[0])
    pl.figure("Tuning")
    pl.plot(map(lambda x : x[0], cpu.ratios), map(lambda x : x[2], cpu.ratios))
    
    pl.figure("Tuning samples")
    pl.scatter(map(lambda x : x[0], cpu.ratios), map(lambda x : x[2] * x[0], cpu.ratios))
    
    pl.show()
    
    pass
    
if __name__ == '__main__':
    cpu = CPU()
    
    LOGGER.info("Tuning CPU on dataset... (or getting from cache)")
    cpu.load_or_gen_data()
    
    LOGGER.info("Tuning completed, executing benchmark")
    execute_benchmark(cpu)

    sys.exit(0)
