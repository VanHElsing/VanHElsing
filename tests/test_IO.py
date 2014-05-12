import unittest
import os
from src import IO
from src import globalVars

class IOTestCase(unittest.TestCase):
    def setUp(self):
        self.problemFile = 'PUZ001+1.p'
        self.pFileExtended = os.path.join(globalVars.PATH,'data',self.problemFile)
        
    def test_file_does_not_exist(self):
        with self.assertRaises(IOError) as context:
            IO.expand_filename('xx')
        self.assertTrue(context.exception.errno == 11 or context.exception.errno == 12)        

    def test_file_does_exist(self):        
        pFileExpanded = IO.expand_filename(self.pFileExtended)
        self.assertEqual(self.pFileExtended,pFileExpanded)        

    def test_run_e_works(self):
        eproverPath = os.path.join(globalVars.EPATH,'eprover') 
        command = ' '.join([eproverPath,'--cpu-limit=10 --tstp-format -s --proof-object',\
                           ' --memory-limit=2048--auto-schedule',self.pFileExtended])
        resultcode, _stdout, _stderr = IO.run_command(command, 10)
        self.assertTrue(resultcode)

        

