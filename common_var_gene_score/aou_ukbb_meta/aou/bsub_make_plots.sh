#!/bin/bash

# BSUB parameters
######################################################################

#BSUB -J make_plots[1-4]
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

#BSUB -o logs/make_plots.%J.%I.out 
# Filename to append the job's stdout; change to -oo to overwrite.
#'%J' becomes the job ID number, '%I' becomes the array index.

#BSUB -e logs/make_plots.%J.%I.err 
# Filename to append the job's stderr; change to -eo to overwrite. 
# If omitted, stderr is combined with stdout. 
# '%J' becomes the job ID number, '%I' becomes the array index.

#BSUB -R "span[hosts=1]"
# Require all cores to be on the same host (for multi-threaded, non-MPI).

#-#BSUB -B
# Send email notification when the job starts

#-#BSUB -N
# Send email notification when the job finishes; otherwise, summary is written to the output file

#BSUB -R "rusage[mem=8000]"
# Per-process memory reservation, in MB.
# (Ensures the job will have this minimum memory.)

#BSUB -M 8000
# Per-process memory limit, in MB.
# (Ensures the job will not exceed this maximum memory.)

#-#BSUB -v 200000
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
## ancestry
ANCESTRY=(
    "EUR"
    "ALL"
    "EUR"
    "ALL"
)

SIG=(
   "1.4e-08" 
   "1.3e-08"
   "1.4e-08" 
   "1.3e-08"
)

SUG=(
    "2.7e-07"
    "2.6e-07"
    "2.7e-07"
    "2.6e-07"
)

INVERT=(
    "True"
    "True"
    "False"
    "False"
)

# Get the index of the current job
INDEX=$((LSB_JOBINDEX-1))

# Define parallelization variable indices
## ancestry
ANCESTRY_INDEX=${ANCESTRY[$INDEX]}
## significance threshold
SIG_INDEX=${SIG[$INDEX]}
## suggestive threshold
SUG_INDEX=${SUG[$INDEX]}
## invert
INVERT_INDEX=${INVERT[$INDEX]}

# activate conda env
module purge
eval "$(conda shell.bash hook)"
conda activate ~/mambaforge/envs/manhattan_plot

# call plotting script
python manhattan_plotting_script.py \
--annot_input vep_output/AOU.AD.${ANCESTRY_INDEX}.vep_output.cleaned.txt \
--sumstats_input sumstats/AOU.AD.${ANCESTRY_INDEX}.all_chr.saige_step2.for_export.txt \
--title AOU_v8.AD.${ANCESTRY_INDEX} \
--sumstats_pval_col p.value \
--sumstats_chr_col CHR \
--sumstats_pos_col POS \
--sumstats_id_col MarkerID \
--annot_id_col GENE \
--annot_chr_col CHR \
--annot_pos_col POS \
--known_genes advp/AD_known_gene_list.txt \
--sig ${SIG_INDEX} \
--sug ${SUG_INDEX} \
--annot ${SUG_INDEX} \
--plot_sig False \
--invert ${INVERT_INDEX} \
--output_prefix plots/AOU_v8.AD.${ANCESTRY_INDEX}.invert=${INVERT_INDEX}