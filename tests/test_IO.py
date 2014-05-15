import unittest
import os
from src import IO
from src import GlobalVars


class IOTestCase(unittest.TestCase):
    def setUp(self):  # NOQA, pylint: disable=C0103
        self.problem_file = 'PUZ001+1.p'
        self.p_file_extended = os.path.join(GlobalVars.PATH, 'data',
                                            self.problem_file)

    def test_file_does_not_exist(self):
        with self.assertRaises(IOError) as context:
            IO.expand_filename('xx')
        self.assertTrue(context.exception.errno == 11 or
                        context.exception.errno == 12)

    def test_file_does_exist(self):
        p_file_expanded = IO.expand_filename(self.p_file_extended)
        self.assertEqual(self.p_file_extended, p_file_expanded)

    def test_run_e_works(self):
        eprover_path = os.path.join(GlobalVars.EPATH, 'eprover')
        command = ' '.join([eprover_path,
                            '--cpu-limit=10 --tstp-format -s --proof-object',
                            ' --memory-limit=2048--auto-schedule',
                            self.p_file_extended])
        resultcode, dummy_stdout, dummy_stderr = IO.run_command(command, 10)
        self.assertTrue(resultcode)
