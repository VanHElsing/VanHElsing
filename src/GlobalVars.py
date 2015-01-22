'''
Contains all global variables for VanHElsing.
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
LOGFILE = os.path.join(PATH, 'log')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s' +
                    '%(message)s',
                    datefmt='%d-%m %H:%M:%S',
                    filename=LOGFILE,
                    filemode='w')
FORMATTER = logging.Formatter('%% %(message)s')
CONSOLE = logging.StreamHandler(sys.stdout)
CONSOLE.setLevel(logging.INFO)
CONSOLE.setFormatter(FORMATTER)
LOGGER = logging.getLogger('VanHElsing')
if CONSOLE not in LOGGER.handlers:
    LOGGER.addHandler(CONSOLE)
