'''
Created on May 15, 2014

@author: Frank Dorssers
'''

from os import listdir
from os.path import isfile, join
import numpy as np
from src.GlobalVars import PATH
from scipy.sparse import coo_matrix as smat

class DataSet(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.feature_matrix = None
        self.strategy_matrix = None
        self.strategies = None
        self.problems = None

    def mask(self, mask):
        copy = DataSet()
        copy.feature_matrix = self.feature_matrix[mask]
        copy.strategy_matrix = self.strategy_matrix[mask]
        copy.strategies = self.strategies
        copy.problems = self.problems[mask]
        return copy

    def sparsify(self):
        self.strategy_matrix = (self.strategy_matrix > -1) * self.strategy_matrix
        self.strategy_matrix = smat(self.strategy_matrix)

    def load(self, data_type):
        if data_type == 'E':
            self.parse_E_data()
        elif data_type == 'Satallax':
            self.parse_Satallax_data()
        else:
            raise IOError('Cannot parse unknown data type %s.'
                          % data_type)

    def parse_Satallax_data(self):
        pass

    def parse_E_data(self):  # NOQA
        self.strategies = []
        sdict = self.load_strategies()
        fdict = self.load_features(sdict)
        self.feature_matrix = self.generate_feature_matrix(fdict)
        self.strategy_matrix = self.generate_strategy_matrix(fdict)
        self.problems = np.array(fdict.keys())
        self.strategies = np.array(self.strategies)

    def is_relevant_strategy(self, filename):
        whitelist = ['protokoll_G', 'protokoll_H', 'protokoll_U']
        return any(map(filename.startswith, whitelist))

    def get_strategy_file_names(self, path=join(PATH,
                                                'data/E/TESTRUNS_PEGASUS/')):
        return [f for f in listdir(path) if
                isfile(join(path, f)) and self.is_relevant_strategy(f)]

    def initialize_dict_with_problems(self, sfile, path):
        sdict = {}
        with open(path + sfile, 'r') as inputstream:
            firstline = True
            for line in inputstream:
                if firstline:
                    firstline = False
                else:
                    sdict[line.split()[0]] = [[], []]
        return sdict

    def load_strategies(self, path=join(PATH, 'data/E/TESTRUNS_PEGASUS/')):
        sfiles = self.get_strategy_file_names()
        sdict = self.initialize_dict_with_problems(sfiles[0], path)
        for sfile in sfiles:
            firstline = True
            with open(path + sfile, 'r') as inputstream:
                for line in inputstream:
                    if firstline:
                        firstline = False
                        self.strategies.append(line[2:].strip())
                    else:
                        sline = line.split()
                        if sline[1] != 'T':
                            sdict[sline[0]][0].append(-1)
                        else:
                            sdict[sline[0]][0].append(float(sline[2]))
        return sdict

    def load_features(self, fdict, path=join(PATH, 'data/E/')):
        ffile = 'pegasusFeatures'
        with open(path + ffile, 'r') as inputstream:
            firstline = True
            for line in inputstream:
                if firstline:
                    firstline = False
                else:
                    tmp = (line.strip()).split('#')
                    key = tmp[0].split('/')[2]
                    fdict[key][1] = [float(x) for x in tmp[1].split(',')]
        return fdict

    def generate_feature_matrix(self, fdict):
        total_features = []
        for key in fdict.keys():
            total_features.append(fdict[key][1])
        return np.array(total_features)

    def generate_strategy_matrix(self, fdict):
        total_strategies = []
        for key in fdict.keys():
            total_strategies.append(fdict[key][0])
        return np.array(total_strategies)
