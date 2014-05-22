'''
Created on May 22, 2014

@author: Daniel Kuehlwein
'''

"""
1. Measure CPU times

2. Create Config (s)
Depending on the model(s) we chose, also set the model parameters
2.1 E config
2.2 Satallax config

3. Learn
3.1 learn E model
3.2 learn satallax model

4. Create executables

Example code:
config = ConfigParser.SafeConfigParser()
config.optionxform = str
config.add_section('Settings')
config.set('Settings','TPTP',TPTP)
config.set('Settings','TmpDir',os.path.join(path,'tmp')) 
config.set('Settings','Cores',str(cpu_count()-1)) 
"""
