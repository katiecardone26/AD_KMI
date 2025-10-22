# load packages
import pandas as pd
import argparse as ap

# define and parse arguments
def make_parser():
    parser = ap.ArgumentParser()

    parser.add_argument('--sumstats', help = 'path to summary statistics file (with beta)')
    parser.add_argument('--gene_annot', help = 'path to gene annotations file (variant gene map)')
    parser.add_argument('--chr_col', help = 'chromosome column name in sumstats file')
    parser.add_argument('--pos_col', help = 'position column name in sumstats file')
    parser.add_argument('--ref_col', help = 'reference allele column name in sumstats file')
    parser.add_argument('--alt_col', help = 'alternate allele column name in sumstats file')
    parser.add_argument('--beta_col', help = 'beta column name in sumstats file')
    parser.add_argument('--output', help= ' path to output file')

    return parser

args = make_parser().parse_args()

# make arguments into variables
sumstats_filepath = args.sumstats
gene_annot_filepath = args.gene_annot
chr_col = args.chr_col
pos_col = args.pos_col
ref_col = args.ref_col
alt_col = args.alt_col
beta_col = args.beta_col
output_filepath = args.output

# read in beta and gene files
print("reading in files")
beta = pd.read_csv(sumstats_filepath, sep = '\t', dtype = str)
print(beta)
gene=pd.read_csv(gene_annot_filepath, sep = '\t')
print(gene)

# clean beta file
print("cleaning beta file")
beta['CHR:BP'] = 'chr' + beta[chr_col] + ':' + beta[pos_col]
beta=beta[['CHR:BP', 'ADSP_variant_id', chr_col, pos_col, ref_col, alt_col, beta_col]]
beta.rename(columns = {'ADSP_variant_id' : 'ID',
                        chr_col : 'CHR',
                        pos_col : 'POS',
                        alt_col : 'A1',
                        ref_col : 'A2',
                        beta_col : 'BETA'}, inplace = True)

# clean gene file
print("cleaning gene file")
gene=gene[['CHR:BP', 'Ensembl_ID', 'Gene']]
gene.rename(columns = {'Gene' : 'GENE'}, inplace = True)

# merge beta and gene files
print('merging files')
beta_gene = beta.merge(gene, on = 'CHR:BP')
print(beta_gene)

# clean merged file
print("cleaning merged file")
## drop chr:bp column
beta_gene.drop(columns = ['CHR:BP'], inplace = True)
## drop duplicates
beta_gene.drop_duplicates(inplace = True)

# export file
print('exporting file')
beta_gene.to_csv(output_filepath, sep = '\t', index = None)
