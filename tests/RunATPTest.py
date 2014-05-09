import unittest
from src import RunATP 
from src import globalVars
"""        
    problemFile = 'PUZ001+1.p'
    pFileExtended = os.path.join(globalVars.PATH,'data',problemFile)
    print pFileExtended
    
    #eprover --auto-schedule --tstp-format -s --proof-object --memory-limit=2048 --cpu-limit=%d %s  
    atp = RunATP(os.path.join(globalVars.EPATH,'eprover'),'--cpu-limit=','--tstp-format -s --proof-object --memory-limit=2048')
    print atp.run('--auto-schedule',10,pFileExtended)
    
"""
class RunATPTestCase(unittest.TestCase):
    def wrongBinaryRaisesError(self):
        atp = RunATP('foo','bar')
        self.assertRaises(IOError, atp.run(),'--auto-schedule',10,'p')
