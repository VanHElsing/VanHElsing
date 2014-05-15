'''
Contains all global variables that might be of use.

Created on May 9, 2014

@author: Daniel Kuehlwein
'''

import logging
import os
import sys


try:
    from signal import SIGKILL  # unused import, pylint: disable=W0611
except ImportError:
    SIGKILL = 9

PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
EPATH = os.path.join(PATH, 'contrib', 'E', 'PROVER')

# TODO: Define logfile name
LOGFILE = os.path.join(PATH, 'log')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s' +
                           '%(message)s',
                    datefmt='%d-%m %H:%M:%S',
                    filename=LOGFILE,
                    filemode='w')
FORMATTER = logging.Formatter('%% %(message)s')
CONSOLE = logging.StreamHandler(sys.stdout)
CONSOLE.setLevel(logging.INFO)
CONSOLE.setFormatter(FORMATTER)
LOGGER = logging.getLogger('')
# TODO: Better check if CONSOLE is already a handler
if len(LOGGER.handlers) < 2:
    LOGGER.addHandler(CONSOLE)
