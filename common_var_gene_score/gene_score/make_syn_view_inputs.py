# import packages
import pandas as pd
import argparse as ap
from decimal import Decimal

# define and parse arguments
def make_arg_parser():
    parser = ap.ArgumentParser(description = ".")

    parser.add_argument('--input_list', required = True, help = 'comma separated logistic regression inputs to put into synthesis view plot')
    parser.add_argument('--pval_col_list', required = True, help = 'comma separated pvalue column names for synthesis view plot, in the same order as input files')
    parser.add_argument('--es_col_list', required = True, help = 'comma separated effect size column names for synthesis view plot, in the same order as input files')
    parser.add_argument('--pval_thres', required = True, help = 'p-value threshold for filtering')
    parser.add_argument('--output_prefix', required = True, help = 'Output prefix')

    return parser

args = make_arg_parser().parse_args()

# turn arguments into variables
input_list = args.input_list.split(',')
pval_col_list = args.pval_col_list.split(',')
es_col_list = args.es_col_list.split(',')
output_prefix = args.output_prefix
pval_thres = float(args.pval_thres)
print(pval_thres)

# read in VEP
adsp_vep_113 = pd.read_csv('/project/ritchie/projects/ADSP_Projects/ADSP_Annotations/VEP_annotation_manual_113/ensembl_start_stop/Homo_sapiens.GRCh38.113.gene_start_stop.refseq.exp_validated.500kb_upstream_downstream.gtf.txt',
             sep = '\t')
print(adsp_vep_113.columns)

# clean VEP
adsp_vep_113 = adsp_vep_113[['ENS_ID', 'GENE', 'CHR', 'START']]
adsp_vep_113.rename(columns =  {'ENS_ID' :'GENE_SCORE',
                                'START' :'Location',
                                'CHR' :'Chromosome',
                                'GENE' :'SNP'}, inplace = True)
adsp_vep_113.sort_values(by = ['Chromosome', 'Location'], inplace = True)
print(len(adsp_vep_113.index))
print(len(adsp_vep_113['GENE_SCORE'].unique()))

# create empty dataframe
gs_syn = pd.DataFrame()

# loop through LR outputs
for index, input_filepath in enumerate(input_list):
    # read in file
    input_dir = '/project/ritchie/projects/AD_KMI/common_var_gene_score/igap_adsp_gene_score/association_study/'
    input = pd.read_csv(input_dir + input_filepath, sep = '\t', dtype = str)
    
    # clean up LR output
    input['GENE_SCORE'] = input['GENE_SCORE'].str.replace('_AVG', '')
    input = input[~input['P'].isin(['Error'])]
    input['P'] = input['P'].apply(lambda x: Decimal(x))
    print(len(input.index))
    print(input.sort_values(by = ['P']))

    # rename p-value column
    pval_colname = pval_col_list[index]
    input.rename(columns = {'P' : pval_colname}, inplace = True)

    # rename effect size column
    es_colname = es_col_list[index]
    input.rename(columns = {'COEF' : es_colname}, inplace = True)

    # merge LR & VEP
    input_vep = adsp_vep_113.merge(input, on = ['GENE_SCORE'], how = 'inner')
    print(len(input_vep.index))
    print(len(input_vep['GENE_SCORE'].unique()))

    # drop and reorder extra cols before merge
    input_vep = input_vep[['SNP', 'Chromosome', 'Location', es_colname, pval_colname]]

    # merge syn view inputs
    if gs_syn.empty:
        gs_syn = input_vep
    else:
        gs_syn = gs_syn.merge(input_vep, on = ['SNP', 'Chromosome', 'Location'], how = 'outer')

    # filter based on p-val
    all_pval_col_list = gs_syn.columns.to_list()
    for col in ['SNP', 'Chromosome', 'Location', es_colname]:
        all_pval_col_list.remove(col)
    gs_syn = gs_syn[(gs_syn[all_pval_col_list] <= pval_thres).any(axis = 1)]
print(gs_syn)
print(gs_syn.shape)

# export dataframe
output_filepath = output_prefix + '.synthesis_view_input.txt'
gs_syn.to_csv(output_filepath, sep = '\t', index = None, na_rep = 'NA')