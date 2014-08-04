'''
Contains code for loading a dataset.
'''

import os
import sys
import ConfigParser
from argparse import ArgumentParser


def set_up_parser():
    """
    Creates the ArgumentParser instance for use with the CLI
    """
    parser = ArgumentParser(description='Van HElsing ' +
                            'dataset tool 0.2 --- May 2014.')
    parser.add_argument('-i', '--inputfile',
                        help='(optional) Input dataset file.',
                        default='')
    parser.add_argument('-o', '--outputfile',
                        help='File to save the output dataset to.',
                        default='')
    parser.add_argument('-c', '--configuration',
                        help='Which configuration file to use.',
                        default=os.path.join(PATH, 'config.ini'))
    parser.add_argument('-lp', '--limitprobs',
                        help='Puts a max-limit on the amount of problems.',
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
        sparsify = configuration.getboolean('DataUtil', 'sparse')
    except ConfigParser.NoOptionError:
        sparsify = False
    if sparsify:
        dataset.sparsify()
        shape = dataset.strategy_matrix.shape
        total = shape[0] * shape[1]
        text = "Sparsify strat matrix - nonzero / total elements: %i / %i"
        LOGGER.info(text, len(dataset.strategy_matrix.nonzero()[0]), total)

    # save dataset
    save_object(dataset, outfile)
    LOGGER.info("Dataset saved to: %s.", outfile)


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

    from src.GlobalVars import PATH, LOGGER
    from src.IO import load_config, save_object
    from src.data_util import remove_unsolveable_problems, \
        load_or_generate_dataset

    sys.exit(load_data())
