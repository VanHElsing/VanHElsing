'''
Created on May 15, 2014

@author: Frank Dorssers
'''

# pylint: disable=C0103, E0611, W0141
from os import listdir
from os.path import isfile, join
import numpy as np
from src.GlobalVars import PATH
from scipy.sparse import coo_matrix as smat


class DataSet(object):
    '''
    Class for loading, parsing and using Satallax and E data.

    This information contains problems (N), features (M) and
    strategy times (K).

    Variables
    ---------
    problems : 1 x N Numpy array
        Contains all problem names
    strategies : 1 x K Numpy array
        Contains all strategy names
    feature matrix :  N x M Numpy array
        Contains all features for each problem
    strategy matrix : N x K numpy array
        Contains all times for each strategy and problem
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.feature_matrix = None
        self.strategy_matrix = None
        self.strategy_files = None
        self.strategies = None
        self.problems = None

        self.whitelist = ['protokoll_G', 'protokoll_H', 'protokoll_U']

    def mask(self, mask):
        '''
        Creates a masked copy of the current data
        '''
        copy = DataSet()
        copy.feature_matrix = self.feature_matrix[mask]
        copy.strategy_matrix = self.strategy_matrix[mask]
        copy.strategies = self.strategies
        copy.strategy_files = self.strategy_files
        copy.problems = self.problems[mask]
        return copy

    def sparsify(self):
        '''
        Creates a sparse version of the current strategy matrix
        '''
        self.strategy_matrix = (self.strategy_matrix > -1) * self.strategy_matrix
        self.strategy_matrix = smat(self.strategy_matrix)

    def load(self, data_type):
        '''
        Loads a certain data type, 'E' or 'Satallax'

        Parameters
        ----------
        data_type : string
            The name of the data type
        '''
        if data_type == 'E':
            self.parse_E_data()
        elif data_type == 'Satallax':
            self.parse_Satallax_data()
        else:
            raise IOError('Cannot parse unknown data type %s.'
                          % data_type)

    def parse_Satallax_data(self):  # NOQA
        '''
        Loads and parses Satallax data, this includes strategy names,
        strategy times, problem names and problem features.
        These are stored in variables in the class
        '''
        self.problems, self.feature_matrix = self.sat_load_features()
        satallax_files = [f for f in self.sat_get_strat_file_names() if f.endswith('.results')]
        satallax_strats = [self.sat_load_strat(sat) for sat in satallax_files]
        tmp_strategies = ['-m ' + sfile.replace('.results', '') for sfile in satallax_files]
        self.strategies = np.array(tmp_strategies)
        self.strategy_matrix = self.sat_generate_strat_matrix(self.problems, satallax_strats)

    def parse_E_data(self):  # NOQA
        '''
        Loads and parses E data, this includes strategy names,
        strategy times, problem names and problem features.
        These are stored in variables in the class
        '''
        self.strategies = []
        self.strategy_files = []
        sdict = self.load_strategies()
        fdict = self.load_features(sdict)
        self.feature_matrix = self.generate_feature_matrix(fdict)
        self.strategy_matrix = self.generate_strategy_matrix(fdict)
        self.problems = np.array(fdict.keys())
        self.strategies = np.array(self.strategies)

    def is_relevant_strategy(self, strategy):
        '''
        Checks whether a certain strategy is a valid E strategy depending on the whitelist

        Parameters
        ----------
        strategy : string
            The name of the strategy that should be checked

        Returns
        -------
        result : boolean
            True if it is a relevant strategy
        '''
        return any(map(strategy.startswith, self.whitelist))

    def get_strategy_file_names(self, path=join(PATH, 'data/E/TESTRUNS_PEGASUS/')):
        '''
        Collects and returns all relevant filenames for 'E' strategies in a certain path

        Parameters
        ----------
        path : string
            Path to a folder which should be checked for strategy file names

        Returns
        -------
        result : list
            A list of strings containing all relevant strategy file names
        '''
        return [f for f in listdir(path) if
                isfile(join(path, f)) and self.is_relevant_strategy(f)]

    def load_strategies(self, path=join(PATH, 'data/E/TESTRUNS_PEGASUS/')):
        '''
        Loads all strategy file names, parses them and puts them in a list of
        dictionaries in the shape of {key : [[],[]]}, the initial list in the
        value will contain the strategy times

        Parameters
        ----------
        path : string
            Path to a folder which contains the strategy files

        Returns
        -------
        sdict : list
            List containing a dictionary for each strategy file in the shape
            of {key : [[],[]]}, the initial list containing the strategy times
        '''
        sfiles = self.get_strategy_file_names()
        sdict = dict()
        for sfile_i in range(len(sfiles)):
            sfile = sfiles[sfile_i]
            firstline = True
            with open(path + sfile, 'r') as inputstream:
                for line in inputstream:
                    if firstline:
                        firstline = False
                        self.strategies.append(line[2:].strip())
                        self.strategy_files.append(sfile)
                    else:
                        sline = line.split()
                        if not sline[0] in sdict:
                            sdict[sline[0]] = [-1 * np.ones(len(sfiles)), []]
                        if sline[1] == 'T':
                            sdict[sline[0]][0][sfile_i] = float(sline[2])
        return sdict

    def load_features(self, fdict, path=join(PATH, 'data/E/')):
        '''
        Loads the features file, parses it and adds them to the second
        list in the fdict

        Parameters
        ----------
        fdict : list
            List containing dictionaries in the shape of {key : [[],[]]}
            where the first list in the list contains strategy times and
            the second list will be filled with the features
        path : string
            Path to a folder which contains the features file

        returns
        -------
        fdict : list
            Same type and shape as the initial fdict parameter but with
            the second list in the value containing the parsed features
        '''
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
        '''
        Converts a list of dictionaries in the shape as the one generated by
        the 'load_features' and 'sat_load_features' functions and turns it
        into a N x M numpy array

        Parameters
        ----------
        fdict : list
            List of dictionaries containing all features for all problems as
            generated by the function 'load_features'

        Returns
        -------
        result : numpy array
            N x M array containing all features for all problems in the parameters
        '''
        total_features = []
        for key in fdict.keys():
            total_features.append(fdict[key][1])
        return np.array(total_features)

    def generate_strategy_matrix(self, sdict):
        '''
        Converts a list of dictionaries in the shape as the one generated by
        the 'load_strategies' function and turns it into a N x K numpy array

        Parameters
        ----------
        fdict : list
            List of dictionaries containing all strategy times for all problems as
            generated by the function 'load_strategies'

        Returns
        -------
        result : numpy array
            N x K array containing all strategy times for all problems in the parameters
        '''
        total_strategies = []
        for key in sdict.keys():
            total_strategies.append(sdict[key][0])
        return np.array(total_strategies)

    def sat_load_strat(self, filename, path=join(PATH, 'data/Satallax/results')):
        '''
        Loads a single Satallax strategy and puts it in a dictionary in the
        shape of {problem : time}

        Parameters
        ----------
        filename : string
            The name of the file containing the strategy data

        Returns
        -------
        new_strat : dictionary
            Contains all times for each solved problem, in the shape
            of {problem : time}
        '''
        new_strat = {}
        with open(join(path, filename), 'r') as inputstream:
            for line in inputstream:
                sline = line.split()
                new_strat[sline[0].split('/')[6]] = float(sline[1])
        return new_strat

    def sat_load_features(self):
        '''
        Loads and parses the feature names and actual features

        Returns
        -------
        Problems : 1 x N Numpy array
            Numpy array containing all problem names
        Features : N x M Numpy array
            Numpy array containing the actual features
        '''
        features_path = join(PATH, 'data', 'Satallax', 'Satallax_features')
        problems = []
        features = []
        with open(features_path, 'r') as f:
            for line in f:
                hashtag_split = line.split('#')
                problems.append(hashtag_split[0].split('/')[7])
                features.append(map(float, hashtag_split[1].replace('\n', '').split(',')))
        return np.array(problems), np.array(features)

    def sat_generate_strat_matrix(self, probs, strat_dicts):
        '''
        Converts a list of dictionaries in the shape as the one generated by
        the 'sat_load_strat' function and turns it into a numpy array

        Parameters
        ----------
        probs : list
            List of all problem names
        strat_dicts : list
            Contains dictionaries as generated by 'sat_load_strat'

        Returns
        -------
        result : numpy array
            N x K array containing all strategy times for all problems in the parameters
        '''
        strategy_matrix = np.empty((len(probs), len(strat_dicts)))
        strategy_matrix[:] = -1
        index_dict = dict([index_item for index_item in zip(probs, range(len(probs)))])
        for col, strat in enumerate(strat_dicts):
            for prob in strat.keys():
                strategy_matrix[index_dict[prob], col] = strat[prob]
        return strategy_matrix

    def sat_get_strat_file_names(self, path=join(PATH, 'data/Satallax/results')):
        '''
        Collects and returns all relevant filenames for Satallax strategies in a certain path

        Parameters
        ----------
        path : string
            Path to a folder which should be checked for strategy file names

        Returns
        -------
        result : list
            A list of strings containing all relevant strategy file names
        '''
        return [f for f in listdir(path) if isfile(join(path, f))]
