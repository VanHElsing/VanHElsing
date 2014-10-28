import sys
import os
from tempfile import NamedTemporaryFile

def gen_prog(dataset, number_solved):
    problem_count, strat_count = dataset.strategy_matrix.shape

    result = ""

    result += "(define Runtime::(-> real real))\n"
    result += "(define Solved::real)\n"
    
    # All runtimes >= 0
    result += "(assert (and "
    for s in range(strat_count):
        result +="(>= (Runtime %d) 0) " % s
    result += "))\n"
    
    # Sum of runtimes <= 300
    result += "(assert (>= 300 (+ "
    for s in range(strat_count):
        result += "(Runtime %d) " % s
    result += ")))\n"
    
    # Specify the number of problems solved
    result += "(assert (= Solved (+\n"
    for p in range(problem_count):
        result += "(ite (or "
        for s in range(strat_count):
            t = dataset.strategy_matrix[p][s]
            if t == -1:
                t = 301
                
            result += "(<= %f (Runtime %d)) " % (t, s)
        result += ") 1 0)\n"
    result += ")))\n"
    
    result += "(assert (>= Solved %d))\n" % number_solved
    
    result += "(check)\n"
    result += "(show-model)\n"
    
    return result

def try_prog(dataset, number_solved):
    with NamedTemporaryFile() as tmp_f:
        prog = gen_prog(dataset, number_solved)
        tmp_f.write(prog)
        tmp_f.flush()
        result = run_command("./yices_main %s" % tmp_f.name, 3600000)
        return result[1].find("unsat") is -1

def search_sat_prog(dataset):
    lowerbound = 1
    upperbound = 11000
    
    while lowerbound != upperbound:
        i = lowerbound + (upperbound - lowerbound) / 2
        print "%d (%d, %d)" % (i, lowerbound, upperbound)
        result = try_prog(dataset, i)
        print result
        
        if result:
            lowerbound = i+1
        else:
            upperbound = i
    
    return lowerbound  # Is equal to upperbound

def main():
    dataset = DataSet()
    dataset.load('E')
    dataset = remove_unsolveable_problems(dataset)
    
    search_sat_prog(dataset)
    
    # Show the program for the best amount of problems solved
    # print gen_prog(dataset, 9945)
    
    return 0

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

    from src.DataSet import DataSet
    from src.data_util import remove_unsolveable_problems
    from src.IO import run_command

    sys.exit(main())
