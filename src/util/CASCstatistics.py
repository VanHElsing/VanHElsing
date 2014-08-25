import sys
import os
import numpy as np

from argparse import ArgumentParser

UNSEEN_PROBLEMS = [
    "ARI626=1.p", "ARI627=1.p", "BIO001+1.p", "DAT071=1.p", "DAT072=1.p", "DAT073=1.p", "DAT074=1.p", "DAT075=1.p",
    "DAT076=1.p", "DAT077=1.p", "DAT078=1.p", "DAT079=1.p", "DAT080=1.p", "DAT081=1.p", "DAT082=1.p", "DAT083=1.p",
    "DAT084=1.p", "DAT085=1.p", "DAT086=1.p", "DAT087=1.p", "DAT088=1.p", "DAT089=1.p", "DAT090=1.p", "DAT091=1.p",
    "DAT092=1.p", "DAT093=1.p", "DAT094=1.p", "DAT095=1.p", "DAT097=1.p", "DAT098=1.p", "DAT099=1.p", "DAT100=1.p",
    "DAT101=1.p", "DAT102=1.p", "DAT103=1.p", "DAT104=1.p", "DAT105=1.p", "DAT106=1.p", "HWV087=1.p", "HWV087_1.p",
    "HWV087-1.p", "HWV087+1.p", "HWV088=1.p", "HWV088_1.p", "HWV088-1.p", "HWV088+1.p", "HWV089=1.p", "HWV089_1.p",
    "HWV089-1.p", "HWV089+1.p", "HWV090=1.p", "HWV090_1.p", "HWV090-1.p", "HWV090+1.p", "HWV091=1.p", "HWV091_1.p",
    "HWV091-1.p", "HWV091+1.p", "HWV092=1.p", "HWV092_1.p", "HWV092-1.p", "HWV092+1.p", "HWV093=1.p", "HWV093_1.p",
    "HWV093-1.p", "HWV093+1.p", "HWV094=1.p", "HWV094_1.p", "HWV094-1.p", "HWV094+1.p", "HWV095=1.p", "HWV095_1.p",
    "HWV095-1.p", "HWV095+1.p", "HWV096=1.p", "HWV096_1.p", "HWV096-1.p", "HWV096+1.p", "HWV097=1.p", "HWV097_1.p",
    "HWV097-1.p", "HWV097+1.p", "HWV098=1.p", "HWV098_1.p", "HWV098-1.p", "HWV098+1.p", "HWV099=1.p", "HWV099_1.p",
    "HWV099-1.p", "HWV099+1.p", "HWV100=1.p", "HWV100_1.p", "HWV100-1.p", "HWV100+1.p", "HWV101=1.p", "HWV101_1.p",
    "HWV101-1.p", "HWV101+1.p", "HWV102=1.p", "HWV102_1.p", "HWV102-1.p", "HWV102+1.p", "HWV103=1.p", "HWV103_1.p",
    "HWV103-1.p", "HWV103+1.p", "HWV104=1.p", "HWV104_1.p", "HWV104-1.p", "HWV104+1.p", "HWV105=1.p", "HWV105_1.p",
    "HWV105-1.p", "HWV105+1.p", "HWV106=1.p", "HWV106_1.p", "HWV106-1.p", "HWV106+1.p", "HWV107=1.p", "HWV107_1.p",
    "HWV107-1.p", "HWV107+1.p", "HWV108=1.p", "HWV108_1.p", "HWV108-1.p", "HWV108+1.p", "HWV109=1.p", "HWV109_1.p",
    "HWV109-1.p", "HWV109+1.p", "HWV110=1.p", "HWV110_1.p", "HWV110-1.p", "HWV110+1.p", "HWV111=1.p", "HWV111_1.p",
    "HWV111-1.p", "HWV111+1.p", "HWV112=1.p", "HWV112_1.p", "HWV112-1.p", "HWV112+1.p", "HWV113=1.p", "HWV113_1.p",
    "HWV113-1.p", "HWV113+1.p", "HWV114=1.p", "HWV114_1.p", "HWV114-1.p", "HWV114+1.p", "HWV115=1.p", "HWV115_1.p",
    "HWV115-1.p", "HWV115+1.p", "HWV116=1.p", "HWV116_1.p", "HWV116-1.p", "HWV116+1.p", "HWV117=1.p", "HWV117_1.p",
    "HWV117-1.p", "HWV117+1.p", "HWV118=1.p", "HWV118_1.p", "HWV118-1.p", "HWV118+1.p", "HWV119=1.p", "HWV119_1.p",
    "HWV119-1.p", "HWV119+1.p", "HWV120=1.p", "HWV120_1.p", "HWV120-1.p", "HWV120+1.p", "HWV121=1.p", "HWV121_1.p",
    "HWV121-1.p", "HWV121+1.p", "HWV122=1.p", "HWV122_1.p", "HWV122-1.p", "HWV122+1.p", "HWV123=1.p", "HWV123_1.p",
    "HWV123-1.p", "HWV123+1.p", "HWV124=1.p", "HWV124_1.p", "HWV124-1.p", "HWV124+1.p", "HWV125=1.p", "HWV125_1.p",
    "HWV125-1.p", "HWV125+1.p", "HWV126=1.p", "HWV126_1.p", "HWV126-1.p", "HWV126+1.p", "HWV127=1.p", "HWV127_1.p",
    "HWV127-1.p", "HWV127+1.p", "HWV128=1.p", "HWV128_1.p", "HWV128-1.p", "HWV128+1.p", "HWV129=1.p", "HWV129_1.p",
    "HWV129-1.p", "HWV129+1.p", "HWV130=1.p", "HWV130-1.p", "HWV130+1.p", "HWV131=1.p", "HWV131_1.p", "HWV131-1.p",
    "HWV131+1.p", "HWV132=1.p", "HWV132_1.p", "HWV132-1.p", "HWV132+1.p", "HWV133=1.p", "HWV133_1.p", "HWV133-1.p",
    "HWV133+1.p", "HWV134=1.p", "HWV134_1.p", "HWV134-1.p", "HWV134+1.p", "PHI001^1.p", "PHI002^1.p", "PHI002^2.p",
    "PHI003^1.p", "PHI003^2.p", "PHI004^1.p", "PHI004^2.p", "PHI005^1.p", "PHI005^2.p", "PHI005^3.p", "PUZ139_1.p",
    "PUZ140^1.p", "SWW573=2.p", "SWW574=2.p", "SWW575=2.p", "SWW576=2.p", "SWW577=2.p", "SWW578=2.p", "SWW579=2.p",
    "SWW580=2.p", "SWW581=2.p", "SWW582=2.p", "SWW583=2.p", "SWW584=2.p", "SWW585=2.p", "SWW586=2.p", "SWW587=2.p",
    "SWW588=2.p", "SWW589=2.p", "SWW590=2.p", "SWW591=2.p", "SWW592=2.p", "SWW593=2.p", "SWW594=2.p", "SWW595=2.p",
    "SWW596=2.p", "SWW597=2.p", "SWW598=2.p", "SWW599=2.p", "SWW600=2.p", "SWW601=2.p", "SWW602=2.p", "SWW603=2.p",
    "SWW604=2.p", "SWW605=2.p", "SWW606=2.p", "SWW607=2.p", "SWW608=2.p", "SWW609=2.p", "SWW610=2.p", "SWW611=2.p",
    "SWW612=2.p", "SWW613=2.p", "SWW614=2.p", "SWW615=2.p", "SWW616=2.p", "SWW617=2.p", "SWW618=2.p", "SWW619=2.p",
    "SWW620=2.p", "SWW621=2.p", "SWW622=2.p", "SWW623=2.p", "SWW624=2.p", "SWW625=2.p", "SWW626=2.p", "SWW627=2.p",
    "SWW628=2.p", "SWW629=2.p", "SWW630=2.p", "SWW631=2.p", "SWW632=2.p", "SWW633=2.p", "SWW634=2.p", "SWW635=2.p",
    "SWW636=2.p", "SWW637=2.p", "SWW638=2.p", "SWW639=2.p", "SWW640=2.p", "SWW641=2.p", "SWW642=2.p", "SWW643=2.p",
    "SWW644=2.p", "SWW645=2.p", "SWW646=2.p", "SWW647=2.p", "SWW648=2.p", "SWW649=2.p", "SWW650=2.p", "SWW651=2.p",
    "SWW652=2.p", "SWW653=2.p", "SWW654=2.p", "SWW655=2.p", "SWW656=2.p", "SWW657=2.p", "SWW658=2.p", "SWW659=2.p",
    "SWW660=2.p", "SWW661=2.p", "SWW662=2.p", "SWW663=2.p", "SWW664=2.p", "SWW665=2.p", "SWW666=2.p", "SWW667=2.p",
    "SWW668=2.p", "SWW669=2.p", "SWW670=2.p", "SWW671=2.p", "SWW672=2.p"]


def main(argv):
    parser = ArgumentParser(description='CASCJ7 statistics script.\n')
    parser.add_argument('-d', '--dataset',
                        help='Directory with CASCJ7 problems',
                        default=None)
    
    args = parser.parse_args(argv)

    dataset = DataSet()
    dataset.load('E')
    
    path = args.dataset
    
    if path is None:
        print "Use -d, or run bin/test_CASCJ7"
        return 1
    
    problems = []
    old_problems = []
    new_problems = []
    completely_new_problems = []
    
    for problem_dir in os.listdir(path):
        problem_subdir = os.path.join(path, problem_dir)
        if not os.path.isdir(problem_subdir):
            continue
        
        for problem_file in os.listdir(problem_subdir):
            if problem_file[0] == '.':
                continue
        
            problem_tuple = (problem_file, os.path.join(path, problem_dir, problem_file))
            problems.append(problem_tuple)
            
            if problem_file not in dataset.problems:
                new_problems.append(problem_tuple)
            else:
                old_problems.append(problem_tuple)
            
            if problem_file in UNSEEN_PROBLEMS:
                completely_new_problems.append(problem_tuple)
    
    lost_new_problems = [p for p in new_problems if p not in completely_new_problems]
    
    problem_filter = np.max(dataset.strategy_matrix, axis=1) < 0
    dataset = dataset.mask(problem_filter)
    
    problem_indices = []
    for problem_file, problem_path in problems:
        if problem_file in dataset.problems:
            problem_indices.append(list(dataset.problems).index(problem_file))
    
    datasetcopy = dataset.mask(problem_indices)
    
    print "Seen problems: %i" % len(old_problems)
    print "Unseen problems: %i" % len(new_problems)
    print "Unseen problems: %i (according to CASC)" % len(completely_new_problems)
    print "Unseen problems: %i (out-of-date PEGASUS)" % len(lost_new_problems)
    print "Unsolvable problems: %i (excluding unseen)" % len(datasetcopy.problems)
    
    print "Unseen problem set (CASC): "
    print [x[0] for x in completely_new_problems]
    
    print "Unseen problem set (out-of-date PEGASUS): "
    print [x[0] for x in lost_new_problems]
    
    unknown_problems = []
    unknown_problems.extend(new_problems)
    for problem_file, problem_path in old_problems:
        if problem_file in datasetcopy.problems:
            unknown_problems.append((problem_file, problem_path))
    
    print "Running unknown problems (%i problems)" % len(unknown_problems)
    atp_eval_problems([p[1] for p in unknown_problems], "helsing", 600, outfile="runs/real/E/atp_eval_CASCJ7_unknown")

    return 0


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.DataSet import DataSet
    from src.eval.atp_evaluations import atp_eval_problems

    sys.exit(main(sys.argv[1:]))
