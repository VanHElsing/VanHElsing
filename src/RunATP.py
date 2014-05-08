'''
Created on May 8, 2014

@author: Daniel Kuehlwein
'''

import shlex,subprocess,os
from time import time
from TimeoutThread import processTimeout


class RunATP(object):
    def __init__(self,binary,timeString,default = ''):
        '''
        Example call:
        atp = RunATP('eprover','--cpu-limit=','--tstp-format -s --proof-object --memory-limit=2048')
        atp.run('--auto-schedule',10,PUZ001+1.p)
        '''
        self.binary = binary
        self.timeString = timeString
        self.default = default
    
    def run(self,strategy,timeLimit,problemFile):
        '''
        Run a command with a timeout after which it will be forcibly
        killed.
        '''
        if not os.path.exists(self.binary):
            raise IOError(10,'Cannot find ATP binary %s' % self.binary)
        # TODO: timeString is E specific!
        timeString = self.timeString + str(timeLimit)
        command = ' '.join([self.binary,self.default,strategy,timeString,problemFile])
        args = shlex.split(command)        
        startTime = time()
        self.process = subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,preexec_fn=os.setsid)
        with processTimeout(timeLimit, self.process.pid):
            stdout, _stderr = self.process.communicate()        
        resultcode = self.process.wait()
        if resultcode < 0:
            return False,False,None,self.runTime
        usedTime = time() - startTime
        proofFound,countersat = self.parse_output(stdout)
        return proofFound,countersat,stdout,usedTime 
    
    def parse_output(self,output):
        '''
        Checks whether the ATP found a proof or a counterexample.
        '''
        proofFound = False
        countersat = False
        for line in output.split('\n'):
            # FOF - Theorem
            if line.startswith('# SZS status Theorem') or line.startswith('% SZS status Theorem') :
                    proofFound = True
            # CNF Theorem 
            if line.startswith('# SZS status Unsatisfiable'):
                    proofFound = True
            if line.startswith('# SZS status CounterSatisfiable') or line.startswith('% SZS status CounterSatisfiable'):
                    countersat = True
        return proofFound,countersat


    
if __name__ == '__main__':  
    from os.path import realpath,dirname
    testDir = dirname(dirname(realpath(__file__)))    
    problemFile = 'PUZ001+1.p'
    pFileExtended = os.path.join(testDir,'data',problemFile)
    print pFileExtended
    
    #eprover --auto-schedule --tstp-format -s --proof-object --memory-limit=2048 --cpu-limit=%d %s  
    atp = RunATP('/home/daniel/TPTP/E1.8/PROVER/eprover','--cpu-limit=','--tstp-format -s --proof-object --memory-limit=2048')
    print atp.run('--auto-schedule',10,pFileExtended)
    