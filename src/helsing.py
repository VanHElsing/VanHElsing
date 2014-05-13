"""
VanHElsing v0.1

Vampire watch out!
Creates a schedule based on the trained data
and runs the ATP with the schedule.

Created on May 14, 2014

@author: Sil van de Leemput
"""

from RunATP import ATP
from StrategyScheduler import StrategyScheduler
from time import time


def run():
    # TODO obtain from CLI
    problem = "something"
    time_limit = 300

    # start tracking time
    start_time = time()

    # init ATP TODO verify correctness
    atp = ATP('eprover', '--cpu-limit=',
              '--tstp-format -s --proof-object --memory-limit=2048')

    # init predictor from file or memory
    # ssm = StrategySchedulerModel()
    scheduler = StrategyScheduler(problem, time_limit, None)

    # main loop
    proof_found = False
    time_left = time_limit - (time() - start_time)
    while not proof_found and time_left > 0:
        strat, strat_time = scheduler.predict(time_left)
        proof_found, _cs, _stdout, _used_time = atp.run('--auto-schedule',
                                                        strat_time, strat)
        if not proof_found:
            scheduler.update()
            time_left = time_limit - (time() - start_time)

    # TODO output results
    if proof_found:
        print "Problem {} solved in {}/{}".format(problem,
                                                  (time() - start_time),
                                                  time_limit)
    else:
        print "No solution found for Problem {} " + \
              "within time limit ({})".format(problem, time_limit)

if __name__ == '__main__':
    run()
