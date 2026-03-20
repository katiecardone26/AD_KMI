# load packages
import pandas as pd
import argparse as ap
from datetime import datetime

# define arguments
def make_arg_parser():
    parser = ap.ArgumentParser(description = '.')
    # sumstats file name
    parser.add_argument('--vep')
    # output prefix
    parser.add_argument('--output_prefix')

    return parser

args = make_arg_parser().parse_args()

# convert args to variables
vep_filepath = args.vep
output_prefix = args.output_prefix

# read in input file
vep = pd.read_csv(vep_filepath ,sep = '\t', comment = '#', header = None)

# create chromosome and position columns
vep[['CHR', 'POS']] = vep[1].str.split(':', 1, expand = True)

# subset columns
vep_sub = vep[[0, 'CHR', 'POS', 3, 4]]

# rename columns
vep_sub.rename(columns = {0 : 'ID',
                            3 : 'GENE',
                            4 : 'ENSEMBL_ID'}, inplace = True)

# identify variants w and w/o gene annotations
vep_gene = vep_sub[~vep_sub['GENE'].isin(['-'])]
vep_no_gene = vep_sub[vep_sub['GENE'].isin(['-'])]

# rename and drop columns
vep_gene.drop(columns = ['ENSEMBL_ID'], inplace = True)
vep_no_gene.drop(columns = ['GENE'], inplace = True)
vep_no_gene.rename(columns = {'ENSEMBL_ID' : 'GENE'}, inplace = True)

# concat
vep_gene_clean = pd.concat([vep_gene, vep_no_gene], axis = 0)

# remove duplicates in which one gene is Ensembl Gene
if vep_gene_clean['ID'].duplicated().any():
    print('duplicated variant IDs')

    # get duplicates variants
    dups = vep_gene_clean[vep_gene_clean.duplicated(subset = ['ID'], keep = False)]

    # make dups list
    dups_list=sorted(list(set(dups['ID'].tolist())))

    # create empty list of dfs
    fixed_dups_dfs = []

    # create dups df
    dups_df = vep_gene_clean[vep_gene_clean['ID'].isin(dups_list)]
    dups_df.sort_values(by = ['ID'], inplace = True)

    # Create a dictionary for faster index lookup
    snp_map = {snp: i for i, snp in enumerate(dups_list)}

    # loop through and correct duplicate IDs
    for snp, snp_df in dups_df.groupby('ID'):
        print(snp_map[snp])
        no_ensg = snp_df[~snp_df['GENE'].str.startswith('ENSG')]
    
        # Append results efficiently
        fixed_dups_dfs.append(snp_df if no_ensg.empty else no_ensg)

    fixed_dups_df=pd.concat(fixed_dups_dfs,axis=0)
    
    # create df with no duplicates
    no_dups = vep_gene_clean[vep_gene_clean['ID'].duplicated() == False]

    # concatenate
    vep_gene_no_dups = pd.concat([no_dups,fixed_dups_df], axis = 0)

    # drop duplicates
    vep_gene_no_dups.drop_duplicates(inplace = True)

# export file
output_filepath = output_prefix + '.vep_output.cleaned.txt'
vep_gene_no_dups.to_csv(output_filepath, sep = '\t', index = None)