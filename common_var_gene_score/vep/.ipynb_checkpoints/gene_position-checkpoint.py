# load packages
import pandas as pd
import argparse as ap
import sys

# create arguments
def make_arg_parser():
    parser = ap.ArgumentParser(description = ".")
    
    parser.add_argument('--chrom', required = True, help = 'chromosome')
    parser.add_argument('--start_col', required = True, help = 'Gene start position column name')
    parser.add_argument('--stop_col', required = True, help = 'Gene stop position column name')
    parser.add_argument('--output_suffix', required = True, help = 'output suffix')
    
    return parser

args = make_arg_parser().parse_args()

# define arguments as variables
chrom = args.chrom
start_col = args.start_col
stop_col = args.stop_col
output_suffix = args.output_suffix

# create vep input file path
vep_filepath = 'VEP_cleaned/ADSP.chr' + str(chrom) + '.base_cleaning.no_consequence.txt'

# read in input files
pos = pd.read_csv('ensembl_start_stop/Homo_sapiens.GRCh38.113.gene_start_stop.refseq.exp_validated.500kb_upstream_downstream.gtf.txt', sep = '\t')
vep = pd.read_csv(vep_filepath, sep = '\t', header = None)

# drop gene column from vep
vep.drop(columns = [3],inplace = True)

# filter pos file to chromosome of interest
pos = pos[pos['CHR'].isin([int(chrom)])]

# create chr and position columns in vep file
vep[['CHR','POS']] = vep[1].str.split(':', expand = True)

# convert pos column to integer
vep['POS'] = vep['POS'].astype(int)

# create gene list from position file
gene_list = pos['Ensembl_ID'].unique().tolist()

# create empty list of dfs
gene_dfs = [] # variants that fit inside gene coordinates
dup_genes = [] # duplicate genes in position file
no_pos = [] # genes that did not have any variants within position constraints

# reset vep index
vep.reset_index(inplace = True, drop = True)

# loop through genes
for gene in gene_list:
    # filter to gene in vep file and reset index
    #vep_gene = vep[vep[5].isin([gene])]
    #vep_gene.reset_index(inplace = True, drop = True)

    # filter to gene in position file, check if there are more than 1 row
    pos_gene = pos[pos['Ensembl_ID'].isin([gene])]
    if len(pos_gene.index) != 1:
        print('more than one row in position file for ' + str(gene))
        dup_genes.append(gene)
        continue
    
    # extract start and stop positions
    start = pos_gene.iloc[0][start_col]
    stop = pos_gene.iloc[0][stop_col]

    # add gene column back
    vep_gene = vep.copy()
    vep_gene.insert(3,'Ensembl_ID',gene)

    
    # extract rows that are within position boundaries
    vep_gene = vep_gene[vep_gene['POS'] >= start]
    vep_gene = vep_gene[vep_gene['POS'] <= stop]
    
    # check if any variants fit the position reqs
    if len(vep_gene.index) > :

        # concentate list of dataframe
        gene_fit = vep_gene

        # append to gene df list
        gene_dfs.append(gene_fit)
    
    else:
        no_pos.append(gene)
    
# concetenate gene dataframes
gene_final = pd.concat(gene_dfs, axis = 0)
print(gene_final)
print(vep.shape)
print(gene_final.shape)

# make and export dup genes
if len(dup_genes) > 0:
    dup_df = pd.DataFrame(data = {'GENE' : dup_genes})
    dup_output_filename = 'VEP_cleaned/ADSP.chr' + str(chrom) + str(output_suffix) + '.duplicates'
    dup_df.to_csv(dup_output_filename, sep = '\t', index = None)

# make and export genes that did not fit position reqs
if len(no_pos) > 0:
    no_pos_df = pd.DataFrame(data = {'GENE' : no_pos})
    no_pos_output_filename = 'VEP_cleaned/ADSP.chr' + str(chrom) + str(output_suffix) + '.genes_with_no_variants.txt'
    no_pos_df.to_csv(no_pos_output_filename, sep = '\t', index = None)

# create output file path
output_filepath = 'VEP_cleaned/ADSP.chr' + str(chrom) + str(output_suffix) + '.txt'

# export file
gene_final.to_csv(output_filepath, sep = '\t', index = None, header = None)
