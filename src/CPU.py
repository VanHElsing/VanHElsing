'''
Created on May 18, 2014

@author: daniel
'''

import os
import sys
from time import time

from src.GlobalVars import PATH, EPATH, LOGGER
from src.RunATP import ATP

try:
   import cPickle as pickle
except:
   import pickle

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

    def compare_cpu_with_data_set(self, runs=10):
        """
        Compares the data set run times of E with the real run times.
        Protokoll_G-E--_008_C18_F1_PI_SE_CS_SP_CO_S4S is used as baseline.
        Parameters: --definitional-cnf=24 --tstp-in --condense --simul-paramod --forward-context-sr --strong-destructive-er --destructive-er-aggressive --destructive-er --prefer-initial-clauses -tKBO6 -winvfreqrank -c1 -Ginvfreq -F1 -s --delete-bad-limit=1024000000 -WSelectNewComplexAHPNS -H'(10*ConjectureRelativeSymbolWeight(ConstPrio,0.1, 100, 100, 100, 100, 1.5, 1.5, 1.5),1*FIFOWeight(ConstPrio))'
        Problem 1: AGT004+1.p 0.065000
        Problem 2: AGT003+1.p 1.573000
        Problem 3: SEU008+1.p 9.783000
        Problem 4: GRP390-1.p 27.243000
        Problem 5: SWC089-1.p 99.398000
        """

        TPTPPath = os.getenv('TPTP')
        if TPTPPath is None:
            raise IOError('$TPTP is not defined.')

        test_data = []
        test_data.append(('AGT004+1.p', 0.065000))
        test_data.append(('AGT003+1.p', 1.573000))
        test_data.append(('SEU008+1.p', 9.783000))
        test_data.append(('GRP390-1.p', 27.243000))
        test_data.append(('SWC089-1.p', 99.398000))
            
        strategy = "--definitional-cnf=24 --tstp-in --condense --simul-paramod --forward-context-sr --strong-destructive-er --destructive-er-aggressive --destructive-er --prefer-initial-clauses -tKBO6 -winvfreqrank -c1 -Ginvfreq -F1 -s --delete-bad-limit=1024000000 -WSelectNewComplexAHPNS -H'(10*ConjectureRelativeSymbolWeight(ConstPrio,0.1, 100, 100, 100, 100, 1.5, 1.5, 1.5),1*FIFOWeight(ConstPrio))'"

        series = []
        LOGGER.info('Starting CPU measurements')
        for p_name, p_time in test_data:
            LOGGER.info('Problem %s', p_name)
            p_path = os.path.join(TPTPPath, 'Problems', p_name[:3], p_name)
            measurements = []
            for i in range(runs):
                LOGGER.info('Run %s / %s', i, runs)
                used_time = self.measure(strategy, p_path)
                measurements.append((used_time, abs(used_time - p_time), used_time / p_time))
                
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
            self.times = self.compare_cpu_with_data_set(10)
            with open(path, 'wb') as out_s:
                pickle.dump(self.times, out_s)
    
        self.ratios = []
        for measurements in self.times:
            self.ratios.append(max(measurements, key=(lambda x : x[2])))
        
        print self.ratios

    def get_ratio(self, time):
        if self.ratios is None:
            self.load_or_gen_data()
    
        leastDiff = 1000000
        bestRatio = None
        
        for used_time, diff_time, ratio in self.ratios:
            diff = abs(used_time - time)
            if diff < leastDiff:
                leastDiff = diff
                bestRatio = ratio
    
        return bestRatio
    

if __name__ == '__main__':
    cpu = CPU()
    cpu.load_or_gen_data()
    
    sys.exit(0)
