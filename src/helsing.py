#! /usr/bin/env python
"""
VanHElsing v0.1

Vampire watch out!
Creates a schedule based on the trained data
and runs the ATP with the schedule.

Created on May 14, 2014

@author: Sil van de Leemput
"""

import os
import sys
from time import time

from argparse import ArgumentParser
from src.GlobalVars import PATH, LOGGER
from src.IO import load_config
from src.RunATP import get_ATP_from_config
from src.schedulers.util import init_scheduler


def set_up_parser():
    parser = ArgumentParser(description='Van HElsing 0.1 --- May 2014.')
    parser.add_argument('-t', '--time', help='Maximum runtime of Van HElsing.',
                        type=int, default=10)
    parser.add_argument('-p', '--problem', help='The location of the problem.',
                        default=os.path.join(PATH, 'data/PUZ001+1.p'))
    parser.add_argument('-c', '--configuration',
                        help='Which configuration file to use.',
                        default=os.path.join(PATH, 'config.ini'))
    return parser


def main(argv=sys.argv[1:]):
    parser = set_up_parser()
    args = parser.parse_args(argv)
    configuration = load_config(args.configuration)

    # start tracking time
    start_time = time()

    # init ATP TODO verify correctness
    atp = get_ATP_from_config(configuration)
    scheduler_file = configuration.get('Scheduler', 'modelfile')
    scheduler = init_scheduler(args.problem, scheduler_file)

    # main loop
    proof_found = False
    time_left = args.time - (time() - start_time)
    while not proof_found and time_left > 0:
        strat, strat_time = scheduler.predict(time_left)
        # TODO: Check this here or in the scheduler?
        run_time = min(time_left, strat_time)
        proof_found, _cs, _stdout, _used_time = atp.run(args.problem,
                                                        run_time, strat)
        print _stdout
        if not proof_found:
            scheduler.update()
            time_left = args.time - (time() - start_time)

    # TODO output results
    if proof_found:
        LOGGER.info("Problem %s solved in %f/%f",
                    args.problem, (time() - start_time), args.time)
        return True
    else:
        LOGGER.info("No solution found for Problem %s within time limit (%f)",
                    args.problem, args.time)
        return False

if __name__ == '__main__':
    sys.exit(main())
