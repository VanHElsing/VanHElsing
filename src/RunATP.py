'''
Created on May 8, 2014

@author: Daniel Kuehlwein
'''

import os
from time import time
import IO
import re

from src.GlobalVars import LOGGER

# For matching /usr/bin/time
RX_TIME_USER = re.compile(r"user ([0-9]+\.[0-9]+)")

def get_ATP_from_config(configuration):  # NOQA, pylint: disable=C0103
    binary = configuration.get('ATP Settings', 'binary')
    time_str = configuration.get('ATP Settings', 'time')
    default = configuration.get('ATP Settings', 'default')
    return ATP(binary, time_str, default)


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

    def run(self, strategy, time_out, problem_file, measure_cpu_time=False):
        '''
        Run a command with a time_out after which it will be forcibly killed.
        '''
        if not os.path.exists(self.binary):
            raise IOError(10, 'Cannot find ATP binary %s' % self.binary)
        # TODO: time_string and round_time is E specific!
        rounded_time = int(time_out + 1.5)
        if self.time_string.endswith('='):
            time_string = self.time_string + str(rounded_time)
        else:
            time_string = self.time_string + ' ' + str(rounded_time)
        command = ' '.join([self.binary, self.default, strategy, time_string,
                            problem_file])
                            
        if measure_cpu_time:
            assert(os.name is "posix")
            command = '/usr/bin/time -p ' + command
        
        LOGGER.debug('Running %s', command)
        start_time = time()
        resultcode, stdout, stderr = IO.run_command(command, time_out)
        if resultcode < 0:
            return False, False, stdout, time() - start_time
            
        used_time = time() - start_time

        if measure_cpu_time:
            result = RX_TIME_USER.match(stderr.split("\n")[1])
            if result is None:
                print "Failed to execute, dumping stderr:"
                print stderr
                return False, False, stdout, time() - start_time

            used_time = float(result.groups()[0])
        
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
            if line.startswith('# SZS status Satisfiable') or \
               line.startswith('% SZS status Satisfiable'):
                countersat = True
            # CNF Theorem
            if line.startswith('# SZS status Unsatisfiable') or \
               line.startswith('% SZS status Unsatisfiable'):
                proof_found = True
            if line.startswith('# SZS status CounterSatisfiable') or \
               line.startswith('% SZS status CounterSatisfiable'):
                countersat = True
        return proof_found, countersat
