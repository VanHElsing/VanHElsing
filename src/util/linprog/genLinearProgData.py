import sys
from src.DataSet import DataSet
from src.data_util import remove_unsolveable_problems


def main():
    dataset = DataSet()
    dataset.load('E')
    dataset = remove_unsolveable_problems(dataset)
    
    problem_count, strat_count = dataset.strategy_matrix.shape
    
    print "param I_count := %i;" % problem_count
    print "param J_count := %i;" % strat_count

    print "param T : ",
    for strategy_i in range(strat_count):
        print "%i " % (strategy_i + 1),
    print ":="
    
    for problem_i in range(problem_count):
        print "%i  " % (problem_i + 1),
        for strategy_i in range(strat_count):
            t = dataset.strategy_matrix[problem_i][strategy_i]
            if t == -1:
                t = 301
                
            print "%f " % t,
        
        print ""
    print ";"
    print "end;"

    return 0


if __name__ == '__main__':
    sys.exit(main())
