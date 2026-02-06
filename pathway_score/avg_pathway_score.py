# 1. load packages
print('loading packages')
import pandas as pd
import numpy as np
import sys
import itertools
import csv
import gzip
import re
import gc
from memory_profiler import memory_usage
import time
import inspect
import argparse as ap

# define arguments
def make_arg_parser():
    parser = ap.ArgumentParser(description = ".")

    parser.add_argument('--pathway_map', required = True, help = 'pathway map')

    parser.add_argument('--scale_key', required = True, help = 'scale key')

    parser.add_argument('--output_tag', required = True, help = 'output tag')

    return parser

args = make_arg_parser().parse_args()

# parse arguments
pathway_map = args.pathway_map
scale_key = args.scale_key
output_tag = args.output_tag

# 2. set options
pd.options.mode.copy_on_write = True

# 3. define memory usage function
def print_mem_usage():
    frame = inspect.currentframe()
    caller_frame = frame.f_back
    lineno = caller_frame.f_lineno
    filename = caller_frame.f_code.co_filename
    mem = memory_usage(-1, interval=0.1, timeout=1)
    print(f"[{filename}:{lineno}] Current memory usage: {mem[0]:.2f} MiB")
    
print_mem_usage()

# 4. read in input files
print('reading in input files', flush = True)
print('gs adsp', flush = True)
gene_score_adsp = pd.read_csv(('common_var_gene_score/igap_adsp_gene_score/merged_outputs/AOU_ALL.UKBB.metasoft.ADSP.all.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.gene_symbol.average_gene_score.merged.common_id.transpose.' + scale_key + '.txt.gz'),
                        sep = '\t', low_memory = False)
print('rs rosmap', flush = True)
rnaseq_rosmap = pd.read_csv(('pathway_score/gene_mapping/ROSMAP.RNAseq.TPM5_log2norm.individualids.codinggenes.VEP_v113_genes.gene_symbol.common_id.duplicate_ids_removed.transpose.' + scale_key + '.txt'),
                    sep = '\t')
print('rs 10 msbb', flush = True)
rnaseq_10_msbb = pd.read_csv(('pathway_score/msbb/MSBB.RNAseq.BA_10.19batch.gene_symbol.individualID.mvalue_norm.tpm.log2.coding_genes_only.covar_corrected.common_id.transpose.' + scale_key + '.txt'),
                    sep = '\t')
print('rs 22 msbb', flush = True)
rnaseq_22_msbb = pd.read_csv(('pathway_score/msbb/MSBB.RNAseq.BA_22.19batch.gene_symbol.individualID.mvalue_norm.tpm.log2.coding_genes_only.covar_corrected.common_id.transpose.' + scale_key + '.txt'),
                    sep = '\t')
print('rs 36 msbb', flush = True)
rnaseq_36_msbb = pd.read_csv(('pathway_score/msbb/MSBB.RNAseq.BA_36.19batch.gene_symbol.individualID.mvalue_norm.tpm.log2.coding_genes_only.covar_corrected.common_id.transpose.' + scale_key + '.txt'),
                    sep = '\t')
print('rs 44 msbb', flush = True)
rnaseq_44_msbb = pd.read_csv(('pathway_score/msbb/MSBB.RNAseq.BA_44.19batch.gene_symbol.individualID.mvalue_norm.tpm.log2.coding_genes_only.covar_corrected.common_id.transpose.' + scale_key + '.txt'),
                    sep = '\t')
print('ma rosmap', flush = True)
methyl_rosmap = pd.read_csv(('pathway_score/rosmap/ROSMAP_arrayMethylation_imputed.gene_symbol.individualID.mvalue_norm.weighted_gene_average.common_id.transpose.' + scale_key + '.txt'),
                        sep = '\t')
print('ma msbb', flush = True)
methyl_msbb = pd.read_csv(('pathway_score/msbb/MSBB.methylation_array.19batch.gene_symbol.individualID.mvalue_norm.weighted_gene_average.common_id.transpose.' + scale_key + '.txt'),
                    sep = '\t')
print('sp rosmap', flush = True)
somoscan_rosmap = pd.read_csv(('pathway_score/rosmap/ROSMAP.proteomics.somoscan.individualID.entrez_gene_symbol.common_id.transpose.' + scale_key + '.txt'),
                    sep = '\t')
print('tmt msbb', flush = True)
tmt_msbb = pd.read_csv(('pathway_score/msbb/MSBB.TMT_proteomics.19batch.normalized.gene_symbol.individualID.log2_transformed.common_id.transpose.' + scale_key + '.txt'),
                    sep = '\t')
print('path map', flush = True)
all_path_map = pd.read_csv(('pathway_score/pathway_annotation/' + pathway_map),
                            sep = '\t')
print('id map', flush = True)
id_map_keep_quest_comb = pd.read_csv('pathway_score/id_map/ADSP.ROSMAP.MSBB.keep_quest_comb.id_map.txt',
                              sep = '\t')

print_mem_usage()

print('inital cleaning', flush = True)
# 5. drop phenotype/covariate columns
gene_score_adsp = gene_score_adsp[~gene_score_adsp['GENE'].isin(['ALZ_STATUS',
                                                                    'AGE',
                                                                    'SEX',
                                                                    'PC1',
                                                                    'PC2',
                                                                    'PC3',
                                                                    'PC4',
                                                                    'PC5',
                                                                    'PC6',
                                                                    'PC7',
                                                                    'PC8'])]

# 6. clean methylation data
methyl_rosmap = methyl_rosmap.replace([np.inf, -np.inf], np.nan)
methyl_msbb = methyl_msbb.replace([np.inf, -np.inf], np.nan)

# 7. filter to genes in path map
gene_score_adsp = gene_score_adsp[gene_score_adsp['GENE'].isin(all_path_map['GENE'])]
rnaseq_rosmap = rnaseq_rosmap[rnaseq_rosmap['GENE'].isin(all_path_map['GENE'])]
rnaseq_10_msbb = rnaseq_10_msbb[rnaseq_10_msbb['GENE'].isin(all_path_map['GENE'])]
rnaseq_22_msbb = rnaseq_22_msbb[rnaseq_22_msbb['GENE'].isin(all_path_map['GENE'])]
rnaseq_36_msbb = rnaseq_36_msbb[rnaseq_36_msbb['GENE'].isin(all_path_map['GENE'])]
rnaseq_44_msbb = rnaseq_44_msbb[rnaseq_44_msbb['GENE'].isin(all_path_map['GENE'])]
methyl_rosmap = methyl_rosmap[methyl_rosmap['GENE'].isin(all_path_map['GENE'])]
methyl_msbb = methyl_msbb[methyl_msbb['GENE'].isin(all_path_map['GENE'])]
somoscan_rosmap = somoscan_rosmap[somoscan_rosmap['GENE'].isin(all_path_map['GENE'])]
tmt_msbb = tmt_msbb[tmt_msbb['GENE'].isin(all_path_map['GENE'])]

# 8. set index as gene
gene_score_adsp.set_index('GENE', inplace = True)
rnaseq_rosmap.set_index('GENE', inplace = True)
rnaseq_10_msbb.set_index('GENE', inplace = True)
rnaseq_22_msbb.set_index('GENE', inplace = True)
rnaseq_36_msbb.set_index('GENE', inplace = True)
rnaseq_44_msbb.set_index('GENE', inplace = True)
methyl_rosmap.set_index('GENE', inplace = True)
methyl_msbb.set_index('GENE', inplace = True)
somoscan_rosmap.set_index('GENE', inplace = True)
tmt_msbb.set_index('GENE', inplace = True)
all_path_map.set_index('GENE', inplace = True)

# filter to IDs in keep quest comb
print(gene_score_adsp.shape, flush = True)
gene_score_adsp = gene_score_adsp.loc[:, gene_score_adsp.columns.isin(id_map_keep_quest_comb['CommonID'])]
print(gene_score_adsp.shape, flush = True)

print(rnaseq_rosmap.shape, flush = True)
rnaseq_rosmap = rnaseq_rosmap.loc[:, rnaseq_rosmap.columns.isin(id_map_keep_quest_comb['CommonID'])]
print(rnaseq_rosmap.shape, flush = True)

print(rnaseq_10_msbb.shape, flush = True)
rnaseq_10_msbb = rnaseq_10_msbb.loc[:, rnaseq_10_msbb.columns.isin(id_map_keep_quest_comb['CommonID'])]
print(rnaseq_10_msbb.shape, flush = True)

print(rnaseq_22_msbb.shape, flush = True)
rnaseq_22_msbb = rnaseq_22_msbb.loc[:, rnaseq_22_msbb.columns.isin(id_map_keep_quest_comb['CommonID'])]
print(rnaseq_22_msbb.shape, flush = True)

print(rnaseq_36_msbb.shape, flush = True)
rnaseq_36_msbb = rnaseq_36_msbb.loc[:, rnaseq_36_msbb.columns.isin(id_map_keep_quest_comb['CommonID'])]
print(rnaseq_36_msbb.shape, flush = True)

print(rnaseq_44_msbb.shape, flush = True)
rnaseq_44_msbb = rnaseq_44_msbb.loc[:, rnaseq_44_msbb.columns.isin(id_map_keep_quest_comb['CommonID'])]
print(rnaseq_44_msbb.shape, flush = True)

print(methyl_rosmap.shape, flush = True)
methyl_rosmap = methyl_rosmap.loc[:, methyl_rosmap.columns.isin(id_map_keep_quest_comb['CommonID'])]
print(methyl_rosmap.shape, flush = True)

print(methyl_msbb.shape, flush = True)
methyl_msbb = methyl_msbb.loc[:, methyl_msbb.columns.isin(id_map_keep_quest_comb['CommonID'])]
print(methyl_msbb.shape, flush = True)

print(somoscan_rosmap.shape, flush = True)
somoscan_rosmap = somoscan_rosmap.loc[:, somoscan_rosmap.columns.isin(id_map_keep_quest_comb['CommonID'])]
print(somoscan_rosmap.shape, flush = True)

print(tmt_msbb.shape, flush = True)
tmt_msbb = tmt_msbb.loc[:, tmt_msbb.columns.isin(id_map_keep_quest_comb['CommonID'])]
print(tmt_msbb.shape, flush = True)

# 9. concatenate dfs
all_omics = pd.concat([gene_score_adsp,
                        rnaseq_rosmap,
                        rnaseq_10_msbb,
                        rnaseq_22_msbb,
                        rnaseq_36_msbb,
                        rnaseq_44_msbb,
                        methyl_rosmap,
                        methyl_msbb,
                        somoscan_rosmap,
                        tmt_msbb], axis = 0)
print(all_omics.shape, flush = True)
print_mem_usage()

# 10. take gene level avergaes
print('taking gene level averages', flush = True)
all_gene_avg = all_omics.groupby(all_omics.index).mean()
print(all_gene_avg.shape, flush = True)
print_mem_usage()

del all_omics

# 11. create unique pathway list
path_list = all_path_map['PATHWAY_ID'].unique().tolist()

# 12. create pathway scores with gene level averages
print('creating pathway scores with gene level averages', flush = True)
# 12.1 merge gene averages and pathways
gene_avg_pathway_score = pd.merge(all_path_map, all_gene_avg, left_index = True, right_index = True, how = 'inner')
# 12.2 make gene index column
gene_avg_pathway_score['GENE'] = gene_avg_pathway_score.index
# 12.3 set index as pathway ID
gene_avg_pathway_score.set_index('PATHWAY_ID', inplace = True)
# 12.5 drop pathway name and gene columns
gene_avg_pathway_score = gene_avg_pathway_score.drop(columns = ['GENE'])
# 12.6 take mean per pathway
gene_avg_pathway_score = gene_avg_pathway_score.groupby(gene_avg_pathway_score.index).mean()
print(gene_avg_pathway_score.shape)
# export
gene_avg_pathway_score.to_csv(('pathway_score/rosmap/avg_pathways/AOU_ALL.UKBB.metasoft.gene_score.ROSMAP.RNAseq.methylation.somoscan_proteomics.MSBB.RNAseq.methylation.tmt_proteomics.ADSP.gene_average.pathway_scores.' + output_tag + '.txt'),
sep = '\t',
na_rep = 'NaN')

del gene_avg_pathway_score
gc.collect()

print_mem_usage()

# 13. create datatype specific pathway scores
print('creating datatype specific pathway scores', flush = True)

# 13.1. create dictionary with file paths, output file prefix, and suffix
single_datatype_pathway_score_dict = {
    'gs_adsp' : (gene_score_adsp, 'AOU_ALL.UKBB.metasoft.gene_score.', '_GSadsp'),
    'rs_rosmap' : (rnaseq_rosmap, 'ROSMAP.RNAseq.', '_RSrosmap'),
    'rs_10_msbb' : (rnaseq_10_msbb, 'MSBB.RNAseq.BA_10.', '_RS10msbb'),
    'rs_22_msbb' : (rnaseq_22_msbb, 'MSBB.RNAseq.BA_22.', '_RS22msbb'),
    'rs_36_msbb' : (rnaseq_36_msbb, 'MSBB.RNAseq.BA_36.', '_RS36msbb'),
    'rs_44_msbb' : (rnaseq_44_msbb, 'MSBB.RNAseq.BA_44.', '_RS44msbb'),
    'ma_rosmap' : (methyl_rosmap, 'ROSMAP.arrayMethylation.', '_MArosmap'),
    'ma_msbb' : (methyl_msbb, 'MSBB.methylation_array.', '_MAmsbb'),
    'sp_rosmap' : (somoscan_rosmap, 'ROSMAP.somoscan_proteomics.', '_SProsmap'),
    'tp_msbb' : (tmt_msbb, 'MSBB.TMT_proteomics.', '_TPmsbb'),
}
del gene_score_adsp
del rnaseq_rosmap
del rnaseq_10_msbb
del rnaseq_22_msbb
del rnaseq_36_msbb
del rnaseq_44_msbb
del methyl_rosmap
del methyl_msbb
del somoscan_rosmap
del tmt_msbb
gc.collect()

# 13.2. create empty list
all_pathway_score_list = []

# 13.3. loop through datatypes and create datatype specific pathway scores
for key, (df, output_prefix, suffix) in single_datatype_pathway_score_dict.items():
    print(key, flush = True)

    # 13.3.1 merge gene averages and pathways
    pathway_score_single_datatype = pd.merge(all_path_map, df, left_index = True, right_index = True, how = 'inner')
    # 13.3.2 create gene column from index
    pathway_score_single_datatype['GENE'] = pathway_score_single_datatype.index
    # 13.3.3 set index as pathway ID
    pathway_score_single_datatype.set_index('PATHWAY_ID', inplace = True)
    # 13.3.5 drop pathway name and gene columns
    pathway_score_single_datatype = pathway_score_single_datatype.drop(columns = ['GENE'])
    # 13.3.6 take mean per pathway
    pathway_score_single_datatype = pathway_score_single_datatype.groupby(pathway_score_single_datatype.index).mean()
    # 13.3.7 create output filenames
    pathway_score_single_datatype_filename = ('pathway_score/rosmap/avg_pathways/' + output_prefix + 'ADSP.pathway_average.pathway_scores.' + output_tag + '.txt')
    # 13.3.8. export dataframes
    pathway_score_single_datatype.to_csv(pathway_score_single_datatype_filename,
                                        sep = '\t',
                                        na_rep = 'NaN')
    # 13.3.9 append to list
    all_pathway_score_list.append(pathway_score_single_datatype)

del single_datatype_pathway_score_dict
del pathway_score_single_datatype_filename
del pathway_score_single_datatype
gc.collect()

print_mem_usage()
                                                
# 14. average single datatype pathway scores
print('averaging single datatype pathway scores', flush = True)

# 14.1. merge single datatype pathway scores
pathway_score_avg_pathway = pd.concat(all_pathway_score_list, axis = 0)

# 14.2 take mean per pathway
pathway_score_avg_pathway = pathway_score_avg_pathway.groupby(pathway_score_avg_pathway.index).mean()

print(pathway_score_avg_pathway, flush = True)
print(pathway_score_avg_pathway.shape, flush = True)
print_mem_usage()

# 14.3. export dataframe
# old filepath with just rosmap
pathway_score_avg_pathway.to_csv(('pathway_score/rosmap/avg_pathways/AOU_ALL.UKBB.metasoft.gene_score.ROSMAP.RNAseq.methylation.somoscan_proteomics.MSBB.RNAseq.methylation.tmt_proteomics.ADSP.pathway_average.pathway_scores.' + output_tag + '.txt'),
sep = '\t',
na_rep = 'NaN')