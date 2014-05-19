'''
Created on May 19, 2014

@author: Daniel Kuehlwein
'''

import os
import matplotlib.pyplot as pl
from src.GlobalVars import PATH

def plot_results(result_tuples, axisVals = None):
    plotStyles = ['-','--','-.',':','o--']
    plotStyleCounter = 0
    pl.figure('Results')
    pl.ylabel('Problems solved')
    pl.xscale('log')
    pl.xlabel('Seconds')
    ax = pl.gca()
    ax.set_autoscale_on(False)
    if not axisVals is None:
        pl.axis(axisVals)
    for res_file, res_label in result_tuples:
        results = {}
        IS = open(res_file,'r')
        for line in IS:
            if line.startswith('#'):
                continue
            time = float(line.split(',')[1])
            if not results.has_key(time):
                results[time] = 1
            else:
                results[time] += 1 
        total_solved = 0
        solved_at_time = []
        times = sorted(results.keys())
        for key in times:        
            total_solved += results[key]        
            solved_at_time.append(total_solved)
        times.append(300)
        solved_at_time.append(solved_at_time[-1])
        pl.plot(times,solved_at_time,plotStyles[plotStyleCounter],label=res_label)
    pl.legend(loc='lower right')
    pl.show()

if __name__ == '__main__':
    axisVals = [0.1,300,0,11000]
    NN10 = (os.path.join(PATH,'runs','NN10'),'NN10')
    NN10Local = (os.path.join(PATH,'runs','NN10Local'),'NN10Local')
    NN20Local = (os.path.join(PATH,'runs','NN20Local'),'NN20Local')
    E =  (os.path.join(PATH,'runs','EAuto'),'E 1.8')    
    result_tuples = []
    result_tuples.append(E)
    result_tuples.append(NN10)
    result_tuples.append(NN10Local)
    result_tuples.append(NN20Local)
    plot_results(result_tuples,axisVals)