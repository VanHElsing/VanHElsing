'''
Created on May 15, 2014

@author: Frank Dorssers
'''

from os import listdir
from os.path import isfile, join
import numpy as np
from src.GlobalVars import PATH


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

    def load(self, data_type):
        if data_type == 'E':
            self.parse_E_data()
        elif data_type == 'Satallax':
            self.parse_Satallax_data()
        else:
            raise IOError('Cannot parse unknown data type %s.'
                          % data_type)

    def parse_Satallax_data(self):
        self.problems, self.feature_matrix = self.sat_load_features()
        satallax_files = [f for f in self.sat_get_strat_file_names(join(PATH, 'data/Satallax/results')) if f.endswith('.results')]
        satallax_strats = [self.sat_load_strat(sat) for sat in satallax_files]
        self.strategies = map(lambda x: x.replace('.results',''), satallax_files)
        self.strategy_matrix = self.sat_generate_strat_matrix(self.problems,satallax_strats)
        print self.problems
        print self.feature_matrix[:6,:6]
        print satallax_strats[:1]
        print self.strategies
        print self.problems[:10]
        print self.strategy_matrix[:10,:2]
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

    def sat_load_strat(self,filename, path=join(PATH, 'data/Satallax/results')):
        new_strat = {}
        with open(join(path,filename), 'r') as inputstream:
            for line in inputstream:
                sline = line.split()
                new_strat[sline[0].split('/')[6]] = float(sline[1])
        return new_strat

    def sat_load_features(self):
        features_path = '../data/Satallax/Satallax_features'
        problems = []
        features = []
        with open(features_path,'r') as f:
            for line in f:
                hashtag_split = line.split('#')
                problems.append(hashtag_split[0].split('/')[7])
                features.append(map(float,hashtag_split[1].replace('\n','').split(',')))
        return problems, np.array(features)
    
    def sat_generate_strat_matrix(self,probs,strat_dicts):
        strategy_matrix = np.empty((len(probs),len(strat_dicts)))
        strategy_matrix[:] = -1
        index_dict = dict([index_item for index_item in zip(probs,range(len(probs)))])
        for col,strat in enumerate(strat_dicts):
            for prob in strat.keys():
                strategy_matrix[index_dict[prob],col] = strat[prob]
        return strategy_matrix
    
    def sat_get_strat_file_names(self,path=join(PATH, 'contrib/males/E/resultsTmp')):
        return [f for f in listdir(path) if isfile(join(path, f))]

ds = DataSet()
ds.load('Satallax')