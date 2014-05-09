'''
Contains general IO functions.

Created on May 9, 2014

@author: Daniel Kuehlwein
'''

import os
import subprocess
import shlex
import TimeoutThread

def expand_filename(fileName):
    '''
    Tries to find filename in both the local directory and the TPTP directory.
    If it finds a file, returns a working path.  
    '''
    # Try local directory
    if os.path.isfile(fileName):
        return fileName
    # Try TPTP env
    TPTP = os.getenv('TPTP')
    try:
        TPTPfileName = os.path.join(TPTP,fileName)
    except:
        raise IOError(11,'Cannot find problem file %s and the TPTP environment is not defined.' % fileName)
    if os.path.isfile(TPTPfileName):
        return TPTPfileName
    # Cannot find file
    raise IOError(12,'Cannot find problem file %s or %s. ' % (fileName,TPTPfileName))

def run_command(command,timeOut):
    '''
    Runs command with a timeOut and return the resultcode, stdout and stderr
    '''
    args = shlex.split(command)
    p = subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,preexec_fn=os.setsid)    
    with TimeoutThread.processTimeout(timeOut, p.pid):
        stdout, stderr = p.communicate()        
    resultcode = p.wait()
    return resultcode, stdout, stderr
