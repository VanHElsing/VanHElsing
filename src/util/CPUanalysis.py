import numpy as np
import os
import sys
import matplotlib.pylab as pl
import multiprocessing as mp

try:
    import cPickle as pickle
except ImportError:
    import pickle


def benchmark_task(args):
    """
    Wrapper for cpu_measurements.
    """
    cpu, strategy, p_path, p_name, strategy, pred_time = args
    real_time = cpu.measure(strategy, p_path)
    LOGGER.info('Finished %s in %f', p_path, real_time)
    return (p_name, strategy, pred_time, real_time)


def compute_benchmark(cpu, dataset):
    """
    Measures the CPU times for each problem in dataset.
    """
    TPTPPath = os.getenv('TPTP')

    result = []
    for p_name, strategy, pred_time in dataset:
        p_path = os.path.join(TPTPPath, 'Problems', p_name[:3], p_name)
        result.append(benchmark_task((cpu, strategy, p_path, p_name, strategy, pred_time)))
        
    return result


def compute_benchmark_concurrent(cpu, dataset, cores=None):
    """
    Measures the CPU times for each problem in dataset concurrently.
    """
    TPTPPath = os.getenv('TPTP')
    
    if cores is None:
        cores = mp.cpu_count()
    
    pool = mp.Pool(processes=cores)
    args = [(cpu, strategy, os.path.join(TPTPPath, 'Problems', p_name[:3], p_name), p_name, strategy, pred_time, scaled_time) for p_name, strategy, pred_time, scaled_time in dataset]
    results = pool.map_async(benchmark_task, args)
    pool.close()
    pool.join()
    results.wait()
    
    return results.get()


def show_dataset(dataset, name, color):
    X = []
    y = []
    for row in dataset:
        p_name, strategy, pred_time, real_time = row

        # """ Debug
        print "----"
        print p_name
        print strategy
        print pred_time
        print real_time
        # """

        X.append(pred_time)
        # y.append(scaled_time / real_time)
    
    X = np.array(X)
    y = np.array(y)
    
    return pl.scatter(X, y, c=color)


def execute_benchmark(cpu):
    path = os.path.join(PATH, 'tuning_benchmark')
    
    if os.path.isfile(path):
        with open(path, 'rb') as in_s:
            dataset = pickle.load(in_s)
    else:
        strategies = ['protokoll_G-E--_107_C45_F1_PI_AE_Q7_CS_SP_PS_S0Y',
                      'protokoll_H----_102_C18_F1_PI_AE_Q4_CS_SP_S1S',
                      'protokoll_H----_047_C18_F1_AE_R8_CS_SP_S2S',
                      'protokoll_G-E--_042_C45_F1_PI_AE_Q4_CS_SP_PS_S4S']
        
        ds = DataSet()
        ds.load('E')
        ds = remove_unsolveable_problems(ds)
        
        tasks = []
        for strategy in strategies:
            tasks.extend(gen_tasks(ds, 3, strategy))
        
        series_args = [1, 1, 2, 4, 8]
        dataset = []
        for dataset_arg in series_args:
            LOGGER.info("Executing series %i" % dataset_arg)
            dataset_run = compute_benchmark(cpu, tasks)
            dataset.append((dataset_arg, dataset_run))

        with open(path, 'wb') as out_s:
            pickle.dump(dataset, out_s)
    
    pl.figure("Composed")
    
    dataset_figures = []
    dataset_names = []
    colors = ['r', 'g', 'b', 'y', 'p']
    for dataset_i in range(len(dataset)):
        dataset_arg, dataset_run = dataset[dataset_i]
        dataset_name = "Series n=%i" % dataset_arg
        dataset_names.append(dataset_name)
        dataset_figures.append(show_dataset(dataset_run, dataset_name, colors[dataset_i]))
    
    pl.legend(dataset_figures, dataset_names)


def show_ratios(cpu):
    cpu.ratios.sort(key=lambda x: x[0])
    pl.figure("Tuning")
    pl.plot([x[0] for x in cpu.ratios], [x[2] for x in cpu.ratios])
    
    pl.figure("Tuning samples")
    pl.scatter([x[0] for x in cpu.ratios], [x[2] * x[0] for x in cpu.ratios])


def main():
    cpu = CPU()
    
    LOGGER.info("Tuning CPU on dataset... (or getting from cache)")
    cpu.load_or_gen_data()
    
    LOGGER.info("Tuning completed, executing benchmark")
    execute_benchmark(cpu)
    
    LOGGER.info("Showing ratios")
    show_ratios(cpu)
    
    pl.show()
    
    return 0

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    from src.CPU import CPU, gen_tasks
    from src.GlobalVars import PATH, LOGGER
    from src.DataSet import DataSet
    from src.data_util import remove_unsolveable_problems
    
    sys.exit(main())
