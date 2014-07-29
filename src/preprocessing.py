'''
Created on May 18, 2014

@author: R.J. Drenth, Sil van de Leemput
'''

import numpy as np
import scipy.linalg as linalg


def add_pca_features(X, V, pcas=None):
    '''
    Apply n pca values on X resulting in X'_n then append the matrices to X
    X is the original feature matrix 
    V is the pca matrix (from determine_pca)
    pcas is a list with integer values representing the pca number to used

    Returns X2, that is X app X'_0 app ... app X'_n.    
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
    Determines the principal components from data matrix X

    Returns V, the unitary matrices, which are required for performing PCA
    '''
    U, S, V = linalg.svd(np.mat(X), full_matrices=False)
    return np.array(V).T


def perform_pca(X, V, number_pcas=-1):
    '''
    Performs PCA on the given dataset X, utilising the unitary matrices V.
    number_pcas is the number of PCAs that are used to reconstruct the data.
    Default value is -1, which means all PCAs are used.

    Returns Z, the data expressed in its PCA's.
    '''
    X2 = X.dot(V)
    if number_pcas == -1:
        Z = X2.dot(V.T)
    else:
        Z = X2[:, range(number_pcas)].dot(V[:, range(number_pcas)].T)
    return Z


def standardize_features(X, cap=False, capval=2.5):
    '''
    Returns X, means, stds.
    X is the standardized multidimensional array with means and stds
    holding the respective means and standard deviations of each column.

    If cap=True (default = false), then it will also cap the Z scores at the
    given capval (default = 2.5). For negative scores, it will be capped at
    -capval.
    '''
    means = np.mean(X, axis=0)
    stds = np.std(X, axis=0)
    X = standardize_features_means_stds(X, means, stds, cap, capval)
    return X, means, stds


def standardize_features_means_stds(X, means, stds, cap=False, capval=2.5):
    '''
    Returns X
    X is a normalised multidimensional array, with means and stds
    as the normalisation parameters.

    If cap=True (default = false), then it will also cap the Z scores at the
    given capval (default = 2.5). For negative scores, it will be capped at
    -capval.
    '''
    X = ((X - means) / stds)
    if cap:
        X[X > capval] = capval
        X[X < -capval] = -capval
    return X


if __name__ == '__main__':
    # Tests...
    X1 = np.array([[1.0, 2, 3], [2, 3, 4], [3, 7, 5], [2, 9, 1]])
    V = determine_pca(X1)
    B = perform_pca(X1, V, 3)
    C = add_pca_features(X1, V, [3, 2, 1])
    X2, MEANS, STDS = standardize_features(X1)
    X3 = standardize_features_means_stds(X1, MEANS, STDS)

    print 'X1', X1
    print '\nB', B
    print '\nC', C
    print '\nX2', X2
    print '\nmeans', MEANS
    print '\nstds', STDS
    print '\nX3', X3
