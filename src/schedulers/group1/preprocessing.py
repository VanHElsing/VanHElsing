'''
Module containing default preprocessing functions

Created on May 18, 2014

@author: R.J. Drenth, Sil van de Leemput
'''

import numpy as np
import scipy.linalg as linalg


def add_pca_features(X, V, pcas=None):
    '''
    Each integer i with value $pcas[i]$ within the pcas list determines
    a range (1 - pcas[i]) of principle components used for reconstructing X
    giving X'_i. The resulting matrices are concatenated vertically after
    the original matrix X and returned as a whole new matrix.

    Variables
    ---------
    X    : matrix                   (problems x strategies)
           original feature matrix
    V    : matrix                   (strategies x strategies)
           the unitary matrix from the determine_pca function
    pcas : list                     (Npcas)
           with integer values representing the pca numbers to use
           default = [] i.e. only X is returned. No X'_i is created

    Returns
    -------
    X2 : matrix             (problems x (strategies * (N_pcas + 1)))
        that is the concatenated matrix:
            X concat X'_1 concat ... concat X'_Npcas
    '''
    X2 = X
    if pcas is None:
        pcas = []
    for pca in pcas:
        pcan = perform_pca(X, V, pca)
        X2 = np.append(X2, pcan, axis=1)
    return X2


def determine_pca(X):
    '''
    Determines the unitary matrix V from data matrix X,
    which is required for performing PCA

    Variables
    ---------
    X : the data matrix             (problems x strategies)

    Returns
    -------
    V : the unitary matrix          (strategies x strategies)
    '''
    U, S, V = linalg.svd(np.mat(X), full_matrices=False)
    return np.array(V).T


def perform_pca(X, V, number_pcas=-1):
    '''
    Performs PCA on the given dataset X, utilising the unitary matrix V.

    Variables
    ---------
    X           : numpy array        (problems x strategies)
    V           : the unitary matrix (strategies x strategies)
    number_pcas : integer, the number of PCAs that are used to reconstruct
                the data. Default value is -1, which means all PCAs are used.

    Returns
    -------
    Z : the data matrix              (problems x strategies)
        expressed in its PCA's.
    '''
    X2 = X.dot(V)
    if number_pcas == -1:
        Z = X2.dot(V.T)
    else:
        Z = X2[:, range(number_pcas)].dot(V[:, range(number_pcas)].T)
    return Z


def standardize_features(X, cap=False, capval=2.5):
    '''
    Column-wise standardization of a data matrix

    Variables
    ---------
    X      : data matrix             (problems x strategies)
    cap    : boolean
    capval : double
            If cap=True (default = false), then it will also cap the Z scores
            at the given capval (default = 2.5). For negative scores, it will
            be capped at -capval.

    Returns
    -------
    X     : standardized data matrix (problems x strategies)
    means : respective means of X    (strategies)
    stds  : respective stds of X     (strategies)
    '''
    means = np.mean(X, axis=0)
    stds = np.std(X, axis=0)
    X = standardize_features_means_stds(X, means, stds, cap, capval)
    return X, means, stds


def standardize_features_means_stds(X, means, stds, cap=False, capval=2.5):
    '''
    Column-wise standardization of a data matrix using precalculated
    means and stds

    Variables
    ---------
    X      : numpy array             (problems x strategies)
    means  : respective means of X   (strategies)
    stds   : respective stds of X    (strategies)
    cap    : boolean
    capval : double
            If cap=True (default = false), then it will also cap the Z scores
            at the given capval (default = 2.5). For negative scores, it will
            be capped at -capval.

    Returns
    -------
    X     : standardized numpy array (problems x strategies)
    '''
    X = ((X - means) / stds)
    if cap:
        X[X > capval] = capval
        X[X < -capval] = -capval
    return X
