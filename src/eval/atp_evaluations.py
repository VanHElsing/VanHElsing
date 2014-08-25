'''
Created on May 17, 2014

@author: Daniel Kuehlwein
'''

import multiprocessing as mp
import os
from src.GlobalVars import PATH, EPATH
from src.RunATP import ATP


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
    # atp = ATP(path, '-t ', '-c /home/daniel/workspace/VanHElsing/src/satallax.ini')
    atp = ATP(path, '-t ', '-c config.ini')
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


def run_satallax(args):
    # satallax.opt -t %d %s
    problem_file, time_limit = args
    # Hack
    path = os.path.join('/home/daniel/workspace/starexec/install/satallax-2.7/bin', 'satallax.opt')
    atp = ATP(path, '-t', '')
    proof_found, _cs, _out, used_time = atp.run('', time_limit,
                                                problem_file)
    return problem_file, proof_found, used_time


def load_problems(problem_file):
    problems = []
    tptp_dir = os.getenv('TPTP')
    with open(problem_file, 'r') as p_stream:
        for p in p_stream:
            problems.append(os.path.join(tptp_dir, p.strip()))
    return problems
    
    
def atp_eval_problems(problems, prover, run_time, outfile=None, cores=None):
    if outfile is None:
        os.path.join(PATH, 'runs', 'atp_eval')
    if cores is None:
        cores = mp.cpu_count()
    if prover == 'E':
        prover_call = run_e_auto
    elif prover == 'satallax':
        prover_call = run_satallax
    elif prover == 'helsing':
        prover_call = run_helsing
    elif prover == 'emales':
        prover_call = run_emales

    print len(problems)
    with open(outfile, 'w') as out_stream:
        pool = mp.Pool(processes=cores)
        
        args = [[p, run_time] for p in problems]
        results = pool.map_async(prover_call, args)
        pool.close()
        pool.join()
        results.wait()
        results = results.get()
        
        proofsFound = 0
        for problem, proofFound, usedTime in results:
            if proofFound:
                out_stream.write('%s,%s\n' % (problem, usedTime))
                proofsFound = proofsFound + 1
        
        return proofsFound / float(len(results))


def atp_eval(problem_file, prover, run_time, outfile=None, cores=None):
    problems = load_problems(problem_file)
    return atp_eval_problems(problems, prover, run_time, outfile, cores)
