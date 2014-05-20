'''
Created on May 19, 2014

@author: Daniel Kuehlwein
'''

import os
import matplotlib.pyplot as pl
from src.GlobalVars import PATH


def plot_results(result_tuples, axis_vals=None):
    plot_styles = ['-', '--', '-.', ':', 'o--']
    plot_style_counter = 0
    pl.figure('Results')
    pl.ylabel('Problems solved')
    pl.xscale('log')
    pl.xlabel('Seconds')
    ax = pl.gca()
    ax.set_autoscale_on(False)
    if axis_vals is not None:
        pl.axis(axis_vals)
    for res_file, res_label in result_tuples:
        results = {}
        with open(res_file, 'r') as res_stream:
            for line in res_stream:
                if line.startswith('#'):
                    continue
                time = float(line.split(',')[1])
                if time not in results:
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
        pl.plot(times, solved_at_time, plot_styles[plot_style_counter],
                label=res_label)
    pl.legend(loc='lower right')
    pl.show()

if __name__ == '__main__':
    axisVals = [0.1, 300, 0, 11000]
    theory_path = os.path.join(PATH, 'runs', 'theory')
    best_times = (os.path.join(theory_path, 'bestTimes'), 'Best')
    best_times_wo_X = (os.path.join(theory_path,
                       'bestTimesWithoutX'), 'Best without X')
    NN10 = (os.path.join(theory_path, 'NN10'), 'NN10')
    NN10Local = (os.path.join(theory_path, 'NN10Local'), 'NN10Local')
    NN20Local = (os.path.join(theory_path, 'NN20Local'), 'NN20Local')
    NN5LocalDyn = (os.path.join(theory_path, 'NN5LocalDyn'), 'NN5LocalDyn')
    NN10LocalDyn = (os.path.join(theory_path, 'NN10LocalDyn'), 'NN10LocalDyn')
    E = (os.path.join(theory_path, 'EAuto'), 'E 1.8')
    result_tuples = []
    result_tuples.append(E)
    # result_tuples.append(best_times)
    result_tuples.append(best_times_wo_X)
    result_tuples.append(NN10Local)
    result_tuples.append(NN5LocalDyn)

    plot_results(result_tuples, axisVals)
