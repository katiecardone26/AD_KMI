# load packages
import pandas as pd
import argparse as ap
import sys

# define and parse arguments
def make_parser():
    parser = ap.ArgumentParser()

    parser.add_argument('--input', help = 'Input file name')
    parser.add_argument('--output_prefix', nargs = '+', help = 'Output file name')

    return parser

args = make_parser().parse_args()

# convert arguments to variables
input_filename = args.input
output_prefix = args.output_prefix
output_prefix = ''.join(output_prefix)

# read in input file
raw_clump = pd.read_csv(input_filename, sep = '\t')

# subset dataframe
raw_clump_sub = raw_clump[['#CHROM', 'POS', 'ID', 'SP2']]

# create ID list
id_list= raw_clump_sub['ID'].to_list()

# create empty list of dfs
sp2_dfs = []

# loop through ID list to hash out dataframe
for id in id_list:
    # extract variables
    sp2_col = raw_clump_sub[raw_clump_sub['ID'].str.contains(id)]['SP2']
    chr_col = raw_clump_sub[raw_clump_sub['ID'].str.contains(id)]['#CHROM']
    pos_col = raw_clump_sub[raw_clump_sub['ID'].str.contains(id)]['POS']
    id_col = raw_clump_sub[raw_clump_sub['ID'].str.contains(id)]['ID']

    # make sp2 into a list
    sp2_str = sp2_col.reset_index(drop = True)[0]
    sp2_list= sp2_str.split(',')

    # convert other variables into strings
    chr_str =chr_col.reset_index(drop = True)[0]
    pos_str = pos_col.reset_index(drop = True)[0]
    id_str =id_col.reset_index(drop = True)[0]

    # make new dataframe
    new_df = pd.DataFrame({'#CHROM' : chr_str,
                           'POS' : pos_str,
                           'ID' : id_str,
                           'SP2' : sp2_list})
    
    # append to dataframe
    sp2_dfs.append(new_df)

# concatenate dataframes
new_sp2_df = pd.concat(sp2_dfs, axis = 0)

# remove lines with a period
new_sp2_df = new_sp2_df[~new_sp2_df['SP2'].isin(['.'])]

# create SP2 list
new_sp2_only_df = new_sp2_df[['SP2']]

# create output file name
full_output_filename = output_prefix + '.clumped_variants.txt'
var_list_output_filename = output_prefix + '.exclude_variants.txt'

# export dataframes
new_sp2_df.to_csv(full_output_filename, sep = '\t', index = None)
new_sp2_only_df.to_csv(var_list_output_filename, sep = '\t', index = None, header = None)
