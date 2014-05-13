'''
Created on May 8, 2014

@author: Daniel Kuehlwein
'''

import os
from time import time
import IO


class ATP(object):
    def __init__(self, binary, time_string, default=''):
        '''
        Example call:
        atp = ATP('eprover', '--cpu-limit=',
                  '--tstp-format -s --proof-object --memory-limit=2048')
        atp.run('--auto-schedule',10,PUZ001+1.p)
        '''
        self.binary = binary
        self.time_string = time_string
        self.default = default

    def run(self, strategy, time_out, problem_file):
        '''
        Run a command with a time_out after which it will be forcibly killed.
        '''
        if not os.path.exists(self.binary):
            raise IOError(10, 'Cannot find ATP binary %s' % self.binary)
        # TODO: time_string is E specific!
        time_string = self.time_string + str(time_out)
        command = ' '.join([self.binary, self.default, strategy, time_string,
                            problem_file])
        start_time = time()
        resultcode, stdout, _stderr = IO.run_command(command, time_out)
        if resultcode < 0:
            return False, False, None, self.run_time
        used_time = time() - start_time
        proof_found, countersat = self.parse_output(stdout)
        return proof_found, countersat, stdout, used_time

    def parse_output(self, output):
        '''
        Checks whether the ATP found a proof or a counterexample.
        '''
        proof_found = False
        countersat = False
        for line in output.split('\n'):
            # FOF - Theorem
            if line.startswith('# SZS status Theorem') or \
               line.startswith('% SZS status Theorem'):
                proof_found = True
            # CNF Theorem
            if line.startswith('# SZS status Unsatisfiable'):
                proof_found = True
            if line.startswith('# SZS status CounterSatisfiable') or \
               line.startswith('% SZS status CounterSatisfiable'):
                countersat = True
        return proof_found, countersat
