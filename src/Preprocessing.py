'''
Created on May 18, 2014

@author: R.J. Drenth
modified by: Sil van de Leemput
'''

import numpy as np
import scipy.linalg as linalg

def addPCAFeatures(X, V, pcas = []):
    X2 = X
    for pca in pcas:
        pcan = performPCA(X, V, pca)
        X2 = np.append(X2, pcan, axis=1)      
    return X2 

def determinePCA(X):
    '''    
    Determines the principal components from data matrix X
    
    Returns V, the unitary matrices, which are required for performing PCA
    '''
    U, S, V = linalg.svd(np.mat(X), full_matrices=False)
    return np.array(V).T
    
def performPCA(X, V, numberPCAsToUse=-1):
    ''' 
    Performs PCA on the given dataset X, utilising the unitary matrices V.
    numberPCAsToUse is the number of PCAs that are used to reconstruct the data.
    Default value is -1, which means all PCAs are used.    
    
    Returns Z, the data expressed in its PCA's.
    '''
    Xpca = X.dot(V)
    if numberPCAsToUse == -1:
        Z = Xpca.dot(V.T)
    else:
        Z = Xpca[:,range(numberPCAsToUse)].dot(V[:, range(numberPCAsToUse)].T)
    return Z
    
def standardizeFeatures(X, cap=False, capValue=2.5):
    '''
    Returns X, means, stds.
    X is the standardized multidimensional array with means and stds 
    holding the respective means and standard deviations of each column.
    
    If cap=True (default = false), then it will also cap the Z scores at the 
    given capValue (default = 2.5). For negative scores, it will be capped at
    -capValue.    
    ''' 
    means = np.mean(X, axis=0)
    stds = np.std(X, axis=0)
    X = standardizeFeaturesWithMeansStds(X, means, stds, cap, capValue)
    return X, means, stds
    
def standardizeFeaturesWithMeansStds(X, means, stds, cap=False, capValue=2.5):
    '''
    Returns X
    X is a normalised multidimensional array, with means and stds
    as the normalisation parameters.
    
    If cap=True (default = false), then it will also cap the Z scores at the 
    given capValue (default = 2.5). For negative scores, it will be capped at
    -capValue.    
    '''     
    X = ((X - means) / stds)
    if cap:
        X[X > capValue] = capValue
        X[X < -capValue] = -capValue
    return X
    
if __name__ == '__main__':
    # Tests...
    X1 = np.array([[1.0, 2, 3], [2, 3, 4], [3, 7, 5], [2, 9, 1]])
    V = determinePCA(X1)
    B = performPCA(X1, V, 3)
    C = addPCAFeatures(X1, V, [3, 2, 1])
    X2, means, stds = standardizeFeatures(X1)
    X3 = standardizeFeaturesWithMeansStds(X1, means, stds)

    print 'X1', X1
    print '\nB', B
    print '\nC', C
    print '\nX2', X2
    print '\nmeans', means
    print '\nstds', stds    
    print '\nX3', X3