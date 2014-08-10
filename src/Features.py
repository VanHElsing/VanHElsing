'''
Feature functions for both THF and FOF problems.

@author: Daniel Kuehlwein
'''

import os
from src import IO
from src import GlobalVars


def get_feature_function(config):
    '''
    Loads the feature function corresponding to the config settings.
    '''
    if config is None:
        feature_type = 'E'
    else:
        feature_type = config.get('ATP Settings', 'features')
    
    if feature_type == 'E':
        return EFeatures()
    if feature_type == 'TPTP':
        return TPTPFeatures()
    else:
        raise IOError('Unknown feature type %s', feature_type)


class Features(object):
    '''
    Meta class for feature computations.
    '''
    def __init__(self):
        self.binary = None
        self.args = None
        self.filename = None

    def get(self, filename, time_out=300):
        '''
        Return the features of the problem at filename
        '''
        self.filename = IO.expand_filename(filename)
        binary = os.path.join(GlobalVars.PATH, self.binary)
        command = ' '.join([binary, self.args, self.filename])
        resultcode, stdout, _stderr = IO.run_command(command, time_out)
        if resultcode < 0:
            raise IOError(10, 'Could not compute features. ' +
                          'Try running %s' % command)
        return self.parse_output(stdout)

    def parse_output(self, output):
        '''
        Transforms the stdout output of the feature function into a
        real-valued feature vector.
        '''
        raise NotImplementedError


class EFeatures(Features):
    '''
    Feature function for first order problems.
    '''
    def __init__(self):
        Features.__init__(self)

        self.binary = os.path.join('contrib', 'E', 'PROVER',
                                   'classify_problem')
        self.args = '-caaaaaaaaaaaaa --tstp-in'

    def parse_output(self, output):
        features = []
        for line in output.split('\n'):
            if not line.startswith(self.filename):
                continue
            line = line.split('(')[1]
            line = line.split(')')[0]
            features_str = line.split(',')
            for i in features_str:
                features.append(float(i))
        return features


class TPTPFeatures(Features):
    '''
    Feature function for higher order problems.
    '''
    def __init__(self):
        Features.__init__(self)

        self.binary = os.path.join('bin', 'TPTP_features')
        self.args = '-i'

    def parse_output(self, output):
        features = []
        for line in output.split('\n'):
            line = line.split()
            for word in line:
                try:
                    features.append(float(word))
                except ValueError:
                    continue
        return features
