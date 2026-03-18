#!/bin/bash

######################################################################
# RITCHIE LAB BATCH JOB TEMPLATE
#
# Make a copy of this file to edit for your job. To enable an option,
# remove the extra "#-" prefix (change "#-#BSUB ..." to "#BSUB ...").
# Submit the job by piping it into the "bsub" command, as in
#   cat myjob.bsub | bsub
# or
#   bsub < myjob.bsub
######################################################################

#BSUB -J "rf[1-8]"
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
# of the current sub-job.

#BSUB -o logs/rf.%J-%I.out
# Filename to append the job's stdout; change to -oo to overwrite.
# '%J' becomes the job ID number, '%I' becomes the array index.

#BSUB -e logs/rf.%J-%I.err
# Filename to append the job's stderr; change to -eo to overwrite.
# If omitted, stderr is combined with stdout.

#-#BSUB -B
# Send email notification when the job starts.

#-#BSUB -N
# Send email notification when the job finishes;
# otherwise, summary is written to the output file.

#BSUB -R "rusage[mem=26000]"
# Per-process memory reservation, in MB.
# (Ensures the job will have this minimum memory.)

#BSUB -M 26000
# Per-process memory limit, in MB.
# (Ensures the job will not exceed this maximum memory.)

#BSUB -v 26000
# Total process virtual (swap) memory limit, in MB.

#-#BSUB -W 24:00
# Wall time limit, in the format "hours:minutes".

#BSUB -n 4
# Number of cores to reserve (on one or more hosts; see below).
# The variable $LSB_HOSTS lists allocated hosts like "hostA hostA hostB";
# the variable $LSB_MCPU_HOSTS lists allocated hosts like "hostA 2 hostB 1".

#-#BSUB -R "span[hosts=1]"
# Require all cores to be on the same host (for multi-threaded, non-MPI).

#-#BSUB -R "span[ptile=1]"
# Maximum number of cores to reserve on each host (for MPI).

#BSUB -R "select[ostype>=CENT7]"
# Require that the job runs on CentOS 7 host(s).

######################################################################
# RITCHIE LAB BATCH ENVIRONMENT CONFIG
#
# This ensures the job runs with the expected lab environment, even
# if it's submitted from a non-fully-supported host (i.e. CentOS6).
######################################################################

if test "${HOME}/ritchielab.bashrc" -nt "${HOME}/group/ritchielab.bashrc" ; then
        . "${HOME}/ritchielab.bashrc"
elif test -f "${HOME}/group/ritchielab.bashrc" ; then
        . "${HOME}/group/ritchielab.bashrc"
else
        echo "WARNING: Could not find Ritchie Lab bashrc group environment script."
fi

######################################################################
# JOB COMMANDS
#
# Put your commands below. The script will run in the directory you
# submit it from, not (necessarily) the directory the script is in.
######################################################################

# define parallelization variables
INPUT_PREFIX=(
        'ADSP.genomics.gene_average.pathway_scores.pathway_intersection.multiomics_pathway_average_weighted.standard_scaled.go.keep_quest_comb.covariates'
        'ADSP.genomics.gene_average.pathway_scores.pathway_intersection.multiomics_pathway_average_weighted.pval_0.05.standard_scaled.go.keep_quest_comb.covariates'
        'ADSP.genomics.gene_average.pathway_scores.pathway_intersection.multiomics_pathway_average_weighted.pval_0.01.standard_scaled.go.keep_quest_comb.covariates'
        'ADSP.genomics.gene_average.pathway_scores.pathway_intersection.multiomics_pathway_average_weighted.pval_0.001.standard_scaled.go.keep_quest_comb.covariates'
        'ADSP.genomics.gene_average.pathway_scores.pathway_intersection.multiomics_pathway_average_weighted.pval_0.0001.standard_scaled.go.keep_quest_comb.covariates'
        'ADSP.genomics.gene_average.pathway_scores.pathway_intersection.multiomics_pathway_average_weighted.pval_0.00001.standard_scaled.go.keep_quest_comb.covariates'
        'ADSP.genomics.gene_average.pathway_scores.pathway_intersection.multiomics_pathway_average_weighted.pval_0.000001.standard_scaled.go.keep_quest_comb.covariates'
        'ADSP.genomics.gene_average.pathway_scores.pathway_intersection.multiomics_pathway_average_weighted.pval_0.0000001.standard_scaled.go.keep_quest_comb.covariates'
)

OUTPUT_TAG=(
        'pval_none'
        'pval_0.05'
        'pval_0.01'
        'pval_0.001'
        'pval_0.0001'
        'pval_0.00001'
        'pval_0.000001'
        'pval_0.0000001'
)

# Get the index of the current job
INDEX=$((LSB_JOBINDEX-1))

# Define parallelization variable indices
INPUT_PREFIX_INDEX=${INPUT_PREFIX[$INDEX]}
OUTPUT_TAG_INDEX=${OUTPUT_TAG[$INDEX]}

# load modules
module purge
module load python

# call script
python run_rf_hyperparameter_tuning.py \
        --input_prefix ${INPUT_PREFIX_INDEX} \
        --key_name avg_gene \
        --output_tag multiomics_pathway_average_weighted.${OUTPUT_TAG_INDEX}.standard_scaled.go.keep_quest_comb
