import unittest
from src import DataSet


class RunDataSetTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):  # NOQA
        cls.ds = DataSet.DataSet()
        cls.ds.load('E')
        cls.amount_strategies = 187
        cls.amount_problems = 15560
        cls.amount_features = 22

    def test_strategy_array_shape(self):
        self.assertEqual(self.ds.strategies.shape, (self.amount_strategies,),
                         "Amount of strategies in the DataSet"
                         + "doesn't match the known amount of strategies")

    def test_problem_array_shape(self):
        self.assertEqual(self.ds.problems.shape, (self.amount_problems,),
                         "Amount of problems in the DataSet doesn't match"
                         + "the known amount of problems")

    def test_feature_matrix_shape(self):
        self.assertEqual(self.ds.feature_matrix.shape[0], self.amount_problems,
                         "Amount of rows in the feature matrix doesn't match"
                         + "the known amount of problems")
        self.assertEqual(self.ds.feature_matrix.shape[1], self.amount_features,
                         "Amount of columns in the feature matrix doesn't"
                         + " match the known amount of features")

    def test_strategy_matrix_shape(self):
        self.assertEqual(self.ds.strategy_matrix.shape[0],
                         self.amount_problems,
                         "Amount of rows in the feature matrix doesn't"
                         + "match the known amount of problems")
        self.assertEqual(self.ds.strategy_matrix.shape[1],
                         self.amount_strategies,
                         "Amount of columns in the feature matrix doesn't"
                         + " match the known amount of features")

    def test_is_relevant_strategy(self):
        valid_protocol = 'protokoll_G-E--_008_C18_F1_PI_AE_CS_SP_CO_S4S'
        non_valid_protocol = 'protokoll_X----_satauto_300_tff'
        self.assertTrue(self.ds.is_relevant_strategy(valid_protocol),
                        'Did not recognize a valid strategy')
        self.assertFalse(self.ds.is_relevant_strategy(non_valid_protocol),
                         'Recognized an non-valid strategy as valid')
        