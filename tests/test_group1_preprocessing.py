import unittest
import os

import src.schedulers.group1.preprocessing as pp
import numpy as np

class Group1PreProcessingTestCase(unittest.TestCase):
    def setUp(self):  # NOQA, pylint: disable=C0103
        pass

    def test_preprocessing(self):  # NOQA, pylint: disable=C0103
        X1 = np.array([[1.0, 2, 3], [2, 3, 4], [3, 7, 5], [2, 9, 1]])
        V = pp.determine_pca(X1)
        B = pp.perform_pca(X1, V, 3)
        C = pp.add_pca_features(X1, V, [3, 2, 1])
        X2, MEANS, STDS = pp.standardize_features(X1)
        X3 = pp.standardize_features_means_stds(X1, MEANS, STDS)
        self.assertEqual(B.all(), X1.all())
        self.assertEqual(X2.all(), X3.all())
        self.assertEqual(C[:,3:6].all(), X1.all())        


if __name__ == '__main__':
    X1 = np.array([[1.0, 2, 3], [2, 3, 4], [3, 7, 5], [2, 9, 1]])
    V = pp.determine_pca(X1)
    B = pp.perform_pca(X1, V, 3)
    C = pp.add_pca_features(X1, V, [3, 2, 1])
    X2, MEANS, STDS = pp.standardize_features(X1)
    X3 = pp.standardize_features_means_stds(X1, MEANS, STDS)
    print 'X1', X1
    print '\nB', B
    print '\nC', C[:,3:6]
    print '\nX2', X2
    print '\nmeans', MEANS
    print '\nstds', STDS
    print '\nX3', X3
