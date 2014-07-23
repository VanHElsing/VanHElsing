'''
Created on May 18, 2014

@author: daniel
'''
import os
import sys
from time import time
import numpy as np

from src.DataSet import DataSet
from src.data_util import remove_unsolveable_problems

from src.GlobalVars import PATH, EPATH, LOGGER
from src.RunATP import ATP

try:
   import cPickle as pickle
except:
   import pickle

def gen_tasks(dataset, problems_per_bin, strategy_file):
    TPTPPath = os.getenv('TPTP')
    if TPTPPath is None:
        raise IOError('$TPTP is not defined.')
    
    strategy_i = list(dataset.strategy_files).index(strategy_file)
    
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

        bins[current_bin].append((p_name, strategy, pred_time))
    
    for problems in bins.values():
        result.extend(problems)
    
    return result

def gen_testdata():
    strategy_file = 'protokoll_G-E--_042_C45_F1_PI_AE_Q4_CS_SP_PS_S4S' # --auto-schedule
    
    dataset = DataSet()
    dataset.whitelist = [strategy_file] # for faster loading
    
    dataset.load('E')
    dataset = remove_unsolveable_problems(dataset)
    
    return gen_tasks(dataset, 3, strategy_file)

class CPU(object):
    times = None
    ratios = None
    
    atp = None
    
    def __init__(self):
        eprover_path = os.path.join(EPATH, 'eprover')
        self.atp = ATP(eprover_path, '--cpu-limit=',
                  '--tstp-format -s --proof-object --memory-limit=2048')
        pass
    
    def measure(self, strategy, p_path):
        use_cpu_time = (os.name is "posix")
        start_time = time()
        
        proof_found, _cs, _o, cpu_time = self.atp.run(strategy, 400, p_path, use_cpu_time)
        assert proof_found
        
        if use_cpu_time:
            used_time = cpu_time
        else:
            used_time = time() - start_time
        
        return used_time

    def compare_cpu_with_data_set(self, runs=3):
        TPTPPath = os.getenv('TPTP')
        if TPTPPath is None:
            raise IOError('$TPTP is not defined.')

        test_data = gen_testdata()

        series = []
        LOGGER.info('Starting CPU measurements')
        for p_name, p_strategy, p_time in test_data:
            LOGGER.info('Problem %s', p_name)
            p_path = os.path.join(TPTPPath, 'Problems', p_name[:3], p_name)
            measurements = []
            for i in range(runs):
                LOGGER.info('Run %s / %s', i, runs)
                used_time = self.measure(p_strategy, p_path)
                measurements.append((p_time, abs(used_time - p_time), used_time / p_time))
                
            series.append(measurements)
	
        LOGGER.info('Finished CPU measurements')

        return series

    def load_or_gen_data(self):
        if self.ratios is not None:
            pass
    
        path = os.path.join(PATH, 'tuning')
    
        print path
        if os.path.isfile(path):
            with open(path, 'rb') as in_s:
                self.times = pickle.load(in_s)
        else:
            self.times = self.compare_cpu_with_data_set(3)
            with open(path, 'wb') as out_s:
                pickle.dump(self.times, out_s)

        self.ratios = []
        for measurements in self.times:
            measurements.sort(key=(lambda x : x[2]))
            #self.ratios.append(max(measurements, key=(lambda x : x[2])))
            self.ratios.extend(measurements)
        
        print self.ratios

    def get_ratio(self, time):
        if self.ratios is None:
            self.load_or_gen_data()
    
        leastDiff = 1000000
        bestRatio = None
        
        for p_time, diff_time, ratio in self.ratios:
            diff = abs(p_time - time)
            if diff < leastDiff:
                leastDiff = diff
                bestRatio = ratio
    
        return bestRatio
    

if __name__ == '__main__':
    cpu = CPU()
    cpu.load_or_gen_data()
    
    sys.exit(0)
