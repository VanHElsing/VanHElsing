"""
VanHElsing v0.1

Vampire watch out!
Creates a schedule based on the trained data and runs the ATP with the schedule.

Created on May 14, 2014

@author: Sil van de Leemput
"""

import ConfigParser
import os
import sys
from time import time

from argparse import ArgumentParser
from globalVars import LOGGER,PATH
from RunATP import get_ATP_from_config
from src.schedulers import StrategyScheduler

parser = ArgumentParser(description='Van HElsing 0.1 --- May 2014.')
parser.add_argument('-t','--time',help='Maximum runtime of Van HElsing.',type=int,default=10)
parser.add_argument('-p','--problem',help='The location of the problem.',default = os.path.join(PATH,'data/PUZ001+1.p'))
parser.add_argument('-c','--configuration',help='Which configuration file to use.',default = os.path.join(PATH,'config.ini'))

# TODO: Set up content of config.ini during installation
def load_config(configFile):
    configuration = ConfigParser.SafeConfigParser()
    configuration.optionxform = str
    configuration.read(configFile)    
    return configuration

def main(argv = sys.argv[1:]):
    args = parser.parse_args(argv)
    if not os.path.exists(args.configuration):
        raise IOError(10,'Cannot find configuration file %s' % args.configuration)
    configuration = load_config(args.configuration)

    # TODO obtain from CLI
    problem = args.problem
    time_limit = args.time

    # start tracking time
    start_time = time()

    # init ATP TODO verify correctness
    atp = get_ATP_from_config(configuration)        
    #print atp.run('--auto-schedule', 10, '../data/PUZ001+1.p')
    
    # init predictor from file or memory
    #SSM = StrategySchedulerModel()
    SS = StrategyScheduler(problem, time_limit, None)

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
        LOGGER.info("Problem {} solved in {}/{}".format(problem, (time() - start_time), time_limit))
    else:
        LOGGER.info("No solution found for Problem {} within time limit ({})".format(problem, time_limit))
        
if __name__ == '__main__':
    sys.exit(main())        