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

#BSUB -J "vep_113[1-22]"
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

#BSUB -o logs/vep_113.%J-%I.out
# Filename to append the job's stdout; change to -oo to overwrite.
# '%J' becomes the job ID number, '%I' becomes the array index.

#BSUB -e logs/vep_113.%J-%I.err
# Filename to append the job's stderr; change to -eo to overwrite.
# If omitted, stderr is combined with stdout.

#-#BSUB -B
# Send email notification when the job starts.

#-#BSUB -N
# Send email notification when the job finishes;
# otherwise, summary is written to the output file.

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

#-#BSUB -n 4
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

module load singularity

singularity exec --bind ./VEP_cache:/VEP_cache/,./input:/input/,./raw_output:/raw_output/ vep.sif \
    vep --dir /VEP_cache/ --cache --offline --format vcf \
        --force_overwrite \
        -i /input/gcad.qc.compact_filtered.r4.wgs.36361.GATK.2023.06.06.biallelic.genotypes.chr"$LSB_JOBINDEX".ALL.vcf.bgz \
        -o /raw_output/ADSPraw_chr"$LSB_JOBINDEX".txt \
        --symbol \
        --tab \
        --buffer_size 10000 \
        --cache_version 113
