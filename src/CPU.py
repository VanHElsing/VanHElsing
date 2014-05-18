'''
Created on May 18, 2014

@author: daniel
'''

import numpy as np
import os
from time import time
from src.GlobalVars import EPATH, LOGGER
from src.RunATP import ATP


def compare_cpu_with_data_set(runs = None):
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

    if runs is None:
        runs = 10
    strategy = "--definitional-cnf=24 --tstp-in --condense --simul-paramod --forward-context-sr --strong-destructive-er --destructive-er-aggressive --destructive-er --prefer-initial-clauses -tKBO6 -winvfreqrank -c1 -Ginvfreq -F1 -s --delete-bad-limit=1024000000 -WSelectNewComplexAHPNS -H'(10*ConjectureRelativeSymbolWeight(ConstPrio,0.1, 100, 100, 100, 100, 1.5, 1.5, 1.5),1*FIFOWeight(ConstPrio))'"
    eprover_path = os.path.join(EPATH, 'eprover')
    atp = ATP(eprover_path, '--cpu-limit=', '--tstp-format -s --proof-object --memory-limit=2048')

    test_times = []
    test_times_diff = []
    LOGGER.info('Starting CPU measurements')
    for p_name, p_time in test_data[:2]:
        LOGGER.info('Problem %s', p_name)        
        p_path = os.path.join(TPTPPath, 'Problems', p_name[:3], p_name)
        measured_times = []
        measured_times_diff = []
        for i in range(runs):
            LOGGER.info('Run %s / %s', i, runs)
            start_time = time() 
            proof_found, _cs, _o, _used_time = atp.run(strategy, 200, p_path)
            assert proof_found    
            used_time = time() - start_time
            measured_times.append(used_time)
            measured_times_diff.append(abs(used_time - p_time))
        test_times.append(measured_times)
        test_times_diff.append(measured_times_diff)
    LOGGER.info('Finished CPU measurements')

    print np.mat(test_times)
    print np.mat(test_times_diff)
compare_cpu_with_data_set()