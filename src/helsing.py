#! /usr/bin/env python
"""
VanHElsing v1.0

Creates a schedule based on the trained data and runs
the ATP with the schedule.

@author: Frank Dorssers, Wouter Geraedts, Daniel Kuehlwein, Sil van de Leemput
"""

import argparse as ap
import os
import sys
from time import time


def set_up_parser():
    '''
    Initializes parser.

    Returns
    -------
    Parser : ArgumentParser
        Initialized ArgumentParser which contains relevant arguments
    '''
    parser = ap.ArgumentParser(description="""
Van HElsing 1.0 --- June 2014

Runs an ATP on the problem p with a strategy schedule predicted with
the model defined in the configuration c for the time limit t.

Created by Frank Dorssers, Wouter Geraedts, Daniel Kuehlwein
and Sil van de Leemput
                               """, formatter_class=ap.RawTextHelpFormatter)
    parser.add_argument('-t', '--time', help='Maximum runtime of Van HElsing.',
                        type=int)
    parser.add_argument('-p', '--problem', help='The location of the problem.')
    parser.add_argument('-c', '--configuration',
                        help='Which configuration file to use.')
    return parser


def check_args(args):
    '''
    Verifies the existence of the expected arguments.

    Parameters
    ----------
    args : Arguments
        Should contain arguments for the time, problem and configuration
    '''
    if args.time is None:
        LOGGER.error("No argument for time found.")
        sys.exit(-1)
    if args.problem is None:
        LOGGER.error("No argument for problem found.")
        sys.exit(-1)
    if args.configuration is None:
        LOGGER.error("No argument for configuration found.")
        sys.exit(-1)


def helsing(argv):
    '''
    Main function for VanHElsing.
    Runs an ATP on the problem $p$ with a strategy schedule predicted with
    the model defined in the configuration $c$ for the time limit $t$.

    Inputs (command line)
    ---------------------
    c : Configuration file
    t : Time limit
    p : Problem file

    Returns
    -------
    Result : boolean
        True if a proof has been found
    '''
    parser = set_up_parser()
    args = parser.parse_args(argv)
    check_args(args)
    configuration = load_config(args.configuration)

    # start tracking time
    start_time = time()

    atp = get_ATP_from_config(configuration)
    scheduler_file = configuration.get('Scheduler', 'modelfile')
    scheduler = init_scheduler(args.problem, scheduler_file)

    # Main loop: Predict and run strategies until no time is left.
    proof_found = False
    time_left = args.time - (time() - start_time)
    while (not proof_found) and time_left > 0:
        strat, strat_time = scheduler.predict(time_left)
        run_time = min(time_left, strat_time)
        LOGGER.info("Running %s for %s seconds", strat, strat_time)
        proof_found, _cs, output, _time = atp.run(strat, run_time,
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
    from src.GlobalVars import LOGGER
    from src.IO import load_config
    from src.RunATP import get_ATP_from_config
    from src.schedulers.util import init_scheduler

    sys.exit(helsing(sys.argv[1:]))
