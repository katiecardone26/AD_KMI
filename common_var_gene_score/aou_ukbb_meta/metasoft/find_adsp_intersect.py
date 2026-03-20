# load packages
print('loading packages')
import pandas as pd
import sys
import argparse as ap

# define and parse arguments
def make_parser():
    parser = ap.ArgumentParser()

    parser.add_argument('--sumstats', help = 'sumstats filepath')
    parser.add_argument('--sumstats_output_prefix', help = 'sumstats output filepath')
    parser.add_argument('--clump_output_prefix', help = 'clump output filepath')

    return parser

args = make_parser().parse_args()

# make arguments into variables
sumstats_filepath = args.sumstats
sumstats_output_prefix = args.sumstats_output_prefix
clump_output_prefix = args.clump_output_prefix

# read in sumstats file
## output
sumstats = pd.read_csv(sumstats_filepath,
                        sep = '\t', dtype = str)
print(sumstats)
## adsp variant list
adsp = pd.read_csv('/project/ritchie/projects/AD_KMI/common_var_gene_score/igap_adsp_gene_score/ADSP_plink_subset/variant_list/ADSP.mac20.noduplicates.geno0.01.mind0.05.maf0.01.new_var_id.all_chr.snplist',
                    header = None)
print(adsp)

# filter to variants in ADSP

## create variant ID columns
print('creating variant id columns')
sumstats['REF_ALT_ID'] = 'chr' + sumstats['CHR'] + ':' + sumstats['POS'] + ':' + sumstats['REF'] + ':' + sumstats['ALT']
sumstats['ALT_REF_ID'] = 'chr' + sumstats['CHR'] + ':' + sumstats['POS'] + ':' + sumstats['ALT'] + ':' + sumstats['REF'] 
print(sumstats)

## find intersections
print('finding intersections')
sumstats_no_flip_intersect = sumstats[sumstats['REF_ALT_ID'].isin(adsp[0])]
sumstats_flip_intersect = sumstats[sumstats['ALT_REF_ID'].isin(adsp[0])]
print(sumstats_no_flip_intersect)
print(sumstats_flip_intersect)

## drop columns
print('dropping columns')
sumstats_no_flip_intersect.drop(columns = ['ALT_REF_ID'], inplace = True)
sumstats_flip_intersect.drop(columns = ['REF_ALT_ID'], inplace = True)
print(sumstats_no_flip_intersect)
print(sumstats_flip_intersect)

## rename columns
print('renaming columns')
sumstats_no_flip_intersect.rename(columns = {'RSID' : 'original_variant_id', 'REF_ALT_ID' : 'ADSP_variant_id'}, inplace = True)
sumstats_flip_intersect.rename(columns = {'RSID' : 'original_variant_id', 'ALT_REF_ID' : 'ADSP_variant_id'}, inplace = True)
print(sumstats_no_flip_intersect)
print(sumstats_flip_intersect)

## concatenate
print('concatenating')
sumstats_adsp_id = pd.concat([sumstats_no_flip_intersect, sumstats_flip_intersect], axis = 0)
print(sumstats_adsp_id)

# create variant ID list
sumstats_adsp_id_var_list = sumstats_adsp_id[['ADSP_variant_id']]

# reformat for plink clump
print('reformatting for plink clump')
clump_input_fe = sumstats_adsp_id[['ADSP_variant_id', 'PVALUE_FE', 'CHR', 'POS', 'ALT']]
clump_input_re = sumstats_adsp_id[['ADSP_variant_id', 'PVALUE_RE', 'CHR', 'POS', 'ALT']]
clump_input_fe.rename(columns = {'ADSP_variant_id' : 'SNP', 'PVALUE_FE': 'P', 'POS': 'BP', 'ALT': 'A1'}, inplace = True)
clump_input_re.rename(columns = {'ADSP_variant_id' : 'SNP', 'PVALUE_RE' : 'P', 'POS' : 'BP', 'ALT' : 'A1'}, inplace = True)
print(clump_input_fe)
print(clump_input_re)

# create output filepaths
sumstats_output_filepath = sumstats_output_prefix + '.txt'
sumstats_var_list_filepath = sumstats_output_prefix + '.variant_list.txt'
clump_fe_output_filepath = clump_output_prefix + '.FE_PVAL.plink_clump_input.txt'
clump_re_output_filepath = clump_output_prefix + '.RE_PVAL.plink_clump_input.txt'

# export sumstats
print('exporting sumstats')
sumstats_adsp_id.to_csv(sumstats_output_filepath, sep = '\t', index = None)
sumstats_adsp_id_var_list.to_csv(sumstats_var_list_filepath, sep = '\t', index = None)
clump_input_fe.to_csv(clump_fe_output_filepath, sep = '\t', index = None)
clump_input_re.to_csv(clump_re_output_filepath, sep = '\t', index = None)