import unittest
import os
import IO
import globalVars


class IOTestCase(unittest.TestCase):
    def setUp(self):  # NOQA
        self.problemFile = 'PUZ001+1.p'
        self.pFileExtended = os.path.join(globalVars.PATH, 'data',
                                          self.problemFile)

    def test_file_does_not_exist(self):
        with self.assertRaises(IOError) as context:
            IO.expand_filename('xx')
        self.assertTrue(context.exception.errno == 11 or
                        context.exception.errno == 12)

    def test_file_does_exist(self):
        p_file_expanded = IO.expand_filename(self.pFileExtended)
        self.assertEqual(self.pFileExtended, p_file_expanded)

    def test_run_e_works(self):
        eprover_path = os.path.join(globalVars.EPATH, 'eprover')
        command = ' '.join([eprover_path,
                            '--cpu-limit=10 --tstp-format -s --proof-object',
                            ' --memory-limit=2048--auto-schedule',
                            self.pFileExtended])
        resultcode, _stdout, _stderr = IO.run_command(command, 10)
        self.assertTrue(resultcode)
