import unittest
import os
import RunATP 
import globalVars

class RunATPTestCase(unittest.TestCase):
    def test_wrong_binary_raises_error(self):
        atp = RunATP.ATP('foo','bar')
        with self.assertRaises(IOError) as context:
            atp.run('--auto-schedule',10,'p')
        self.assertEqual(context.exception.strerror, 'Cannot find ATP binary foo')        

    def test_can_solve_problems(self):
        problemFile = 'PUZ001+1.p'
        pFileExtended = os.path.join(globalVars.PATH,'data',problemFile)
        eproverPath = os.path.join(globalVars.EPATH,'eprover') 
        atp = RunATP.ATP(eproverPath,'--cpu-limit=','--tstp-format -s --proof-object --memory-limit=2048')
        proofFound,_countersat,_stdout,usedTime = atp.run('--auto-schedule',10,pFileExtended)
        self.assertTrue(proofFound)
        self.assertLess(usedTime, 0.5)
        

