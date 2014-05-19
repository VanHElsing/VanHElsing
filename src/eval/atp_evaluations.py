'''
Created on May 17, 2014

@author: daniel
'''

import multiprocessing as mp
import os

from src.GlobalVars import PATH, EPATH
from src.RunATP import ATP


"""
#TODO: Is this necessary?
class NoDaemonProcess(mp.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class MyPool(mp.pool.Pool):
    Process = NoDaemonProcess
#End TODO
"""

def run_e_auto(args):
    problem_file, time_limit = args
    eprover_path = os.path.join(EPATH, 'eprover')
    atp = ATP(eprover_path, '--cpu-limit=',
              '--tstp-format -s --proof-object --memory-limit=2048')
    proof_found, _countersat, _stdout, used_time = atp.run('--auto-schedule', time_limit, problem_file)
    return problem_file, proof_found, used_time

def run_helsing(args):
    problem_file, time_limit = args
    eprover_path = os.path.join(PATH, 'src', 'helsing.py')
    atp = ATP(eprover_path, '-t ', '')
    #TODO: Get rid of this -p hack
    proof_found, _countersat, _stdout, used_time = atp.run('', time_limit, '-p '+problem_file)
    return problem_file, proof_found, used_time

def load_problems(problem_file):
    problem_file = 'PUZ001+1.p'
    p_file_extended = os.path.join(PATH, 'data', problem_file)
    return [p_file_extended]

def atp_eval(problem_file, prover, run_time, outfile=None, cores=None):
    if outfile is None:
        os.path.join(PATH, 'runs', 'atp_eval')
    if cores is None:
        cores = mp.cpu_count()
    if prover == 'E':
        prover_call = run_e_auto
    elif prover == 'helsing':
        prover_call = run_helsing
    problems = load_problems(problem_file)
    with open(outfile, 'w') as OS:
        #pool = MyPool(processes = cores)
        pool = mp.Pool(processes=cores)
        args = [[p, run_time] for p in problems]
        results = pool.map_async(prover_call, args)
        pool.close()
        pool.join()
        results.wait()
        results = results.get()
        for problem, proofFound, usedTime in results:
            if proofFound:
                OS.write('%s,%s\n' % (problem, usedTime))

if __name__ == '__main__':
    cores = 1
    outfile = 'atp_eval'
    problem_file = os.path.join(PATH, 'data', 'E_eval', 'CASC24Training')
    prover = 'E'
    run_time = 300
    atp_eval(problem_file, prover, run_time, outfile, cores)

# TODO: Take E-MaLeS 1.2 test problems. Run ATP over them. Store and compare.
