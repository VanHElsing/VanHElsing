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


def make_data_distribution(cores, problems, filenames):
    distribution = [{'file': filenames[i], 'probs': []} for i in range(cores)]
    for i, p in enumerate(problems):
        distribution[i % cores]['probs'].append(p)
    return distribution


def get_prob_path(prob):
    return IO.expand_filename('Problems/{}/{}'.format(prob[:3], prob))


def run_distribution(dist):
    cmd = '../contrib/E/PROVER/classify_problem -caaaaaaaaaaaaa --tstp-in {}'
    with open(dist['file'], 'w') as f:
        for p in dist['probs']:
            curr_time = time.clock()
            IO.run_command(cmd.format(get_prob_path(p)), 300)
            f.write('{},{}\n'.format(p, (time.clock() - curr_time)))


if __name__ == '__main__':
    cores = 2
    m_problems = get_all_problems()
    m_filenames = get_all_filenames(cores)
    m_distributions = make_data_distribution(cores, m_problems, m_filenames)
#     distributions = [{'file':'results_p0.csv','probs':['AGT001+1.p','AGT001+2.p']},{'file':'results_p1.csv','probs':['AGT002+1.p','AGT002+2.p']}]

    print 'Starting pool'
    pool = Pool(processes=cores)
    pool.map(run_distribution, m_distributions)
    print 'Done'
