'''
Contains all global variables that might be of use.

Created on May 9, 2014

@author: Daniel Kuehlwein
'''

import logging
import os
import sys


try:
    from signal import SIGKILL
except:
    SIGKILL = 9

PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
EPATH = os.path.join(PATH,'contrib','E','PROVER')

# TODO: Config Parser
"""
    atpConfig = ConfigParser.SafeConfigParser()
    atpConfig.optionxform = str
    atpConfig.read(args.ATP)
""" 

# TODO: Define logfile name
logFile = os.path.join(PATH,'log')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m %H:%M:%S',
                    filename=logFile,
                    filemode='w')
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
formatter = logging.Formatter('%% %(message)s')
console.setFormatter(formatter)    
LOGGER = logging.getLogger('')
LOGGER.addHandler(console)

