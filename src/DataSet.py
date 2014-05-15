'''
Created on May 15, 2014

@author: Daniel Kuehlwein
'''

class DataSet(object):
    '''
    classdocs
    '''

    def __init__(self, data_type):
        '''
        Constructor
        '''
        self.feature_matrix = None
        self.strategy_matrix = None
        self.strategies = None
        self.problems = None
        self.data_type = data_type
        self.parse()
        
    def parse(self):
        if self.data_type == 'E':
            self.parse_E_data()
        else:
            raise IOError('Cannot parse unknown data type %s.' % self.data_type)
        
    def parse_E_data(self):
        raise NotImplementedError