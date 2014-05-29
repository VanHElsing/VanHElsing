'''
Created on May 17, 2014

@author: Daniel Kuehlwein
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
    path = os.path.join(EPATH, 'eprover')
    atp = ATP(path, '--cpu-limit=',
              '--tstp-format -s --proof-object --memory-limit=2048')
    proof_found, _cs, _out, used_time = atp.run('--auto-schedule', time_limit,
                                                problem_file)
    return problem_file, proof_found, used_time


def run_helsing(args):
    problem_file, time_limit = args
    path = os.path.join(PATH, 'src', 'helsing.py')
    atp = ATP(path, '-t ', '')
    # TODO: Get rid of this -p hack
    proof_found, _cs, _out, used_time = atp.run('', time_limit,
                                                '-p ' + problem_file)
    return problem_file, proof_found, used_time


def run_emales(args):
    problem_file, time_limit = args
    # TODO: HACK!
    path = os.path.join('/scratch/kuehlwein/males/MaLeS', 'males.py')
    atp = ATP(path, '-t ', '')
    # TODO: Get rid of this -p hack
    proof_found, _cs, _out, used_time = atp.run('', time_limit,
                                                '-p ' + problem_file)
    return problem_file, proof_found, used_time


def load_problems(problem_file):
    problems = []
    tptp_dir = os.getenv('TPTP')
    with open(problem_file, 'r') as p_stream:
        for p in p_stream:
            problems.append(os.path.join(tptp_dir, p.strip()))
    return problems


def atp_eval(problem_file, prover, run_time, outfile=None, cores=None):
    if outfile is None:
        os.path.join(PATH, 'runs', 'atp_eval')
    if cores is None:
        cores = mp.cpu_count()
    if prover == 'E':
        prover_call = run_e_auto
    elif prover == 'helsing':
        prover_call = run_helsing
    elif prover == 'emales':
        prover_call = run_emales
    problems = load_problems(problem_file)
    with open(outfile, 'w') as OS:
        # pool = MyPool(processes = cores)
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
