#! /usr/bin/env python
"""
VanHElsing v1.0

Vampire watch out!
Creates a schedule based on the trained data
and runs the ATP with the schedule.

Created on May 14, 2014

@author: Frank Dorssers, Wouter Geraedts, Sil van de Leemput
"""

import os
import sys
from time import time
from argparse import ArgumentParser

def set_up_parser():
    parser = ArgumentParser(description='Van HElsing 1.0 --- June 2014.')
    parser.add_argument('-t', '--time', help='Maximum runtime of Van HElsing.',
                        type=int)
    parser.add_argument('-p', '--problem', help='The location of the problem.')
    parser.add_argument('-c', '--configuration',
                        help='Which configuration file to use.')
    return parser


def adapt_run_time(pred_time, time_left, config):
    cpu = CPU()
    
    run_time = None
    if pred_time < 1.0:
        run_time = pred_time + 0.5
    else:
        ratio = cpu.get_ratio(pred_time)
        run_time = pred_time * ratio * 1.1
    return min(time_left, run_time)


def check_args(args):
    if args.time is None:
        LOGGER.error("No argument for time found.")
        sys.exit(-1)
    if args.problem is None:
        LOGGER.error("No argument for problem found.")
        sys.exit(-1)
    if args.configuration is None:
        LOGGER.error("No argument for configuration found.")
        sys.exit(-1)


def main(argv=sys.argv[1:]):
    parser = set_up_parser()
    args = parser.parse_args(argv)
    check_args(args)
    configuration = load_config(args.configuration)

    # start tracking time
    start_time = time()

    atp = get_ATP_from_config(configuration)
    scheduler_file = configuration.get('Scheduler', 'modelfile')
    scheduler = init_scheduler(args.problem, scheduler_file)

    # main loop
    proof_found = False
    time_left = args.time - (time() - start_time)
    while (not proof_found) and time_left > 0:
        strat, strat_time = scheduler.predict(time_left)
        #run_time = adapt_run_time(strat_time, time_left, configuration)
        run_time = min(time_left, strat_time)
        LOGGER.info("Running %s for %s seconds" % (strat, strat_time))
        proof_found, _cs, output, _used_time = atp.run(strat, run_time,
                                                       args.problem)
        if not proof_found:
            scheduler.update()
            time_left = args.time - (time() - start_time)

    if proof_found:
        LOGGER.info("\n" + output)
        return True
    LOGGER.info("SZS status Timeout")
    return False

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

    from src.GlobalVars import PATH, LOGGER
    from src.IO import load_config
    from src.RunATP import get_ATP_from_config
    from src.schedulers.util import init_scheduler
    from src.CPU import CPU

    sys.exit(main())
