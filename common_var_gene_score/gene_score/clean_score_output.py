# import packages
import pandas as pd
import argparse as ap
import numpy as np
import warnings
import sys

# supress warnings
warnings.simplefilter(action = 'ignore', category = FutureWarning)

# define and parse arguments
def make_arg_parser():
    parser = ap.ArgumentParser(description = ".")

    parser.add_argument('--score_prefix', required = True, help = 'score filename prefix (before chromosome number)')
    parser.add_argument('--beta_gene', required = True, help = 'beta gene filename')
    parser.add_argument('--output_prefix', required = True, help = 'Output prefix (before chromosome number)')
    parser.add_argument('--chrom', required = True, help = 'Chromosome')

    return parser

args = make_arg_parser().parse_args()

# turn arguments into variables
score_prefix = args.score_prefix
beta_gene_filename = args.beta_gene
output_prefix = args.output_prefix
chrom = args.chrom
print(chrom)

# read in input files
print("reading in files")
# build score filename
score_filename = score_prefix + str(chrom) + '.sscore'
score = pd.read_csv(score_filename, sep = '\t', dtype = 'str')
gene = pd.read_csv(beta_gene_filename, sep = '\t')

# clean score file
## rename ID column
score.rename(columns = {'#IID' : 'IID'}, inplace = True)

print('processing input files')
# filter gene file to chromosome of interest
gene=gene[gene['CHR'] == int(chrom)]
print(gene['CHR'].unique())
# get number of genes per chromosome
gene_counts=gene['Ensembl_ID'].value_counts().to_frame()
gene_counts['GENE_NAME'] = gene_counts.index
gene_counts.sort_values(by = ['GENE_NAME'], inplace = True)
gene_counts.drop(columns = ['GENE_NAME'], inplace = True)
gene_counts_transposed = gene_counts.transpose()
gene_counts_rep = pd.DataFrame(np.repeat(gene_counts_transposed.values, len(score.index), axis = 0))
gene_counts_rep.columns = gene_counts_transposed.columns

# merge with score file
score_gene_counts = pd.concat([score, gene_counts_rep], axis = 1)

# create gene list
gene_list=gene['Ensembl_ID'].unique().tolist()

# create gene score average columns
print('creating gene score average columns')
gene_dfs=[]
for gene in gene_list:
    gene_sum_colname = gene + '_SUM'
    gene_avg_colname = gene + '_AVG'
    if gene_sum_colname in score_gene_counts.columns:
        gene_df = score_gene_counts[['IID', gene_sum_colname, gene]]
        gene_df[gene_sum_colname] = gene_df[gene_sum_colname].astype(float)
        gene_df[gene_avg_colname] = gene_df[gene_sum_colname] / gene_df[gene]
        gene_df.drop(columns = [gene], inplace = True)
        gene_df.set_index('IID', inplace = True)
        gene_dfs.append(gene_df)
    else:
        continue
gene_avg_cat = pd.concat(gene_dfs, axis = 1)
print(gene_avg_cat)

# export dataframe
# build output filename
output_filename = output_prefix + str(chrom) + '.txt'
print('exporting dataframe')
gene_avg_cat.to_csv(output_filename, sep = '\t')
