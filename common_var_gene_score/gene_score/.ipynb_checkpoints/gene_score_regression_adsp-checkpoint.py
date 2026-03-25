print('importing python modules')
import os
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import itertools
import warnings
import argparse as ap
from statsmodels.tools.sm_exceptions import ConvergenceWarning, PerfectSeparationError
warnings.simplefilter('ignore', ConvergenceWarning)
warnings.filterwarnings("ignore", category = RuntimeWarning)

# set up arguments
def make_arg_parser():
    parser = ap.ArgumentParser(description = ".")
    
    parser.add_argument('--gene_score', required = True, help = 'gene score input file name and path')
    parser.add_argument('--pheno', required = True, help = 'pheno input file name and path')
    parser.add_argument('--pheno_id_col', required = True, help = 'id column name in pheno file')
    parser.add_argument('--output', required = True, help = 'output file name and path')
    
    return parser

# parse args
args = make_arg_parser().parse_args()

gene_score_filepath = args.gene_score
pheno_filepath = args.pheno
pheno_id_col = args.pheno_id_col
output_filepath = args.output

# read in input files
# gene score
print('reading in gene score file')
score = pd.read_csv(gene_score_filepath, sep = '\t')
print(score)
# pheno
pheno = pd.read_csv(pheno_filepath, sep = '\t')
print(pheno)

# filter gene scores to people in pheno file
score = score[score['ID'].isin(pheno[pheno_id_col])]
print(len(score.index))

# make gene score list
print('making list of gene scores')
gene_list = score.columns.to_list()
pheno_covar_list = ['ID', 'ALZ_STATUS', 'AGE', 'SEX', 'PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8']
for i in pheno_covar_list:
    gene_list.remove(i)
print(gene_list[0])


# loop through genes
print('looping through genes')
dfs = []
for gene in gene_list:
    print('processing ' + gene)

    design_str = f"ALZ_STATUS ~ {gene} + SEX + AGE + PC1 + PC2 + PC3 + PC4 + PC5 + PC6 + PC7 + PC8"

    try:
        log_reg = smf.logit(design_str, data = score, missing = 'drop').fit(maxiter = 100, disp = 0)
        print(log_reg.params)
        dict = {'GENE_SCORE' : gene,
                'COEF' : log_reg.params[1],
                'P' : log_reg.pvalues[1]}
        df = pd.DataFrame(dict, index = [0])
    except np.linalg.LinAlgError as err:
        print("LinAlgError")
        dict = {'GENE_SCORE' : gene,
                'COEF' : 'Error',
                'P' : 'Error'}
        df = pd.DataFrame(dict, index = [0])
    except PerfectSeparationError as err:
        print("PerfectSeparationError")
        dict = {'GENE_SCORE' : gene,
                'COEF' : 'Error',
                'P' : 'Error'}
        df = pd.DataFrame(dict, index = [0])
    except Exception as err:
        print("Exception")
        dict = {'GENE_SCORE' : gene,
                'COEF' : 'Error',
                'P' : 'Error'}
        df = pd.DataFrame(dict, index = [0])
    dfs.append(df)

# concatenate dfs
print('concatenating dataframes')
final_df = pd.concat(dfs,axis = 0, ignore_index = True)
print(final_df)

# export dataframe
print('exporting dataframe')
final_df.to_csv(output_filepath, sep = '\t', index = None)