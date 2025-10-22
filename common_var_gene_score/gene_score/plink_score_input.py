# load python packages
import pandas as pd
import argparse as ap

# define and parse arguments
def make_arg_parser():
    parser = ap.ArgumentParser(description = ".")

    parser.add_argument('--beta_gene', required = True, help = 'Beta Gene filename')
    parser.add_argument('--chrom', required = True, help = 'Chromosome')
    parser.add_argument('--output_prefix', required = True, help = 'Output prefix')

    return parser

args = make_arg_parser().parse_args()

# set argument variables
beta_gene_filename = args.beta_gene
chrom = args.chrom
output_prefix = args.output_prefix
print(chrom)

# read in input files
print("reading in file")
beta_gene = pd.read_csv(beta_gene_filename, sep = '\t', dtype = {'beta' : str})
print(beta_gene)
print(beta_gene['CHR'].unique())

# convert beta column to float
beta_gene['BETA'] = beta_gene['BETA'].astype(float)

# create empty list of dataframes
chr_dfs = []
print("filtering by chromosome")
# filter to chromosome of interest
chr_file = beta_gene.loc[beta_gene['CHR'] == int(chrom)]
print(chr_file)
# create gene list
gene_list = chr_file['Ensembl_ID'].unique().tolist()
# loop through genes and make plink score input
print("looping through gene file and making gene-separated dataframes")
for gene in gene_list:
    gene_file = chr_file.loc[chr_file['Ensembl_ID'] == gene]
    gene_file = gene_file[['ID', 'A1', 'BETA']]
    gene_file = gene_file.set_index(['ID', 'A1'])
    gene_file.rename(columns = {'BETA' : gene}, inplace = True)
    gene_file.drop_duplicates(inplace = True)
    chr_dfs.append(gene_file)
# concatenate dataframes
print("concatenating gene separated dataframes")
chr_cat = pd.concat(chr_dfs, axis = 1)
# fill missing values with zeros
print("filling missing values with zeros")
chr_cat = chr_cat.fillna(0)
# drop duplicates
print("dropping duplicates")
chr_cat.drop_duplicates(inplace = True)
# build output file
output_filename = output_prefix + chrom + '.txt'
# export file
chr_cat.to_csv(output_filename, sep = '\t', header = True, index = True)
