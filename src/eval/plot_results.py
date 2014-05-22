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


def plot_theory():
    axis_vals = [0.1, 300, 0, 11000]
    results = {}
    path = os.path.join(PATH, 'runs', 'theory')
    best_times = (os.path.join(path, 'bestTimes'), 'Best')
    best_times_wo_x = (os.path.join(path,
                       'bestTimesWithoutX'), 'Best without X')
    nn10 = (os.path.join(path, 'NN10'), 'NN10')
    nn_10_local = (os.path.join(path, 'NN10Local'), 'NN10Local')
    nn_20_local = (os.path.join(path, 'NN20Local'), 'NN20Local')
    nn_5_local_dyn = (os.path.join(path, 'NN5LocalDyn'), 'NN5LocalDyn')
    nn_10_local_dyn = (os.path.join(path, 'NN10LocalDyn'), 'NN10LocalDyn')
    e18 = (os.path.join(path, 'EAuto'), 'E 1.8')
    result_tuples = []
    result_tuples.append(e18)
    # result_tuples.append(best_times)
    result_tuples.append(best_times_wo_x)
    result_tuples.append(nn_10_local)
    result_tuples.append(nn_5_local_dyn)
    return result_tuples, axis_vals


def plot_real_training():
    axis_vals = [1, 300, 0, 1121]
    path = os.path.join(PATH, 'runs', 'real')
    e18 = (os.path.join(path, 'atp_eval_CASC_Train_E1.8'), 'E 1.8')
    e17 = (os.path.join(path, 'atp_eval_CASC_Train_E1.7'), 'E 1.7')
    emales = (os.path.join(path, 'atp_eval_CASC_Train_emales1.2'), 'E-MaLeS 1.2')
    helsing_nn = (os.path.join(path, 'atp_eval_CASC_Train_helsing_NN_with_basic_time_scaling'), 'Hesling NN')
    result_tuples = []
    result_tuples.append(e18)
    result_tuples.append(e17)
    result_tuples.append(emales)
    result_tuples.append(helsing_nn)
    return result_tuples, axis_vals


def plot_real_test():
    axis_vals = [1, 300, 0, 700]
    path = os.path.join(PATH, 'runs', 'real')
    e18 = (os.path.join(path, 'atp_eval_CASC_Test_E1.8'), 'E 1.8')
    e17 = (os.path.join(path, 'atp_eval_CASC_Test_E1.7'), 'E 1.7')
    emales = (os.path.join(path, 'atp_eval_CASC_Test_emales1.2'), 'E-MaLeS 1.2')
    result_tuples = []
    result_tuples.append(e18)
    result_tuples.append(e17)
    result_tuples.append(emales)
    return result_tuples, axis_vals


if __name__ == '__main__':
    #result_tuples, axis_vals = plot_theory()
    result_tuples, axis_vals = plot_real_training()
    #result_tuples, axis_vals = plot_real_test()
    plot_results(result_tuples, axis_vals)
