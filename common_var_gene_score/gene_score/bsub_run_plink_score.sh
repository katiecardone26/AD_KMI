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

#BSUB -J "run_plink_score[1-88]"
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

#BSUB -o logs/run_plink_score.%J-%I.out
# Filename to append the job's stdout; change to -oo to overwrite.
# '%J' becomes the job ID number, '%I' becomes the array index.

#BSUB -e logs/run_plink_score.%J-%I.err
# Filename to append the job's stderr; change to -eo to overwrite.
# If omitted, stderr is combined with stdout.

#-#BSUB -B
# Send email notification when the job starts.

#-#BSUB -N
# Send email notification when the job finishes;
# otherwise, summary is written to the output file.

#-#BSUB -R "rusage[mem=2000]"
# Per-process memory reservation, in MB.
# (Ensures the job will have this minimum memory.)

#-#BSUB -M 50000
# Per-process memory limit, in MB.
# (Ensures the job will not exceed this maximum memory.)

#-#BSUB -v 128
# Total process virtual (swap) memory limit, in MB.

#-#BSUB -W 24:00
# Wall time limit, in the format "hours:minutes".

#-#BSUB -n 1
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

SCORE_INPUT_PREFIX=(
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
        'plink_score_input/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_input.chr'
)

OUTPUT_PREFIX=(
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_ALL.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.FE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
        'plink_score_output/AOU_EUR.UKBB.metasoft.VEP_v113.gene_by_position.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.plink_score_output.chr'
)

CHR=(
        1
        2
        3
        4
        5
        6
        7
        8
        9
        10
        11
        12
        13
        14
        15
        16
        17
        18
        19
        20
        21
        22
        1
        2
        3
        4
        5
        6
        7
        8
        9
        10
        11
        12
        13
        14
        15
        16
        17
        18
        19
        20
        21
        22
        1
        2
        3
        4
        5
        6
        7
        8
        9
        10
        11
        12
        13
        14
        15
        16
        17
        18
        19
        20
        21
        22
        1
        2
        3
        4
        5
        6
        7
        8
        9
        10
        11
        12
        13
        14
        15
        16
        17
        18
        19
        20
        21
        22
)
# Get the index of the current job
INDEX=$((LSB_JOBINDEX-1))

# get variable indices
SCORE_INPUT_PREFIX_INDEX=${SCORE_INPUT_PREFIX[$INDEX]}
CHR_INDEX=${CHR[$INDEX]}
OUTPUT_PREFIX_INDEX=${OUTPUT_PREFIX[$INDEX]}

# load modules
module load plink/2.0-20240804 

# get score column names
filename=${SCORE_INPUT_PREFIX_INDEX}
filename+=${CHR_INDEX}
filename+='.txt'
echo $filename
temp=$(awk '{{print NF}}' $filename | sort -nu | tail -n 1)
colnums=$(seq 3 $temp)
echo $colnums

# plink command      
plink2 --score ${SCORE_INPUT_PREFIX_INDEX}${CHR_INDEX}.txt header-read cols=+scoresums,-scoreavgs list-variants \
--score-col-nums $colnums \
--pfile ADSP_plink_subset/new_var_id/ADSP.mac20.noduplicates.geno0.01.mind0.05.maf0.01.new_var_id.chr${CHR_INDEX} \
--out ${OUTPUT_PREFIX_INDEX}${CHR_INDEX}
