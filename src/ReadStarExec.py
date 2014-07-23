import os
import sys
import re

from src.DataSet import DataSet
from src.data_util import remove_unsolveable_problems
from src.GlobalVars import PATH, EPATH, LOGGER

try:
   import cPickle as pickle
except:
   import pickle

RX_TIME = re.compile(r"([0-9]+\.[0-9]+)/([0-9]+\.[0-9]+)	EOF")

if __name__ == '__main__':
    tuning_path = os.path.join(PATH, 'tuning')
    path = os.path.join(PATH, 'data', 'StarExec')
    
    if os.path.isfile(tuning_path):
        LOGGER.info('First delete tuning file before attempting to generate it by reading StarExec output')
        sys.exit(0)
    
    times = []
    for strategy_file in os.listdir(path):
        print strategy_file
    
        dataset = DataSet()
        dataset.whitelist = [strategy_file] # for faster loading
        
        dataset.load('E')
        dataset = remove_unsolveable_problems(dataset)
        
        strategy_i = list(dataset.strategy_files).index(strategy_file)
        
        for f in os.listdir(os.path.join(path, strategy_file)):
            fpath = os.path.join(path, strategy_file, f)
            if not os.path.isfile(fpath):
                continue
            
            if not f in dataset.problems:
                continue

            problem_i = list(dataset.problems).index(f)
            
            lastline = None
            with open(fpath, 'r') as inputstream:
                for line in inputstream:
                    lastline = line
            
            result = RX_TIME.match(lastline)
            assert(not result is None)
            used_time = float(result.groups()[0])
            print used_time
            if used_time >= 300.0:
                used_time = -1.0
            
            if used_time <= 0.0:
                continue
            
            p_time = dataset.strategy_matrix[problem_i][strategy_i]
            
            if p_time == -1.0:
                LOGGER.info("We solved " + f + " with " + str(used_time) + ", but PEGASUS did not")
                continue
            
            for time in times:
                print time
                
            times.append([(p_time, abs(used_time - p_time), used_time / p_time)])

    print len(times)
    with open(tuning_path, 'wb') as out_s:
        pickle.dump(times, out_s)
