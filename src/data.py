'''
Created on May 23, 2014

@author: Sil van de Leemput
'''

import os, sys
from argparse import ArgumentParser

def set_up_parser():
    parser = ArgumentParser(description='Van HElsing ' +
                            'dataset tool 0.1 --- May 2014.')
    parser.add_argument('-i', '--inputfile',
                        help='(optional) input dataset file.',
                        default='')
    parser.add_argument('-o', '--outputfile',
                        help='file to save the output dataset to.',
                        default='')
    parser.add_argument('-c', '--configuration',
                        help='Which configuration file to use.',
                        default=os.path.join(PATH, 'config.ini'))
    parser.add_argument('-lp', '--limitprobs',
                        help='Limit the amount of problems in the dataset for testing.',
                        type=int, default=-1)
    return parser

def load_data(argv=sys.argv[1:]):
    """
    input: Config file, (optional dataset)
    output: stores model in modelfile
    """
    LOGGER.info('Loading Data')
    # load config
    parser = set_up_parser()
    args = parser.parse_args(argv)
    configuration = load_config(args.configuration)

    outfile = args.outputfile
    if outfile == '':
        outfile = configuration.get('DataUtil', 'outfile')
    if outfile == '':
        msg = "Could not start process, no output filename was given"
        LOGGER.error(msg)
        raise IOError(99, msg)
       
    # load dataset
    dataset = load_or_generate_dataset(args.inputfile, configuration)


    # remove unsolvable problems
    if configuration.getboolean('DataUtil', 'removeunsolvables'):
        dataset = remove_unsolveable_problems(dataset)
        LOGGER.info("Removing unsolvable problems - prob x strats: %i x %i",
                len(dataset.problems), len(dataset.strategies))

    # retain only a few problems if option set
    if args.limitprobs > -1:
        dataset = dataset.mask(range(args.limitprobs))
        LOGGER.info("Limiting problems - prob x strats: %i x %i",
                    len(dataset.problems), len(dataset.strategies))

    # store strategy matrix as sparse matrix
    try: 
        sparse = configuration.getboolean('DataUtil', 'sparse')
    except:
        sparse = False
    if sparse:
        dataset.sparsify()
        LOGGER.info("Sparsify strategy matrix - nonzero elements / total elements: %i / %i",
                len(dataset.strategy_matrix.nonzero()[0]), (dataset.strategy_matrix.shape[0] * dataset.strategy_matrix.shape[1]))  
  

    # save dataset
    save_object(dataset, outfile)
    LOGGER.info("Dataset saved to: %s.", outfile)


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    
    from src.GlobalVars import PATH, LOGGER
    from src.IO import load_config, save_object
    from src.data_util import remove_unsolveable_problems, load_or_generate_dataset
    
    sys.exit(load_data())
