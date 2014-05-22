'''
Created on May 22, 2014

@author: Daniel Kuehlwein
'''

import os
from src.GlobalVars import PATH
from src.eval.atp_evaluations import atp_eval

CORES = 1
PROVER = 'emales'
RUNTIME = 300
OUT = 'atp_eval_CASC_Training_E1.8'
PROBLEMS = os.path.join(PATH, 'data', 'E_eval', 'CASC24Training')
atp_eval(PROBLEMS, PROVER, RUNTIME, OUT, CORES)

Outfile = 'atp_eval_CASC_Test_E1.8'
PROBLEMS = os.path.join(PATH, 'data', 'E_eval', 'CASC24Test')
atp_eval(PROBLEMS, PROVER, RUNTIME, OUT, CORES)
