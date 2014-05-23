'''
Created on May 23, 2014

@author: Sil van de Leemput
'''

import os, sys
from argparse import ArgumentParser

from src.GlobalVars import PATH, LOGGER
from src.IO import load_config, load_object, save_object
from src.DataSet import DataSet
from src.data_util import remove_unsolveable_problems


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


def load_dataset(args, configuration):
    dataset = DataSet()
    datasetfile = args.inputfile
    if datasetfile == '':
        datasetfile = configuration.get('DataUtil', 'infile')
    if configuration.getboolean('DataUtil', 'generatedataset'):
        datatype = configuration.get('DataUtil', 'datatype')        
        LOGGER.info("Generating dataset from type: %s.", datatype)
        dataset.load(datatype)
        LOGGER.info("Dataset generated.")
    elif not os.path.isfile(datasetfile):
        msg = "No dataset found for %s." % datasetfile
        LOGGER.error(msg)
        raise IOError(99, msg)        
    else:
        dataset = load_object(datasetfile)
        if not isinstance(dataset, DataSet):
            msg = "file: %s is not of type DataSet" % datasetfile
            LOGGER.error(msg)
            raise IOError(99, msg)
        LOGGER.info("Dataset: %s loaded  prob x strats: %i x %i",
                    datasetfile, len(dataset.problems), len(dataset.strategies))
    return dataset


def main(argv=sys.argv[1:]):
    """
    input: Config file, (optional dataset)
    output: stores model in modelfile
    """
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
    dataset = load_dataset(args, configuration)

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

    # save dataset
    save_object(dataset, outfile)
    LOGGER.info("Dataset saved to: %s.", outfile)


if __name__ == '__main__':
    sys.exit(main())