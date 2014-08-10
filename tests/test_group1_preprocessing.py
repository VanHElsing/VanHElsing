# pylint: disable=C0103
import unittest
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
        self.assertTrue(np.equal(B.round(), X1.round()).all())
        self.assertTrue(np.equal(X2.round(), X3.round()).all())
        self.assertTrue(np.equal(C[:, 3:6].round(), X1.round()).all())
