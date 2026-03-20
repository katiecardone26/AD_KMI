# load packages
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, average_precision_score, f1_score, balanced_accuracy_score
import sys
import numpy as np
import statsmodels.api as sm
import argparse as ap
import time
import inspect
from datetime import datetime

start_time = datetime.now()
print("Start time:", start_time, flush = True)

# define arguments
def make_arg_parser():
    parser = ap.ArgumentParser(description = ".")

    parser.add_argument('--input_prefix', required = True, help = 'input prefix')

    parser.add_argument('--key_name', required = True, help = 'key name')

    parser.add_argument('--output_tag', required = True, help = 'phrase to add into output filename')

    return parser

args = make_arg_parser().parse_args()

# parse arguments
input_prefix = args.input_prefix
key_name = args.key_name
output_tag = args.output_tag

# read in input files
print('reading in input files', flush = True)
input_dir = '/project/ritchie/projects/AD_KMI/ML/statistical_models/input/'
input_suffix = '.statistical_models_input.txt'

input_df = pd.read_csv((input_dir + input_prefix + input_suffix),
sep = '\t').replace([np.inf, -np.inf], np.nan).dropna(axis = 1)
print(input_df.shape)

# make dictionary
print('running models', flush = True)
file_dict = {key_name: input_df}

# make empty lists
beta_list = []
pval_list = []

# create output directory
output_dir = '/project/ritchie/projects/AD_KMI/ML/statistical_models/lr_output/iterations/'

# make predictors list
predictors = input_df.columns.tolist()
predictors.remove('ID')
predictors.remove('AD')
predictors.remove('Age')
predictors.remove('Sex')
predictors.remove('PC1')
predictors.remove('PC2')
predictors.remove('PC3')
predictors.remove('PC4')

# make empty list
metric_list = []

# loop through pathways
for col in predictors:
    print(col)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(input_df[[col, 'Age', 'Sex', 'PC1', 'PC2', 'PC3', 'PC4']])

    model = sm.Logit(input_df['AD'], X_scaled).fit()
    pval = f"{model.pvalues.iloc[0]:.2e}"
    beta = model.params.iloc[0]
    df = pd.DataFrame(data = {'Feature' : [col], 'BETA' : beta, 'PVAL' : pval})
    metric_list.append(df)

# concat
metric_df = pd.concat(metric_list, axis = 0)

# export dfs
output_dir = '/project/ritchie/projects/AD_KMI/ML/statistical_models/omics_weights/'
metric_df.to_csv(output_dir + 'MULTIOMICS.PATHWAY_SCORES.LR_METRICS.' + key_name + '.' + output_tag + '.csv', index = None)