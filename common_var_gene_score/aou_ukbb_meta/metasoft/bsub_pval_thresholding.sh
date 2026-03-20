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

#BSUB -J "pval_thresholding[1]"
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

#BSUB -o logs/pval_thresholding.%J-%I.out
# Filename to append the job's stdout; change to -oo to overwrite.
# '%J' becomes the job ID number, '%I' becomes the array index.

#BSUB -e logs/pval_thresholding.%J-%I.err
# Filename to append the job's stderr; change to -eo to overwrite.
# If omitted, stderr is combined with stdout.

#-#BSUB -B
# Send email notification when the job starts.

#-#BSUB -N
# Send email notification when the job finishes;
# otherwise, summary is written to the output file.

#BSUB -R "rusage[mem=100000]"
# Per-process memory reservation, in MB.
# (Ensures the job will have this minimum memory.)

#BSUB -M 100000
# Per-process memory limit, in MB.
# (Ensures the job will not exceed this maximum memory.)

#BSUB -v 100000
# Total process virtual (swap) memory limit, in MB.

#BSUB -W 24:00
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
## sumstats prefix
SUMSTATS=(
        "AD.AOU_ALL.UKBB.no_adjustment.metasoft_output.extra_cols.adsp_intersect.cleaned.RE_PVAL.r2_0.1_clump_variants_excluded.txt"
)
## pval column number
PVAL_COL_NUM=(
        "6"
)
## output filename
OUTPUT=(
        "AD.AOU_ALL.UKBB.no_adjustment.metasoft_output.adsp_intersect.r2_0.1_clump_variants_excluded.RE_pval_threshold_0.05.txt"
)

# Get the index of the current job
INDEX=$((LSB_JOBINDEX-1))

# get variable indices
SUMSTATS_INDEX=${SUMSTATS[$INDEX]}
PVAL_COL_NUM_INDEX=${PVAL_COL_NUM[$INDEX]}
OUTPUT_INDEX=${OUTPUT[$INDEX]}

# pval filtering
awk -v col=${PVAL_COL_NUM_INDEX} '{if ($col ~ "e-" || $col < 0.05) {print $0}}' ${SUMSTATS_INDEX} | awk 'BEGIN {print "original_variant_id #STUDY PVALUE_FE BETA_FE STD_FE PVALUE_RE BETA_RE STD_RE PVALUE_RE2 STAT1_RE2 STAT2_RE2 PVALUE_BE I_SQUARE QPVALUE_Q TAU_SQUARE CHR POS REF ALT ADSP_variant_id"} {print $0}' | sed 's/\t/,/g' | sed 's/ /,/g' | sed 's/,/\t/g' > ${OUTPUT_INDEX}

