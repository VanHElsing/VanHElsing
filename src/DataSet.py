'''
Created on May 15, 2014

@author: Daniel Kuehlwein
'''

from os import listdir
from os.path import isfile, join
import numpy as np

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
            raise IOError('Cannot parse unknown data type %s.'
                          % self.data_type)

    def parse_E_data(self):  # NOQA
        sdict = self.load_strategies()
        fdict = self.load_features(sdict)
        self.feature_matrix = self.generate_feature_matrix(fdict)
        self.strategy_matrix = self.generate_strategy_matrix(fdict)
        self.strategies = self.get_strategy_file_names()
        self.problems = fdict.keys()
        
    def is_relevant_strategy(self,filename):
        whitelist = ['protokoll_G','protokoll_H','protokoll_U']
        return any(map(filename.startswith,whitelist))

    def get_strategy_file_names(self,path='../data/TESTRUNS_PEGASUS/'):
        return [f for f in listdir(path) if isfile(join(path,f)) and self.is_relevant_strategy(f)]
    
    def initialize_dict_with_problems(self,f,path):
        sdict = {}
        with open(path+f,'r') as IS:
            firstline = True
            for line in IS:
                if firstline:
                    firstline = False
                else:
                    sdict[line.split()[0]] = [[],[]]
        return sdict

    def load_strategies(self,path='../data/TESTRUNS_PEGASUS/'):
        fs = self.get_strategy_file_names()
        sdict = self.initialize_dict_with_problems(fs[0],path)
        for f in fs:
            firstline = True
            with open(path+f,'r') as IS:
                for line in IS:
                    if firstline:
                        firstline = False
                    else:
                        sline = line.split()
                        if(sline[1] != 'T'):
                            sdict[sline[0]][0].append(-1)
                        else:
                            sdict[sline[0]][0].append(float(sline[2]))
        return sdict
                    
    def load_features(self,fdict,path='../data/'):
        f = 'pegasusFeatures'
        with open(path+f,'r') as IS:
            firstline = True
            for line in IS:
                if firstline:
                    firstline = False
                else:
                    tmp = (line.strip()).split('#')
                    fdict[tmp[0].split('/')[2]][1] = [float(x) for x in tmp[1].split(',')]
        return fdict
    
    def generate_feature_matrix(self,fdict):
        total_features = []
        for key in fdict.keys():
            total_features.append(fdict[key][1])
        return np.array(total_features)
        
    def generate_strategy_matrix(self,fdict):
        total_strategies = []
        for key in fdict.keys():
            total_strategies.append(fdict[key][0])
        return np.array(total_strategies)