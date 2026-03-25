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

#BSUB -J "adsp_min_gene_pos[1-22]"
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

#BSUB -o logs/adsp_min_gene_pos.%J-%I.out
# Filename to append the job's stdout; change to -oo to overwrite.
# '%J' becomes the job ID number, '%I' becomes the array index.

#BSUB -e logs/adsp_min_gene_pos.%J-%I.err
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

VEP=(
    '113'
    '113'
    '113'
    '113'
    '113'
    '113'
    '113'
    '113'
    '113'
    '113'
    '113'
    '113'
    '113'
    '113'
    '113'
    '113'
    '113'
    '113'
    '113'
    '113'
    '113'
    '113'
)

FILENAME=(
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
        'ADSP.all_chr.genes.by_annotation.chr_bp_combined.txt'
)

GENE_COLNUM=(
        '6'
        '6'
        '6'
        '6'
        '6'
        '6'
        '6'
        '6'
        '6'
        '6'
        '6'
        '6'
        '6'
        '6'
        '6'
        '6'
        '6'
        '6'
        '6'
        '6'
        '6'
        '6'
)

CHR_COLNUM=(
        '7'
        '7'
        '7'
        '7'
        '7'
        '7'
        '7'
        '7'
        '7'
        '7'
        '7'
        '7'
        '7'
        '7'
        '7'
        '7'
        '7'
        '7'
        '7'
        '7'
        '7'
        '7'
)

POS_COLNUM=(
        '8'
        '8'
        '8'
        '8'
        '8'
        '8'
        '8'
        '8'
        '8'
        '8'
        '8'
        '8'
        '8'
        '8'
        '8'
        '8'
        '8'
        '8'
        '8'
        '8'
        '8'
        '8'
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
)

# Get the index of the current job
INDEX=$((LSB_JOBINDEX-1))

# Define parallelization variable indices
VEP_INDEX=${VEP[$INDEX]}
FILENAME_INDEX=${FILENAME[$INDEX]}
GENE_COLNUM_INDEX=${GENE_COLNUM[$INDEX]}
CHR_COLNUM_INDEX=${CHR_COLNUM[$INDEX]}
POS_COLNUM_INDEX=${POS_COLNUM[$INDEX]}
CHR_INDEX=${CHR[$INDEX]}

# create chromosome separated file
echo "processing chromosome ${CHR_INDEX}"
echo "making chromosome separated file"
temp_filepath="adsp_vep_min_gene_pos/v${VEP_INDEX}/temp_files/"
# grep 'chr'${LSB_JOBINDEX}':' /project/ritchie07/personal/katie/AD_gene_score/ukbb_vep/cleaned_vep_output/ukb_imp_v3_vep_annotations_cleaned_concat_chr_bp.txt > ukbb_vep_min_gene_pos/chr${CHR_INDEX}
grep 'chr'${CHR_INDEX}':' /project/ritchie/projects/ADSP_Projects/ADSP_Annotations/VEP_annotation_manual_${VEP_INDEX}/VEP_cleaned/${FILENAME_INDEX} > adsp_vep_min_gene_pos/v${VEP_INDEX}/temp_files/chr${CHR_INDEX}
awk 'NR>1 {print $0}'  adsp_vep_min_gene_pos/v${VEP_INDEX}/temp_files/chr${CHR_INDEX} | cut -f ${GENE_COLNUM_INDEX} | sort | uniq | wc -l

# make gene list
echo 'making gene list'
awk 'NR>1 {print $0}' adsp_vep_min_gene_pos/v${VEP_INDEX}/temp_files/chr${CHR_INDEX} | cut -f ${GENE_COLNUM_INDEX} | sort | uniq | tr '\n' ' ' > adsp_vep_min_gene_pos/v${VEP_INDEX}/temp_files/chr${CHR_INDEX}_temp
gene_list=$(cat adsp_vep_min_gene_pos/v${VEP_INDEX}/temp_files/chr${CHR_INDEX}_temp)

# create empty file
touch adsp_vep_min_gene_pos/v${VEP_INDEX}/temp_files/chr${CHR_INDEX}_min_gene_pos.txt

# for loop
echo "looping through genes"
for gene in $gene_list
do
  echo "processing $gene"
  grep $gene adsp_vep_min_gene_pos/v${VEP_INDEX}/temp_files/chr${CHR_INDEX} |  cut -f ${GENE_COLNUM_INDEX},${CHR_COLNUM_INDEX},${POS_COLNUM_INDEX} | sed 's/chr//g' | sort -k3 -n | head -n1 > adsp_vep_min_gene_pos/v${VEP_INDEX}/temp_files/chr${CHR_INDEX}_gene_temp
  cat adsp_vep_min_gene_pos/v${VEP_INDEX}/temp_files/chr${CHR_INDEX}_gene_temp >> adsp_vep_min_gene_pos/v${VEP_INDEX}/temp_files/chr${CHR_INDEX}_min_gene_pos.txt
done

wc -l adsp_vep_min_gene_pos/v${VEP_INDEX}/temp_files/chr${CHR_INDEX}_min_gene_pos.txt
head adsp_vep_min_gene_pos/v${VEP_INDEX}/temp_files/chr${CHR_INDEX}_min_gene_pos.txt