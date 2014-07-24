import os
import sys
import re

from src.CPU import CPU

from src.DataSet import DataSet
from src.data_util import remove_unsolveable_problems
from src.GlobalVars import PATH, EPATH, LOGGER

import matplotlib.pylab as pl

try:
   import cPickle as pickle
except:
   import pickle

RX_TIME = re.compile(r"([0-9]+\.[0-9]+)/([0-9]+\.[0-9]+)	EOF")

if __name__ == '__main__':
    benchmark_path = os.path.join(PATH, 'benchmark_starexec')
    path = os.path.join(PATH, 'data', 'StarExec')
    TPTPPath = os.getenv('TPTP')
    
    cpu = CPU()
    #cpu.load_or_gen_data()
    
    if not os.path.isfile(benchmark_path):
        series = []
        for strategy_file in os.listdir(path):
            spath = os.path.join(path, strategy_file)
        
            dataset = DataSet()
            dataset.whitelist = [strategy_file] # for faster loading
            
            dataset.load('E')
            dataset = remove_unsolveable_problems(dataset)
            
            strategy_i = list(dataset.strategy_files).index(strategy_file)
            strategy = dataset.strategies[strategy_i]

            times = []
            for f in os.listdir(spath):
                fpath = os.path.join(spath, f)
                if not os.path.isfile(fpath):
                    continue
                
                p_path = os.path.join(TPTPPath, 'Problems', f[:3], f)
                
                lastline = None
                with open(fpath, 'r') as inputstream:
                    for line in inputstream:
                        lastline = line
                
                result = RX_TIME.match(lastline)
                assert(not result is None)
                used_time = float(result.groups()[0])
                
                if used_time >= 300.0:
                    used_time = -1.0
                
                if used_time <= 3.0:
                    continue
                
                real_time = cpu.measure(strategy, p_path)
                
                if real_time == -1:
                    print 'Did not finish within time limit'
                    continue
                
                print 'Finished %s in %f' % (p_path, real_time)
                    
                times.append((real_time, abs(used_time - real_time), used_time / real_time, f))
            
            series.append((strategy_file, times))

        with open(benchmark_path, 'wb') as out_s:
            pickle.dump(series, out_s)
    else:
        with open(benchmark_path, 'rb') as in_s:
            series = pickle.load(in_s)
    
    pl.figure("StarExec comparison to current machine")
    for strategy_file, times in series:
        times.sort(key=lambda x : x[0])
        print times
        pl.plot(map(lambda x : x[0], times), map(lambda x : x[2] * x[0], times))
    
    pl.show()
