#!/bin/bash

# BSUB parameters
######################################################################

#BSUB -J adsp_gene_score_regression[1]
# Job name and (optional) job array properties, in the format
#   "jobname"
# for a simple job, or
#   "jobname[min-max:step]%limit"
# for an array job, where
#   'jobname' is the label shown in job status and summary displays
#   'min' is the first array index
#   'max' is the last array index
#   'step' is the step value between array indecies
#   'limit' is the number of array sub-jobs that can run at once
# In an array job, the variable $LSB_JOBINDEX will contain the index
# of the current sub-job

#BSUB -o logs/adsp_gene_score_regression.%J.%I.out 
# Filename to append the job's stdout; change to -oo to overwrite.
#'%J' becomes the job ID number, '%I' becomes the array index.

#BSUB -e logs/adsp_gene_score_regression.%J.%I.err
# Filename to append the job's stderr; change to -eo to overwrite. 
# If omitted, stderr is combined with stdout. 
# '%J' becomes the job ID number, '%I' becomes the array index.

#BSUB -R "span[hosts=1]"
# Require all cores to be on the same host (for multi-threaded, non-MPI).

#-#BSUB -B
# Send email notification when the job starts

#-#BSUB -N
# Send email notification when the job finishes; otherwise, summary is written to the output file

#BSUB -R "rusage[mem=200000]"
# Per-process memory reservation, in MB.
# (Ensures the job will have this minimum memory.)

#BSUB -M 200000
# Per-process memory limit, in MB.
# (Ensures the job will not exceed this maximum memory.)

#BSUB -v 200000
# Total process virtual (swap) memory limit, in MB.

#-#BSUB -W 24:00
# Wall time limit, in the format "hours:minutes".
#-#BSUB -n 1
# Number of cores to reserve (on one or more hosts: ; see below).
# The variable $LSB_HOSTS lists allocated hosts like "hostA hostA hostB";
# the variable $LSB_MCPU_HOSTS lists allocated hosts like "hostA 2 hostB 1")

#-#BSUB -R "span[ptile=1]"
# Maximum number of cores to reserve on each host (for MPI).

#BSUB -R "select[ostype>=CENT7]"
# Require that the job runs on CentOS 7 host(s).

######################################################################

# define parallelization variables
## merged output
MERGED_OUTPUT=(
        'AOU_ALL.UKBB.metasoft.ADSP.all.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.average_gene_score.merged.txt.gz'
)

PHENO=(
        'keep_quest_comb'
)

OUTPUT=(
        'AOU_ALL.UKBB.metasoft.ADSP.keep_quest_comb.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.average_gene_score.logistic_regression_output.txt'
)


# Get the index of the current job
INDEX=$((LSB_JOBINDEX-1))

# Define parallelization variable indices
## merged output file
MERGED_OUTPUT_INDEX=${MERGED_OUTPUT[$INDEX]}
PHENO_INDEX=${PHENO[$INDEX]}
OUTPUT_INDEX=${OUTPUT[$INDEX]}

# command
python gene_score_regression_adsp.py \
--gene_score AD_KMI/common_var_gene_score/igap_adsp_gene_score/merged_outputs/${MERGED_OUTPUT_INDEX} \
--pheno AD_KMI/adsp_filt_phenos/ADSP.filt_pheno_covar.${PHENO_INDEX}.txt \
--pheno_id_col IID \
--output AD_KMI/common_var_gene_score/igap_adsp_gene_score/association_study/${OUTPUT_INDEX}