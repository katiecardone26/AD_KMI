# Alzheimer's Disease Knowledge-Based Multiomics Integration Project

## Project Overview
- This project uses RNAseq, methylomics, and proteomics data to weight genetic pathway scores to predict AD Case/Control status in ADSP
- This AD GWAS was meta analyzed with an AOU AD GWAS and used to weight gene scores, which aggregated SNP data in ADSP at the gene level

## Analysis Rundown
1. Run AOU and UKBB GWAS (on cloud platforms)
2. Make AOU and UKBB GWAS manhattan plots
    - directories:
        - `common_var_gene_score/aou_ukbb_meta/aou/`
        - `common_var_gene_score/aou_ukbb_meta/ukbb/`
    - scripts:
        1. `bsub_make_vcf.sh` / `make_vcf.py`
        2. `bsub_annotate_vcf.sh`
        3. `bsub_clean_vep.sh` / `clean_vep.py`
        4. `bsub_make_plots.sh` / `manhattan_plotting_script.py`
3. Run meta-analysis between AOU and UKBB GWAS, make manhattan plots, and get intersect with ADSP
    - directory: `common_var_gene_score/aou_ukbb_meta/metasoft/`
    - scripts:
        1. `bsub_make_metasoft_input.sh` / `make_metasoft_input_no_adjustment.py`
        2. `bsub_run_metasoft.sh`
        3. `bsub_clean_metasoft_output.sh`
        4. `bsub_make_vcf.sh` / `make_vcf.py`
        5. `bsub_annotate_vcf.sh`
        6. `bsub_clean_vep.sh` / `clean_vep.py`
        7. `bsub_make_plots.sh` / `manhattan_plotting_script.py`
        8. `bsub_find_adsp_intersect.sh` / `find_adsp_intersect.py`
4. Run PLINK clump to remove SNPs in LD
    - directory: `common_var_gene_score/gene_score/`
    - scripts:
        1. `bsub_make_plink_clump_input.sh`
        2. `bsub_run_plink_clump.sh`
        3. `bsub_clean_clump_outputs.sh` / `clean_clump_outputs.py`
        4. `bsub_cat_clump_outputs.sh`
        5. `bsub_exclude_clump_snps.sh` / `exclude_clump_snps.py`
6. Filter sumstats by p-value threshold
    - directory: `common_var_gene_score/aou_ukbb_meta/metasoft/`
    - scripts:
        1. `bsub_pval_thresholding.sh`
7. Run VEP on ADSP
    - directory: `vep/`
    - scripts:
        1. `bsub_annotate_vcf.sh` / `bsub_annotate_vcf_failed_chr.sh`
        2. `clean_vep_output.sh`
8. Reformat variant ID in ADSP plink files
    - directory: `/project/ritchie/projects/AD_KMI/common_var_gene_score/adsp/plink_subset/`
    - scripts:
        1. `bsub_new_var_id.sh`
9. Make gene scores, run regressions, and make synthesis view plot inputs
    - directory: `common_var_gene_score/gene_score/`
    - scripts:
        1. `bsub_beta_gene.sh` / `beta_gene.py`
        2. `bsub_plink_score_input.sh` / `plink_score_input.py`
        3. `bsub_run_plink_score.sh`
        4. `bsub_clean_score_output.sh` / `clean_score_output.py`
        5. `bsub_merge_score_outputs.sh` / `merge_score_outputs.py`
        6. `bsub_adsp_gene_score_regression.sh` / `gene_score_regression_adsp.py`
        7. `bsub_make_syn_view_inputs.sh` / `make_syn_view_inputs.py`
10. Clean omics data
    - directory: `omics_data/`
    - scripts:
        1. `MSBB_omics_preprocessing.ipynb`
        2. `ROSMAP_Proteomics_Preprocessing.ipynb`
        3. `ROSMAP_Methylation_Preprocessing.ipynb`
        4. `ROSMAP_RNAseq_Preprocessing.ipynb`
11. Map to common ID form
    - directory: `id_map/`
    - scripts:
        1. `MSBB_ID_Mapping.ipynb`
        2. `ROSMAP_ID_Mapping.ipynb`
        3. `ADSP_Common_ID_Map.ipynb`
12. Scale data
    - directory: `pathway_score/`
    - scripts:
        1. `AD_scale_data.ipynb`
13. Map genes to pathways
    - directory: `pathway_score/
    - scripts:
        1. `bsub_go_jaccard_similarity.sh` / `go_jaccard_simularity.py`
        2. `AD_GO.ipynb`
14. Make pathway scores
    - directory: `pathway_score/`
    - scripts:
        1. `bsub_pathway_score.sh` / `avg_pathway_score_no_pval_thres_separate_omics.py`
15. Run regressions with omics pathway scores and AD
    - directory: `ML/statistical_models/`
    - scripts:
        1. `bsub_lr_multiomics.sh` / `run_lr_multiomics.py`      
16. Weight genomics pathway scores and make stats models inputs
    - directory: `ML/statistical_models/`
    - scripts:
        1. `AD_Stats_Models_Input.ipynb`
17. Weight genomics pathway scores and make biological athena inputs
    - directory: `ML/athena/`
    - scripts:
        1. `AD_Athena_Inputs.ipynb`
18. Make simulated datasets
    - directory: `ML/athena/`
    - scripts:
        1. `AD_ML_simulations.ipynb`
19. Run statistical models
    - directory: `ML/statistical_models/`
    - scripts:
        1. `bsub_rf.sh` / `run_rf_hyperparameter_tuning.py`
        2. `bsub_xgboost.sh` / `run_xgboost_hyperparameter_tuning.py`
        3. `bsub_lr_ridge.sh` / `run_lr_hyperparameter_tuning.py`
20. Run athena (simulated and biological)
    - directory: `ML/athena/`
    - scripts:
        1. `bsub_athena.sh`
        2. `bsub_athena_simulations.sh` / `bsub_athena_simulations_failed.sh`
21. Process athena outputs (simulated and biological)
    - directory: `ML/athena/`
    - scripts:
        1. `AD_Athena_Outputs_updated.ipynb`
22. Calculate SHAP values
    - directory: `ML/statistical_models/`
    - scripts:
        1. `AD_shap_values.ipynb`
