import unittest
import os
import RunATP
import GlobalVars


class RunATPTestCase(unittest.TestCase):
    def test_wrong_binary_raises_error(self):
        atp = RunATP.ATP('foo', 'bar')
        with self.assertRaises(IOError) as context:
            atp.run('--auto-schedule', 10, 'p')
        self.assertEqual(context.exception.strerror,
                         'Cannot find ATP binary foo')

    def test_can_solve_problems(self):
        problem_file = 'PUZ001+1.p'
        p_file_extended = os.path.join(GlobalVars.PATH, 'data', problem_file)
        eprover_path = os.path.join(GlobalVars.EPATH, 'eprover')
        atp = RunATP.ATP(eprover_path, '--cpu-limit=',
                         '--tstp-format -s --proof-object --memory-limit=2048')
        proof_found, _cs, _stdout, used_time = atp.run('--auto-schedule',
                                                       10, p_file_extended)
        self.assertTrue(proof_found)
        self.assertLess(used_time, 0.5)