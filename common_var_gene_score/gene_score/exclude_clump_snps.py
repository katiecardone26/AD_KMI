# load packages
import pandas as pd
import argparse as ap
import sys

# define and parse arguments
def make_parser():
    parser = ap.ArgumentParser()

    parser.add_argument('--sumstats', help = 'IGAP sumstats filename')
    parser.add_argument('--clump_exclude', help = 'PLINK clump exclude snplist')
    parser.add_argument('--output', help = 'Output file name')

    return parser

args = make_parser().parse_args()

# convert arguments to variables
sumstats_filename = args.sumstats
clump_filename = args.clump_exclude
output_filename = args.output

# read in input file
sumstats=pd.read_csv(sumstats_filename, sep = '\t', dtype = str)
print(len(sumstats.index))
clump =pd.read_csv(clump_filename, header = None, dtype = str)
print(len(clump.index))

# filter sumstats
sumstats_filt= sumstats[~sumstats['ADSP_variant_id'].isin(clump[0])]
print(len(sumstats_filt.index))

# export dataframe
sumstats_filt.to_csv(output_filename, sep = '\t', index = None)