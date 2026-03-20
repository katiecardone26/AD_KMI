# build singularity container
apptainer build prs.sif docker://katiecardone26/prscsx_apply_pgs:latest

# run nextflow
nextflow run main.nf -profile cluster -resume