"""
VanHElsing v0.1

Vampire watch out!
Creates a schedule based on the trained data and runs the ATP with the schedule.

Created on May 14, 2014

@author: Sil van de Leemput
"""

from RunATP import RunATP
from StrategyScheduler import StrategyScheduler
from StrategySchedulerModel import StrategySchedulerModel

if __name__ == '__main__':  
    # TODO obtain from CLI
    problem = "something"
    time_limit = 300

    # start tracking time
    start_time = time()

    # init ATP TODO verify correctness
    atp = RunATP('eprover','--cpu-limit=','--tstp-format -s --proof-object --memory-limit=2048')        
    
    # init predictor from file or memory
    SSM = StrategySchedulerModel()
    SS = StrategyScheduler(prob, time_limit, SSM)

    # main loop
    proofFound = False
    time_left =  time_limit - (time() - start_time)
    while not proofFound and time_left > 0:
        strat, t = SS.predict(time_left)
        proofFound, countersat, stdout, usedTime = atp.run('--auto-schedule', t, strat)
        if not proofFound:
            SS.update()
            time_left = time_limit - (time() - start_time)

    # TODO output results
    if proofFound:
        print "Problem {} solved in {}/{}".format(problem, (time() - start_time), time_limit)
    else:
        print "No solution found for Problem {} within time limit ({})".format(problem, time_limit)