'''
General IO functions.

Created on May 9, 2014

@author: Daniel Kuehlwein
'''

import os
import subprocess
import shlex
from lib import TimeoutThread


def expand_filename(file_name):
    '''
    Tries to find file_name in both the local directory and the TPTP directory.
    If it finds a file, returns a working path.
    '''
    # Try local directory
    if os.path.isfile(file_name):
        return file_name
    # Try TPTP env
    TPTP = os.getenv('TPTP')  # NOQA, pylint: disable=C0103
    try:
        file_path = os.path.join(TPTP, file_name)
    except:
        raise IOError(11, ('Cannot find problem file %s and the TPTP ' +
                           'environment is not defined.') % file_name)
    if os.path.isfile(file_path):
        return file_path
    # Cannot find file
    raise IOError(12, 'Cannot find problem file %s or %s. ' %
                      (file_name, file_path))


def run_command(command, time_out):
    '''
    Runs command with a time_out and return the resultcode, stdout and stderr
    '''
    args = shlex.split(command)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, preexec_fn=os.setsid)
    # pylint: disable=E1101
    with TimeoutThread.processTimeout(time_out, proc.pid):
        stdout, stderr = proc.communicate()
    resultcode = proc.wait()
    return resultcode, stdout, stderr