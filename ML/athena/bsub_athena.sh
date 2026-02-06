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

#BSUB -J "athena[1-8]"
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

#BSUB -o logs/athena.%J-%I.out
# Filename to append the job's stdout; change to -oo to overwrite.
# '%J' becomes the job ID number, '%I' becomes the array index.

#BSUB -e logs/athena.%J-%I.err
# Filename to append the job's stderr; change to -eo to overwrite.
# If omitted, stderr is combined with stdout.

#-#BSUB -B
# Send email notification when the job starts.

#-#BSUB -N
# Send email notification when the job finishes;
# otherwise, summary is written to the output file.

#BSUB -R "rusage[mem=50000]"
# Per-process memory reservation, in MB.
# (Ensures the job will have this minimum memory.)

#BSUB -M 50000
# Per-process memory limit, in MB.
# (Ensures the job will not exceed this maximum memory.)

#BSUB -v 50000
# Total process virtual (swap) memory limit, in MB.

#-#BSUB -W 24:00
# Wall time limit, in the format "hours:minutes".

#BSUB -n 20
# Number of cores to reserve (on one or more hosts; see below).
# The variable $LSB_HOSTS lists allocated hosts like "hostA hostA hostB";
# the variable $LSB_MCPU_HOSTS lists allocated hosts like "hostA 2 hostB 1".

#BSUB -R "span[hosts=1]"
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

# create parallelization variables
PATHWAY_SCORE=(
        'AOU_ALL.UKBB.metasoft.gene_score.ROSMAP.RNAseq.methylation.somoscan_proteomics.MSBB.RNAseq.methylation.tmt_proteomics.ADSP.gene_average.pathway_scores.standard_scaled.go.keep_quest_comb.80%_train.athena_input.txt'
        'AOU_ALL.UKBB.metasoft.gene_score.ROSMAP.RNAseq.methylation.somoscan_proteomics.MSBB.RNAseq.methylation.tmt_proteomics.ADSP.pathway_average.pathway_scores.standard_scaled.go.keep_quest_comb.80%_train.athena_input.txt'
        'AOU_ALL.UKBB.metasoft.gene_score.ROSMAP.RNAseq.methylation.somoscan_proteomics.MSBB.RNAseq.methylation.tmt_proteomics.ADSP.gene_average.pathway_scores.minmax_scaled.go.keep_quest_comb.80%_train.athena_input.txt'
        'AOU_ALL.UKBB.metasoft.gene_score.ROSMAP.RNAseq.methylation.somoscan_proteomics.MSBB.RNAseq.methylation.tmt_proteomics.ADSP.pathway_average.pathway_scores.minmax_scaled.go.keep_quest_comb.80%_train.athena_input.txt'
        'AOU_ALL.UKBB.metasoft.gene_score.ROSMAP.RNAseq.methylation.somoscan_proteomics.MSBB.RNAseq.methylation.tmt_proteomics.ADSP.gene_average.pathway_scores.standard_scaled.go.keep_quest_comb.80%_train.athena_input.txt'
        'AOU_ALL.UKBB.metasoft.gene_score.ROSMAP.RNAseq.methylation.somoscan_proteomics.MSBB.RNAseq.methylation.tmt_proteomics.ADSP.pathway_average.pathway_scores.standard_scaled.go.keep_quest_comb.80%_train.athena_input.txt'
        'AOU_ALL.UKBB.metasoft.gene_score.ROSMAP.RNAseq.methylation.somoscan_proteomics.MSBB.RNAseq.methylation.tmt_proteomics.ADSP.gene_average.pathway_scores.minmax_scaled.go.keep_quest_comb.80%_train.athena_input.txt'
        'AOU_ALL.UKBB.metasoft.gene_score.ROSMAP.RNAseq.methylation.somoscan_proteomics.MSBB.RNAseq.methylation.tmt_proteomics.ADSP.pathway_average.pathway_scores.minmax_scaled.go.keep_quest_comb.80%_train.athena_input.txt'
)
OUTPUT_PREFIX=(
        'ADSP.gene_average.pathway_scores.standard_scaled.80%_train.genn.athena'
        'ADSP.pathway_average.pathway_scores.standard_scaled.80%_train.genn.athena'
        'ADSP.gene_average.pathway_scores.minmax_scaled.80%_train.genn.athena'
        'ADSP.pathway_average.pathway_scores.minmax_scaled.80%_train.genn.athena'
        'ADSP.gene_average.pathway_scores.standard_scaled.80%_train.gesr.athena'
        'ADSP.pathway_average.pathway_scores.standard_scaled.80%_train.gesr.athena'
        'ADSP.gene_average.pathway_scores.minmax_scaled.80%_train.gesr.athena'
        'ADSP.pathway_average.pathway_scores.minmax_scaled.80%_train.gesr.athena'
)

GRAMMAR=(
        'genn.bnf'
        'genn.bnf'
        'genn.bnf'
        'genn.bnf'
        'gesr.bnf'
        'gesr.bnf'
        'gesr.bnf'
        'gesr.bnf'
)

# Get the index of the current job
INDEX=$((LSB_JOBINDEX-1))

# Define parallelization variable indices
PATHWAY_SCORE_INDEX=${PATHWAY_SCORE[$INDEX]}
OUTPUT_PREFIX_INDEX=${OUTPUT_PREFIX[$INDEX]}
GRAMMAR_INDEX=${GRAMMAR[$INDEX]}

# load modules
module purge
module load athena/2.0.0

which mpirun
mpirun --version
ldd

# call script
mpirun --mca mca_base_component_show_load_errors 0 -np 20 athena.py \
--missing NaN \
--scale-contin \
--gens 700 \
--pop-size 5000 \
--contin-file ML/athena/input/${PATHWAY_SCORE_INDEX} \
--outcome-file ML/athena/input/ADSP_phenotype.keep_quest_comb.80%_train.txt \
--grammar-file ML/athena/athena-python/example/${GRAMMAR_INDEX} \
--fitness balanced_acc \
--crossover2 block \
--gen-cross-switch 400 \
--min-init-tree-depth 11 \
--max-init-tree-depth 15 \
--max-depth 50 \
--out ML/athena/output/${OUTPUT_PREFIX_INDEX}
