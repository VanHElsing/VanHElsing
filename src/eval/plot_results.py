'''
Created on May 19, 2014

@author: Daniel Kuehlwein
'''
# flake8: disable=F841, E265
# pylint: disable=W0621, W0612, C0103
import sys
import os
import operator
import matplotlib.pyplot as pl
from src.GlobalVars import PATH


def plot_results(result_tuples, axis_vals=None):
    plot_styles = ['-', '--', '-.', ':', 'o--']
    plot_style_counter = 0
    pl.figure('Results')
    pl.ylabel('Problems solved')
    # pl.xscale('log')
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
        print len(solved_at_time)
        solved_at_time.append(solved_at_time[-1])
        pl.plot(times, solved_at_time, plot_styles[plot_style_counter],
                label=res_label)
    if axis_vals is not None:
        pl.axis(axis_vals)
    pl.legend(loc='lower right')
    pl.show()
    

def dump_results(result_tuples):
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
        with open("output/real-training-%s.csv" % res_label.replace(' ', '-'), 'w') as s_out:
            s_out.write("Time   Solved\n")
            for x, y in zip(times, solved_at_time):
                s_out.write("%f   %i\n" % (x, y))
    return

def dump_min_result(result_tuples, name):
    timeline_elements = []
    timeline = dict()
    
    for i in range(len(result_tuples)):
        res_file, res_label = result_tuples[i]
        results = {}
        with open(res_file, 'r') as res_stream:
            for line in res_stream:
                if line.startswith('#'):
                    continue
                time = round(float(line.split(',')[1]), 1)
                if time not in results:
                    results[time] = 1
                else:
                    results[time] += 1
        total_solved = 0
        times = sorted(results.keys())
        for key in times:
            total_solved += results[key]
            
            timeline_elements.append(key)
            if key not in timeline:
                timeline[key] = []
            timeline[key].append((i, total_solved))

    timeline_elements = list(set(timeline_elements))
    timeline_elements.sort()
    
    results = []
    for i in range(len(result_tuples)):
        results.append([])
    
    state = len(result_tuples)*[sys.maxint]
    for key in timeline_elements:
        print key
        for i, total_solved in timeline[key]:
            state[i] = total_solved
            
        min_value = min(state)
        for i in range(len(result_tuples)):
            if state[i] != sys.maxint:
                results[i].append((key, state[i] - min_value))
    
    for i in range(len(result_tuples)):
        res_file, res_label = result_tuples[i]
        with open("output/%s-%s.csv" % (name, res_label.replace(' ', '-')), 'w') as s_out:
            s_out.write("Time   Solved\n")
            for x, y in results[i]:
                s_out.write("%f   %i\n" % (x, y))


def plot_theory_satallax():
    axis_vals = [0.1, 350, 0, 573]
    path = os.path.join(PATH, 'runs', 'theory', 'Satallax')
    best_times = (os.path.join(path, 'bestTimes'), 'Best')
    nn_5_local_dyn = (os.path.join(path, 'NN5LocalDyn_1.1'), 'NN5LocalDyn1.1')
    nn_2_local_dyn = (os.path.join(path, 'NN2LocalDyn_1.1'), 'NN2LocalDyn1.1')
    ml_eval = (os.path.join(PATH, 'src', 'ml_eval'), 'ML Eval')
    result_tuples = []
    result_tuples.append(best_times)
    result_tuples.append(ml_eval)
    result_tuples.append(nn_5_local_dyn)
    result_tuples.append(nn_2_local_dyn)
    return result_tuples, axis_vals


def plot_theory_e():
    axis_vals = [1, 350, 0, 11000]
    path = os.path.join(PATH, 'runs', 'theory', 'E')
    best_times = (os.path.join(path, 'bestTimes'), 'Best')
    best_times_wo_x = (os.path.join(path, 'bestTimesWithoutX'), 'Best without X')
    # nn10 = (os.path.join(path, 'NN10'), 'NN10')
    # nn_10_local = (os.path.join(path, 'NN10Local'), 'NN10Local')
    # nn_20_local = (os.path.join(path, 'NN20Local'), 'NN20Local')
    nn_5_local_dyn = (os.path.join(path, 'NN5LocalDyn'), 'NN5LocalDyn')
    nn_2_local_dyn = (os.path.join(path, 'NN2LocalDyn'), 'NN2LocalDyn')
    # nn_10_local_dyn = (os.path.join(path, 'NN10LocalDyn'), 'NN10LocalDyn')
    # greedy_plus_nn_5_local_dyn = (os.path.join(path, 'GreedyPlusNN5LocalDyn'), 'GreedyPlusNN5LocalDyn')
    # ml_eval = (os.path.join(PATH, 'src', 'ml_eval'), 'ML Eval')
    e18 = (os.path.join(path, 'EAuto'), 'E 1.8')
    knn_t200 = (os.path.join(path, 'NN5_t200test'), 'NN5_t200')
    knn_t300 = (os.path.join(path, 'NN5_t300test'), 'NN5_t300')

    result_tuples = []
    result_tuples.append(e18)
    result_tuples.append(best_times)
    result_tuples.append(best_times_wo_x)
    # result_tuples.append(nn_10_local)
    result_tuples.append(nn_5_local_dyn)
    result_tuples.append(nn_2_local_dyn)
    # result_tuples.append(greedy_plus_nn_5_local_dyn)
    # result_tuples.append(ml_eval)
    result_tuples.append(knn_t200)
    result_tuples.append(knn_t300)
    return result_tuples, axis_vals


def plot_real_training_satallax():
    axis_vals = [0.1, 350, 0, 573]
    path = os.path.join(PATH, 'runs', 'real', 'Satallax')
    s27 = (os.path.join(path, 'atp_eval_CASC_Training_Satallax2.7'), 'Satallax 2.7')
    helsing_nn_wots = (os.path.join(path, 'atp_eval_CASC_Training_Satallax-MaLeS1.3'), 'Satallax-MaLeS 1.3')
    s27gp = (os.path.join(path, 'atp_eval_CASC_Training_Satallax2.7_GreedyPlus'), 'Satallax 2.7 GP')
    helsing_nn_wotsgp = (os.path.join(path, 'atp_eval_CASC_Training_Satallax-MaLeS1.3_GreedyPlus'), 'Satallax-MaLeS 1.3 GreedyPlus')
    result_tuples = []
    result_tuples.append(s27gp)
    result_tuples.append(helsing_nn_wotsgp)
    result_tuples.append(s27)
    result_tuples.append(helsing_nn_wots)
    return result_tuples, axis_vals


def plot_real_test_satallax():
    axis_vals = [0.1, 350, 0, 600]
    path = os.path.join(PATH, 'runs', 'real', 'Satallax')
    s27 = (os.path.join(path, 'atp_eval_CASC_Test_Satallax2.7'), 'Satallax 2.7')
    helsing_nn_wots = (os.path.join(path, 'atp_eval_CASC_Test_Satallax-MaLeS1.3'), 'Satallax-MaLeS 1.3')
    s27gp = (os.path.join(path, 'atp_eval_CASC_Test_Satallax2.7_GreedyPlus'), 'Satallax 2.7 GP')
    helsing_nn_wotsgp = (os.path.join(path, 'atp_eval_CASC_Test_Satallax-MaLeS1.3_GreedyPlus'), 'Satallax-MaLeS 1.3 GreedyPlus')
    result_tuples = []
    result_tuples.append(s27)
    result_tuples.append(helsing_nn_wots)
    result_tuples.append(s27gp)
    result_tuples.append(helsing_nn_wotsgp)

    return result_tuples, axis_vals


def plot_real_training():
    axis_vals = [1, 300, 0, 1121]
    path = os.path.join(PATH, 'runs', 'real')
    e18 = (os.path.join(path, 'E', 'atp_eval_CASC_Train_E1.8'), 'E 1.8')
    e17 = (os.path.join(path, 'E', 'atp_eval_CASC_Train_E1.7'), 'E 1.7')
    emales = (os.path.join(path, 'E', 'atp_eval_CASC_Train_emales1.2'), 'E-MaLeS 1.2')
    # helsing_nn_wts = (os.path.join(path, 'E', 'atp_eval_CASC_Train_helsing_NN_with_basic_time_scaling'), 'Helsing NN wts')
    helsing_nn_wots = (os.path.join(path, 'E', 'atp_eval_CASC_Train_helsing_NN_without_time_scaling'), 'Helsing NN wots')
    helsing_nnmax2 = (os.path.join(path, 'E', 'atp_eval_CASC_Training_helsing_NNmax2'), 'Helsing NNmax2')
    
    # helsing_group1 = (os.path.join(path, 'E', 'atp_eval_CASC_Training_helsing_group1'), 'Helsing Group1')
    # helsing_group1rf = (os.path.join(path, 'E', 'atp_eval_CASC_Training_helsing_group1_RF'), 'Helsing Group1 RF')
    # helsing_group1rf2 = (os.path.join(path, 'E', 'atp_eval_CASC_Training_Group1RF_002'), 'Helsing Group1 RF2')
    # helsing_group1dt = (os.path.join(path, 'E', 'atp_eval_CASC_Training_helsing_group1_DT'), 'Helsing Group1 DT')
    # helsing_group1knn = (os.path.join(path, 'E', 'atp_eval_CASC_Training_helsing_group1_KNN'), 'Helsing Group1 KNN')
    greedyplus = (os.path.join(path, 'E', 'atp_eval_CASC_Training_GreedyPlus_002'), 'GreedyPlus')

    result_tuples = []
    result_tuples.append(e18)
    result_tuples.append(e17)
    result_tuples.append(emales)
    # result_tuples.append(helsing_nn_wts)
    result_tuples.append(helsing_nn_wots)
    result_tuples.append(helsing_nnmax2)
    # result_tuples.append(helsing_group1rf)
    # result_tuples.append(helsing_group1rf2)
    # result_tuples.append(helsing_group1dt)
    # result_tuples.append(helsing_group1knn)
    result_tuples.append(greedyplus)

    return result_tuples, axis_vals


def plot_real_test():
    axis_vals = [1, 350, 0, 700]
    path = os.path.join(PATH, 'runs', 'real')
    e18 = (os.path.join(path, 'atp_eval_CASC_Test_E1.8'), 'E 1.8')
    e17 = (os.path.join(path, 'atp_eval_CASC_Test_E1.7'), 'E 1.7')
    emales = (os.path.join(path, 'atp_eval_CASC_Test_emales1.2'), 'E-MaLeS 1.2')
    helsing_nn_wots = (os.path.join(path, 'atp_eval_CASC_Test_helsing_NN_without_time_scaling'), 'Helsing NN wots')
    helsing_group1 = (os.path.join(path, 'atp_eval_CASC_Test_helsing_group1'), 'Helsing Group1')
    result_tuples = []
    result_tuples.append(e18)
    result_tuples.append(e17)
    result_tuples.append(emales)
    result_tuples.append(helsing_nn_wots)
    result_tuples.append(helsing_group1)
    return result_tuples, axis_vals


def plot_theory_cv_nn():
    axis_vals = [1, 300, 0, 10100]
    path = os.path.join(PATH, 'runs', 'theory', 'E')
    sets = [
        (4, 1, 300, 'max'), (4, 2, 300, 'max'), (4, 5, 300, 'max'),
        (4, 1, 300, 'median'), (4, 2, 300, 'median'), (4, 5, 300, 'median'),
        (4, 1, 300, 'mean'), (4, 2, 300, 'mean'), (4, 5, 300, 'mean'),
        (4, 1, 300, 'meanmedian'), (4, 2, 300, 'meanmedian'), (4, 5, 300, 'meanmedian')
    ]
    
    # files = map(lambda (folds, neighbors, max_time, f): ("CV%i_NN%s%i_%i" % (folds, f, neighbors, max_time)), sets)
    files = [("CV%i_NN%s%i_%i" % (folds, f, neighbors, max_time)) for (folds, neighbors, max_time, f) in sets]
    # result_tuples = map(lambda f : (os.path.join(path, f), f), files)
    result_tuples = [(os.path.join(path, f), f) for f in files]
    return result_tuples, axis_vals


if __name__ == '__main__':
    # result_tuples, axis_vals = plot_theory_e()
    # result_tuples, axis_vals = plot_theory_satallax()
    result_tuples, axis_vals = plot_real_training()
    # result_tuples, axis_vals = plot_real_test()
    # result_tuples, axis_vals = plot_theory_cv_nn()
    # plot_results(result_tuples, axis_vals)
    # dump_results(result_tuples)
    # dump_min_result(result_tuples, 'real-training')
    dump_min_result(result_tuples, 'real-training')
