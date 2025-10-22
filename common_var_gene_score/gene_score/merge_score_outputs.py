# load python modules
import pandas as pd
import argparse as ap
import os
import sys

# define and parse arguments
def make_arg_parser():
    parser = ap.ArgumentParser(description = ".")

    parser.add_argument('--score_prefix', required = True, help = 'score filename prefix (before chromosome number)')
    parser.add_argument('--pheno', required = True, help = 'phenotype filename')
    parser.add_argument('--pheno_id_col', required = True, help = 'phenotype file ID column name')
    parser.add_argument('--output_prefix', required = True, help = 'Output prefix (before chromosome number)')

    return parser

args = make_arg_parser().parse_args()

# turn arguments into variables
score_prefix = args.score_prefix
pheno_filename = args.pheno
pheno_id_col = args.pheno_id_col
output_prefix = args.output_prefix


avg_dfs = []
sum_dfs = []
for chr in list(range(1, 23)):
    print_string = "processing chromosome " + str(chr)
    print(print_string)
    
    score_filename = score_prefix + str(chr) + '.txt'
    score=pd.read_csv(score_filename,sep='\t',dtype=str)
    
    id_df = score[['IID']]
    avg_df = score.filter(regex = '_AVG')
    sum_df = score.filter(regex = '_SUM')

    avg_df_cat = pd.concat([id_df, avg_df], axis = 1)
    sum_df_cat = pd.concat([id_df, sum_df], axis = 1)

    avg_df_cat.set_index(['IID'], inplace = True)
    sum_df_cat.set_index(['IID'], inplace = True)

    avg_dfs.append(avg_df_cat)
    sum_dfs.append(sum_df_cat)

print("concatenating dataframes")    
avg_all_chr = pd.concat(avg_dfs, axis = 1)
print(avg_all_chr)
print(avg_all_chr.shape)
print(len(avg_all_chr.columns.unique()))
sum_all_chr = pd.concat(sum_dfs, axis = 1)
print(sum_all_chr.shape)
print(len(sum_all_chr.columns.unique()))

# remove RNA genes
## read in RNA file
rna_avg = pd.read_csv('adsp_vep_min_gene_pos/v110/duplicate_rna_genes_avg_gene_score.txt', header = None)
print(rna_avg)
## add sum suffixes (avg is already there)
rna_sum = rna_avg.copy()
rna_sum[0] = rna_sum[0].str.replace('_AVG','_SUM')
print(rna_sum)
## create keep lists
avg_keep = list(set(avg_all_chr.columns.to_list()) - set(rna_avg[0]))
sum_keep = list(set(sum_all_chr.columns.to_list()) - set(rna_sum[0]))
## remove
print(len(avg_all_chr.shape))
avg_all_chr = avg_all_chr[avg_keep]
print(len(avg_all_chr.shape))

print(len(sum_all_chr.shape))
sum_all_chr = sum_all_chr[sum_keep]
print(len(sum_all_chr.shape))

# check if there are still duplicates
if len(avg_all_chr.columns) != len(set(avg_all_chr.columns)):
    print('duplicates still exist, making and exporting gene lists for find duplicates and exiting')

    # create gene file
    avg_gene_list = avg_all_chr.columns.to_frame()
    sum_gene_list = sum_all_chr.columns.to_frame()

    # create duplicate file names
    avg_gene_list_filename = output_prefix + '.avg_gene_list.txt'
    sum_gene_list_filename = output_prefix + '.sum_gene_list.txt'

    # export gene file
    avg_gene_list.to_csv(avg_gene_list_filename, sep = '\t', header = None, index = None)
    sum_gene_list.to_csv(sum_gene_list_filename, sep = '\t', header = None, index = None)

    # exit
    sys.exit()

elif len(avg_all_chr.columns) == len(set(avg_all_chr.columns)):
    print('no duplicates exist, continuing')

else:
    print('there is an error, exiting')
    sys.exit()

# add phenotype and covariates
print("reading in phenotype dataframe")
pheno=pd.read_csv(pheno_filename, sep = '\t')
pheno=pheno[[pheno_id_col, 'DX_harmonized', 'Age_harmonized', 'Sex', 'PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8']]
pheno.rename(columns = {pheno_id_col : 'ID',
                        'DX_harmonized' : 'ALZ_STATUS',
                        'Age_harmonized' : 'AGE',
                        'Sex' : 'SEX'}, inplace = True)

avg_all_chr.insert(0, 'ID', avg_all_chr.index, False)
sum_all_chr.insert(0, 'ID', sum_all_chr.index, False)
print("merging phenotype and gene dataframes")
avg_final_pheno = pheno.merge(avg_all_chr, on = 'ID')
print(avg_final_pheno)
sum_final_pheno = pheno.merge(sum_all_chr, on = 'ID')
print(sum_final_pheno)

print("exporting dataframes")
# make output filenames
avg_output_filename = output_prefix + '.average_gene_score.merged.txt'
print(avg_output_filename)
sum_output_filename = output_prefix + '.sum_gene_score.merged.txt'

# export dataframes
avg_final_pheno.to_csv(avg_output_filename, sep = '\t', index = False)
sum_final_pheno.to_csv(sum_output_filename, sep = '\t', index = False)

