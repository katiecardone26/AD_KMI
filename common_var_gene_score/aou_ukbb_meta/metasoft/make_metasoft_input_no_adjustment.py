# intialize libaraies 
import pandas as pd
import argparse as ap

# define arguments
def make_arg_parser():
    parser = ap.ArgumentParser(description='.')
    parser.add_argument('--aou_input', required = True, help = "Path to the AOU GWAS input file")
    parser.add_argument('--ukbb_input', required = True, help = "Path to the UKBB GWAS input file")
    parser.add_argument('--output_prefix', required = True, help = "Output prefix")

    return parser

args = make_arg_parser().parse_args()

# convert args to variables
aou_input = args.aou_input
ukbb_input = args.ukbb_input
output_prefix = args.output_prefix

# load the data 
aou = pd.read_csv(aou_input, sep = '\t', dtype = str)
ukbb = pd.read_csv(ukbb_input, sep = '\t', dtype = str)
finngen = pd.read_csv(finngen_input, sep = '\t', dtype = str)

# create ID column in finngen
finngen['MarkerID'] = 'chr' + finngen['#chrom'] + ':' + finngen['pos'] + ':' + finngen['ref'] + ':' + finngen['alt']

# Select relevant columns
aou_sub = aou[['MarkerID', 'BETA', 'SE']]
ukbb_sub = ukbb[['MarkerID', 'BETA', 'SE']]

# Rename columns for merging
aou_sub.rename(columns = {'BETA' : "BETA_AOU", 'SE' : "SE_AOU"}, inplace = True)
ukbb_sub.rename(columns = {'BETA' : "BETA_UKBB", 'SE' : "SE_UKBB"}, inplace = True)

# Merge datasets
union_df = aou_sub.merge(ukbb_sub, on = 'MarkerID', how = 'outer')

# Reorder columns to fit Metasoft format
union_df = union_df[['MarkerID', 'BETA_AOU', 'SE_AOU', 'BETA_UKBB', 'SE_UKBB']]

# make output file names
union_output_file = output_prefix + '.union.txt'

# Write to files
union_df.to_csv(union_output_file, sep = "\t", header = None, index = None, na_rep = 'NA')