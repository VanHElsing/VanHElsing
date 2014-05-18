import unittest
import os

from src import DataSet
from src import GlobalVars
from src.schedulers.BasicSchedulers import SingleStrategyScheduler


class IOTestCase(unittest.TestCase):
    def setUp(self):  # NOQA, pylint: disable=C0103
        self.problem_file = 'PUZ001+1.p'
        self.p_file_extended = os.path.join(GlobalVars.PATH, 'data',
                                            self.problem_file)
        self.data_set = DataSet.DataSet()
        self.data_set.parse_E_data()

    def test_single_strategy_scheduler(self):  # NOQA, pylint: disable=C0103
        self.assertEqual(self.data_set.strategies[0],
                         "--definitional-cnf=24 --tstp-in --split-clauses=4 --split-reuse-defs --simul-paramod --forward-context-sr --destructive-er-aggressive --destructive-er --presat-simplify --prefer-initial-clauses -tLPO4 -Ginvarity -F1 -s --delete-bad-limit=1024000000 -WSelectMaxLComplexAvoidPosPred -H'(4*RelevanceLevelWeight2(SimulateSOS,0,2,1,2,100,100,100,400,1.5,1.5,1),3*ConjectureGeneralSymbolWeight(PreferNonGoals,200,100,200,50,50,1,100,1.5,1.5,1),1*Clauseweight(PreferProcessed,1,1,1),1*FIFOWeight(PreferProcessed))'")  # NOQA
        scheduler = SingleStrategyScheduler()
        scheduler.set_problem(self.p_file_extended)
        scheduler.fit(self.data_set, 300)
        strat, strat_time = scheduler.predict(10)
        self.assertEqual(strat,
                         "--definitional-cnf=24 --tstp-in --split-clauses=4 --split-reuse-defs --simul-paramod --forward-context-sr --destructive-er-aggressive --destructive-er --presat-simplify --prefer-initial-clauses -tLPO4 -Ginvarity -F1 -s --delete-bad-limit=1024000000 -WSelectMaxLComplexAvoidPosPred -H'(4*RelevanceLevelWeight2(SimulateSOS,0,2,1,2,100,100,100,400,1.5,1.5,1),3*ConjectureGeneralSymbolWeight(PreferNonGoals,200,100,200,50,50,1,100,1.5,1.5,1),1*Clauseweight(PreferProcessed,1,1,1),1*FIFOWeight(PreferProcessed))'")  # NOQA
        self.assertAlmostEqual(strat_time, 10.4048506749)
