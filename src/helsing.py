"""
VanHElsing v0.1

Vampire watch out!
Creates a schedule based on the trained data
and runs the ATP with the schedule.

Created on May 14, 2014

@author: Sil van de Leemput
"""

import ConfigParser
import os
import sys
from time import time

from argparse import ArgumentParser
from RunATP import get_ATP_from_config
from src.schedulers import SchedulerTemplate
from src.GlobalVars import PATH, LOGGER

# TODO: Set up content of config.ini during installation
def load_config(config_file):
    if not os.path.exists(config_file):
        raise IOError(10, 'Cannot find configuration file %s' %
                      config_file)
    configuration = ConfigParser.SafeConfigParser()
    configuration.optionxform = str
    configuration.read(config_file)
    return configuration

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

    # TODO obtain from CLI
    problem = args.problem
    time_limit = args.time

    # start tracking time
    start_time = time()

    # init ATP TODO verify correctness
    atp = get_ATP_from_config(configuration)
    # print atp.run('--auto-schedule', 10, '../data/PUZ001+1.p')

    # init predictor from file or memory
    # ssm = StrategySchedulerModel()
    scheduler = SchedulerTemplate.StrategyScheduler(problem, time_limit, None)

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
        LOGGER.info("Problem {} solved in {}/{}".format(problem,
                                                        (time() - start_time),
                                                        time_limit))
    else:
        LOGGER.info("No solution found for Problem {} " +
                    "within time limit ({})".format(problem, time_limit))

if __name__ == '__main__':
    sys.exit(main())
