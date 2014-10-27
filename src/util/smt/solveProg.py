import sys
from src.DataSet import DataSet
from src.data_util import remove_unsolveable_problems
from src.IO import run_command
from tempfile import NamedTemporaryFile

def gen_prog(dataset, number_solved):
    problem_count, strat_count = dataset.strategy_matrix.shape

    result = ""

    result += "(benchmark test\n"
    result += ":logic QF_UFLRA\n"
    result += ":extrafuns ((Runtime Real Real) (Solved Real))\n"
    result += ":formula\n"
    result += "(and\n"
    
    # All runtimes >= 0
    result += "(and\n"
    for s in range(strat_count):
        result +="(>= (Runtime %d) 0) " % s
    result += ")\n"
    
    # Sum of runtimes <= 300
    result += "(>= 300 (+ \n"
    for s in range(strat_count):
        result += "(Runtime %d) " % s
    result += "))\n"
    
    # Specify the number of problems solved
    result += "(= Solved (+\n"
    for p in range(problem_count):
        result += "(ite (or "
        for s in range(strat_count):
            t = dataset.strategy_matrix[p][s]
            if t == -1:
                t = 301
                
            result += "(<= %f (Runtime %d)) " % (t, s)
        result += ") 1 0)"
    result += "))\n"
    
    result += "(>= Solved %d)\n" % number_solved
    
    result += "))"
    
    return result

def try_prog(dataset, number_solved):
    with NamedTemporaryFile() as tmp_f:
        prog = gen_prog(dataset, number_solved)
        tmp_f.write(prog)
        tmp_f.flush()
        result = run_command("./yices_smt %s" % tmp_f.name, 3600000)
        return result[1].find("unsat") is -1

def main():
    dataset = DataSet()
    dataset.load('E')
    dataset = remove_unsolveable_problems(dataset)
    
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
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
