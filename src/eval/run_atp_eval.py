'''
Created on May 22, 2014

@author: Daniel Kuehlwein
'''

import os
from src.GlobalVars import PATH
from src.eval.atp_evaluations import atp_eval

CORES = 8
PROVER = 'helsing'
RUNTIME = 305
OUT = 'runs/real/atp_eval_CASC_Training_Group1_DT_001'
PROBLEMS = os.path.join(PATH, 'data', 'E', 'CASC24Training')
#PROBLEMS = os.path.join(PATH, 'data', 'Satallax', 'CASC24Training')
atp_eval(PROBLEMS, PROVER, RUNTIME, OUT, CORES)

"""
OUT = 'atp_eval_CASC_Test_E1.8'
PROBLEMS = os.path.join(PATH, 'data', 'E_eval', 'CASC24Test')
atp_eval(PROBLEMS, PROVER, RUNTIME, OUT, CORES)
"""