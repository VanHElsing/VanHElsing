from multiprocessing import Pool
import DataSet
import time
import IO


def get_all_problems():
    ds = DataSet.DataSet()
    ds.load('E')
    return ds.problems


def get_all_filenames(cores):
    return ['results_p{}.csv'.format(i) for i in range(cores)]


def get_prob_path(prob):
    return IO.expand_filename('Problems/{}/{}'.format(prob[:3], prob))


def solve_problem(prob):
    cmd = '../contrib/E/PROVER/classify_problem -caaaaaaaaaaaaa --tstp-in {}'
    curr_time = time.clock()
    IO.run_command(cmd.format(get_prob_path(prob)), 300)
    return (prob, (time.clock() - curr_time))


if __name__ == '__main__':
    cores = 2
    m_problems = get_all_problems()

    pool = Pool(processes=cores)
    results = pool.map_async(solve_problem, m_problems)
    pool.close()
    pool.join()
    results.wait()
    results = results.get()
    with open('feature_times.csv', 'w') as f:
        for prob, tm in results:
            f.write('{},{}\n'.format(prob, tm))
