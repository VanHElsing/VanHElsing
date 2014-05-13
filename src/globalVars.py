'''
Contains all global variables that might be of use.

Created on May 9, 2014

@author: Daniel Kuehlwein
'''

import ConfigParser
import logging
import os
import sys


try:
    from signal import SIGKILL
except:
    SIGKILL = 9

PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
EPATH = os.path.join(PATH,'contrib','E','PROVER')

# TODO: Set up content of config.ini during installation
CONFIG = ConfigParser.SafeConfigParser()
CONFIG.optionxform = str
CONFIG.read(os.path.join(PATH,'config.ini'))
 
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

