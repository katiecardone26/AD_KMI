# copy phecode X file to association studies project (in ttyd terminal)
dx mkdir project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/input/
dx cp project-GfYFGzQJ745y0bqkF0PGF53v:/output/file-GxPVBxQJ745y2F5vx3gyzZb7 project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/input/

# extract demographic data using cohort builder
# 1. open app32133_20240306021926.dataset, which will open cohort builder
# 2. navigate to data preview -> add column -> population characteristics -> baseline characterisitcs
# 3. select month of birth (p52), year of birth (p34) & sex (p31)
# 4. hit dashboard actions -> save dashboard view
# 4. exit cohort builder
# 5. navigate to tools -> tools library
# 6. open table exporter
# 7. navigate to output file location, select dashboard view that was exported & customize output prefix

# create GWAS sample list
# 1. navigate to tools -> Jupyter lab
# 2. hit new jupyterlab
# 3. select ukbb project
# 4. phenotyping is the the jupyter notebook named "AD_GWAS_Phenotyping.ipynb"

# initial QC
# 1. navigate to tools -> tools library
# 2. open ttyd (terminal)
# 3. hit run (high priority)
# 4. run the following code in the terminal
bgen_input_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/Bulk/Imputation/Imputation_from_genotype_TOPmed"
sample_input_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/input"
output_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/initial_qc"

for chr in $(seq 1 22)
do
dx run app-swiss-army-knife \
-y \
-iin="${bgen_input_dir}/ukb21007_c${chr}_b0_v1.bgen.bgi" \
-iin="${bgen_input_dir}/ukb21007_c${chr}_b0_v1.bgen" \
-iin="${bgen_input_dir}/ukb21007_c${chr}_b0_v1.sample" \
-iin="${sample_input_dir}/UKBB.AD.ALL.sample_list.txt" \
--brief \
--name "inital_qc.imputed.chr${chr}" \
-icmd="plink2 --bgen ukb21007_c${chr}_b0_v1.bgen ref-first  --sample ukb21007_c${chr}_b0_v1.sample --keep-fam UKBB.AD.ALL.sample_list.txt --geno 0.05 dosage --mind 0.05 dosage --max-alleles 2 --snps-only --make-pgen --out ukb21007_c${chr}_b0_v1.topmed_imputed.initial_qc" \
--destination ${output_dir} \
--instance-type mem1_ssd2_v2_x8
done

# freq QC- make pgen files for ld pruning (for PCA and saige step 1) and snplist for saige step 2 QC
# 1. run the following code from ttyd terminal
inital_qc_input_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/initial_qc"
output_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/freq_qc"

for chr in $(seq 1 22)
do
dx run app-swiss-army-knife \
-y \
-iin="${inital_qc_input_dir}/ukb21007_c${chr}_b0_v1.topmed_imputed.initial_qc.pgen" \
-iin="${inital_qc_input_dir}/ukb21007_c${chr}_b0_v1.topmed_imputed.initial_qc.psam" \
-iin="${inital_qc_input_dir}/ukb21007_c${chr}_b0_v1.topmed_imputed.initial_qc.pvar" \
--brief \
--name "freq_qc.imputed.chr${chr}" \
-icmd="plink2 --pfile ukb21007_c${chr}_b0_v1.topmed_imputed.initial_qc --maf 0.05 --set-all-var-ids chr@:#:\\\$r:\\\$a --write-snplist --make-pgen --out ukb21007_c${chr}_b0_v1.topmed_imputed.freq_qc" \
--destination ${output_dir} \
--instance-type mem1_ssd2_v2_x4
done

# check number of variants
# 1. run the following code from ttyd terminal
dx download project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/freq_qc/ukb21007_c*_b0_v1.topmed_imputed.freq_qc.pvar

for i in $(seq 1 22)
do
wc -l "ukb21007_c"$i"_b0_v1.topmed_imputed.freq_qc.pvar"
done

# LD prune
# 1. run the following code from ttyd terminal
freq_qc_input_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/freq_qc"
output_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/ld_pruned"

for chr in $(seq 1 22)
do
dx run app-swiss-army-knife \
-y \
-iin="${freq_qc_input_dir}/ukb21007_c${chr}_b0_v1.topmed_imputed.freq_qc.pgen" \
-iin="${freq_qc_input_dir}/ukb21007_c${chr}_b0_v1.topmed_imputed.freq_qc.psam" \
-iin="${freq_qc_input_dir}/ukb21007_c${chr}_b0_v1.topmed_imputed.freq_qc.pvar" \
--brief \
--name "ld_prune.imputed.chr${chr}" \
-icmd="plink2 --pfile ukb21007_c${chr}_b0_v1.topmed_imputed.freq_qc --indep-pairwise 150 5 0.1 --out ukb21007_c${chr}_b0_v1.topmed_imputed.ld_pruned" \
--destination ${output_dir} \
--instance-type mem1_ssd2_v2_x4
done
# 2. check number of variants
dx download project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/ld_pruned/ukb21007_c*_b0_v1.topmed_imputed.ld_pruned.prune.in --overwrite

rm ld_pruned.total_linecount
touch ld_pruned.total_linecount
for i in $(seq 1 22)
do
wc -l "ukb21007_c"$i"_b0_v1.topmed_imputed.ld_pruned.prune.in" >> ld_pruned.total_linecount
done

awk '{sum += $1} END {print sum}' ld_pruned.total_linecount >> ld_pruned.total_linecount
cat ld_pruned.total_linecount
dx upload ld_pruned.total_linecount --destination /AD_GWAS/output/ld_pruned/
# 3. extract LD pruned variants
freq_qc_input_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/freq_qc"
output_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/ld_pruned"

for chr in $(seq 1 22)
do
dx run app-swiss-army-knife \
-y \
-iin="${freq_qc_input_dir}/ukb21007_c${chr}_b0_v1.topmed_imputed.freq_qc.pgen" \
-iin="${freq_qc_input_dir}/ukb21007_c${chr}_b0_v1.topmed_imputed.freq_qc.psam" \
-iin="${freq_qc_input_dir}/ukb21007_c${chr}_b0_v1.topmed_imputed.freq_qc.pvar" \
-iin="${output_dir}/ukb21007_c${chr}_b0_v1.topmed_imputed.ld_pruned.prune.in" \
--brief \
--name "ld_prune_extract.imputed.chr${chr}" \
-icmd="plink2 --pfile ukb21007_c${chr}_b0_v1.topmed_imputed.freq_qc --extract ukb21007_c${chr}_b0_v1.topmed_imputed.ld_pruned.prune.in --make-pgen --out ukb21007_c${chr}_b0_v1.topmed_imputed.ld_pruned" \
--destination ${output_dir} \
--instance-type mem1_ssd2_v2_x4
done
# 4. check number of variants
dx download project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/ld_pruned/ukb21007_c*_b0_v1.topmed_imputed.ld_pruned.pvar

touch ld_pruned_extract.total_linecount
for i in $(seq 1 22)
do
wc -l "ukb21007_c"$i"_b0_v1.topmed_imputed.ld_pruned.pvar" >> ld_pruned_extract.total_linecount
done

awk '{sum += $1} END {print sum}' ld_pruned_extract.total_linecount >> ld_pruned_extract.total_linecount
cat ld_pruned_extract.total_linecount
dx upload ld_pruned_extract.total_linecount --destination /AD_GWAS/output/ld_pruned/

# merge LD pruned files
# 1. make merge list
touch merge_list.txt
for chr in $(seq 1 22)
do
echo "ukb21007_c"$chr"_b0_v1.topmed_imputed.ld_pruned" >> merge_list.txt
done

cat merge_list.txt 
dx upload merge_list.txt --destination /AD_GWAS/output/ld_pruned/

# 2. run the following code from ttyd terminal
ld_pruned_input_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/ld_pruned"
output_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/ld_pruned"

dx run app-swiss-army-knife \
-y \
$(dx find data --path "${ld_pruned_input_dir}" --name "ukb21007_c*_b0_v1.topmed_imputed.ld_pruned.*" --created-after="2025-02-19 14:50:00" --brief | awk '{print "-iin="$1}') \
-iin="${ld_pruned_input_dir}/merge_list.txt" \
--brief \
--name "merge_ld_prune.imputed" \
-icmd="plink2 --pmerge-list merge_list.txt --make-bed --out ukb21007_all_chr_b0_v1.topmed_imputed.ld_pruned" \
--destination ${output_dir} \
--instance-type mem1_ssd2_v2_x4
# 3. check number of variants
dx download project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/ld_pruned/ukb21007_all_chr_b0_v1.topmed_imputed.ld_pruned.bim
wc -l ukb21007_all_chr_b0_v1.topmed_imputed.ld_pruned.bim

# build eigenstrat applet (version on UKB doesn't have all the needed flags)
# 1. use app wizard
dx-app-wizard
# 2. add following options into app-wizard
App Name: eigenstrat_kmc
Title []: Eigenstrat Applet created by Katie Cardone
Summary []: Runs any eigenstrat command
Version [0.0.1]: 1.0.0
1st input name (<ENTER> to finish): input
Label (optional human-readable name) []: 
Choose a class (<TAB> twice for choices): array:file
This is an optional parameter [y/n]: n
2nd input name (<ENTER> to finish): command
Label (optional human-readable name) []: 
Choose a class (<TAB> twice for choices): string
This is an optional parameter [y/n]: n
3rd input name (<ENTER> to finish):
1st output name (<ENTER> to finish):
Timeout policy [48h]: 7d
Programming language: bash
Will this app need access to the Internet? [y/N]: y
Will this app need access to the parent project? [y/N]: y
Choose an instance type for your app [mem1_ssd1_v2_x4]: mem1_ssd1_v2_x4
# 3. made additional edits to applet scripts in terminal (see uploaded scripts)
## use vim
# 4. build applet
dx build eigenstrat_kmc --overwrite
# 5. upload applet scripts
dx upload -r eigenstrat_kmc/ --path project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/scripts/eigenstrat_kmc/

# make convertf par file
genotypename="input/ukb21007_all_chr_b0_v1.topmed_imputed.ld_pruned.bed"
snpname="input/ukb21007_all_chr_b0_v1.topmed_imputed.ld_pruned.bim"
indivname="input/ukb21007_all_chr_b0_v1.topmed_imputed.ld_pruned.fam"
outputformat="EIGENSTRAT"
genotypeoutname="output/ukb21007_all_chr_b0_v1.topmed_imputed.AD.PCA_input.eigenstratgeno"
snpoutname="output/ukb21007_all_chr_b0_v1.topmed_imputed.AD.PCA_input.snp"
indivoutname="output/ukb21007_all_chr_b0_v1.topmed_imputed.AD.PCA_input.ind"

echo "genotypename:    $genotypename" > convertf.par
echo "snpname:         $snpname" >> convertf.par
echo "indivname:       $indivname" >> convertf.par
echo "outputformat:    $outputformat" >> convertf.par
echo "genotypeoutname: $genotypeoutname" >> convertf.par
echo "snpoutname:      $snpoutname" >> convertf.par
echo "indivoutname:    $indivoutname" >> convertf.par

# make smartPCA inputs
ld_pruned_input_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/ld_pruned"
output_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/pca/"

dx run eigenstrat_kmc \
-y \
-iinput="${ld_pruned_input_dir}/ukb21007_all_chr_b0_v1.topmed_imputed.ld_pruned.bed" \
-iinput="${ld_pruned_input_dir}/ukb21007_all_chr_b0_v1.topmed_imputed.ld_pruned.bim" \
-iinput="${ld_pruned_input_dir}/ukb21007_all_chr_b0_v1.topmed_imputed.ld_pruned.fam" \
-iinput="${ld_pruned_input_dir}/convertf.par" \
-icommand="convertf -p input/convertf.par" \
--brief \
--name "convertf.imputed" \
--destination="${output_dir}" \
--instance-type mem1_ssd2_v2_x8

# make smartPCA par file
genotypename="input/ukb21007_all_chr_b0_v1.topmed_imputed.AD.PCA_input.eigenstratgeno"
snpname="input/ukb21007_all_chr_b0_v1.topmed_imputed.AD.PCA_input.snp"
indivname="input/ukb21007_all_chr_b0_v1.topmed_imputed.AD.PCA_input.ind"
evecoutname="output/ukb21007_all_chr_b0_v1.topmed_imputed.AD.PCA.eigenvec"
evaloutname="output/ukb21007_all_chr_b0_v1.topmed_imputed.AD.PCA.eigenval"
numoutevec="20"
numoutlieriter="0"
altnormstyle="NO"
fastmode="NO"
numthreads="16"

echo "genotypename:    $genotypename" > smartPCA.par
echo "snpname:         $snpname" >> smartPCA.par
echo "indivname:       $indivname" >> smartPCA.par
echo "evecoutname:     $evecoutname" >> smartPCA.par
echo "evaloutname:     $evaloutname" >> smartPCA.par
echo "numoutevec:      $numoutevec" >> smartPCA.par
echo "numoutlieriter:  $numoutlieriter" >> smartPCA.par
echo "altnormstyle:    $altnormstyle" >> smartPCA.par
echo "fastmode:        $fastmode" >> smartPCA.par
echo "numthreads:      $numthreads" >> smartPCA.par

# run smart PCA
pca_input_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/pca/"
output_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/pca/"

dx run eigenstrat_kmc \
-y \
-iinput="${pca_input_dir}/ukb21007_all_chr_b0_v1.topmed_imputed.AD.PCA_input.eigenstratgeno" \
-iinput="${pca_input_dir}/ukb21007_all_chr_b0_v1.topmed_imputed.AD.PCA_input.snp" \
-iinput="${pca_input_dir}/ukb21007_all_chr_b0_v1.topmed_imputed.AD.PCA_input.ind" \
-iinput="${pca_input_dir}/smartPCA.par" \
-icommand="smartpca -p input/smartPCA.par" \
--brief \
--name "smartpca.imputed" \
--destination ${output_dir} \
--instance-type mem1_ssd1_v2_x16

# clean PCA output
# 1. run the following commands in ttyd terminal
# 2. download raw eigenvec/eigenval file
dx download project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/pca/ukb21007_all_chr_b0_v1.topmed_imputed.AD.PCA.eigenvec
# 3. clean eigenvec
awk 'NR>1' ukb21007_all_chr_b0_v1.topmed_imputed.AD.PCA.eigenvec | sed 's/^.*://g' | sed 's/ /,/g' | sed 's/,\+/,/g' | sed 's/,???//g' | sed 's/,/\t/g' > ukb21007_all_chr_b0_v1.topmed_imputed.AD.PCA_cleaned.eigenvec
# 4. clean eigenval
head -n1 ukb21007_all_chr_b0_v1.topmed_imputed.AD.PCA.eigenvec | sed 's/^.*://' | sed 's/^[ \t]*//' | sed 's/ /,/g' | sed 's/,\+/,/g' | sed 's/,$//' | tr ',' '\n' > ukb21007_all_chr_b0_v1.topmed_imputed.AD.PCA_cleaned.eigenval
# 5. upload files
dx upload ukb21007_all_chr_b0_v1.topmed_imputed.AD.PCA_cleaned.* --path project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/pca/

# add PCs to phenotype covariate file
# 1. commands in jupyter lab notebook

# build SAIGE applet (version on UKB is outdated grrrr)
# 1. use app wizard
dx-app-wizard
# 2. add following options into app-wizard
App Name: saige_v1.4.2
Title []: saige_v1.4.2
Summary []: Runs any saige command with version 1.4.2, made by Katie Cardone
Version [0.0.1]: 1.4.2
1st input name (<ENTER> to finish): input
Label (optional human-readable name) []: 
Choose a class (<TAB> twice for choices): array:file
This is an optional parameter [y/n]: n
2nd input name (<ENTER> to finish): command
Label (optional human-readable name) []: 
Choose a class (<TAB> twice for choices): string
This is an optional parameter [y/n]: n
3rd input name (<ENTER> to finish):
1st output name (<ENTER> to finish):
Timeout policy [48h]: 7d
Programming language: bash
Will this app need access to the Internet? [y/N]: y
Will this app need access to the parent project? [y/N]: y
Choose an instance type for your app [mem1_ssd1_v2_x4]: mem1_ssd1_v2_x4
# 3. made additional edits to applet scripts in terminal (see uploaded scripts)
## use vim
# 4. build applet
dx build saige_v1.4.2 --overwrite
# 5. upload applet scripts
dx upload -r saige_v1.4.2/ --path project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/scripts/saige_v1.4.2/

# run SAIGE step 1 (using SAIGE GWAS GRM applet)
# 1. run the following code in ttyd terminal
ld_pruned_input_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/ld_pruned"
pheno_input_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/input/"
output_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/step1"

dx run saige_v1.4.2 \
-y \
-iinput="${ld_pruned_input_dir}/ukb21007_all_chr_b0_v1.topmed_imputed.ld_pruned.bim" \
-iinput="${ld_pruned_input_dir}/ukb21007_all_chr_b0_v1.topmed_imputed.ld_pruned.bed" \
-iinput="${ld_pruned_input_dir}/ukb21007_all_chr_b0_v1.topmed_imputed.ld_pruned.fam" \
-iinput="${pheno_input_dir}/UKB.AD.ALL.phenotype_covariates.txt" \
-icommand="step1_fitNULLGLMM.R \
            --plinkFile=input/ukb21007_all_chr_b0_v1.topmed_imputed.ld_pruned \
            --phenoFile=input/UKB.AD.ALL.phenotype_covariates.txt \
            --phenoCol=AD \
            --covarColList=AGE,SEX,PC1,PC2,PC3 \
            --qCovarColList=SEX \
            --sampleIDColinphenoFile=id \
            --traitType=binary \
            --IsOverwriteVarianceRatioFile=TRUE \
            --outputPrefix=output/UKBB.AD_GWAS.saige_step1" \
--brief \
--name "saige_step1" \
--destination ${output_dir} \
--instance-type mem1_ssd1_v2_x8

# freq QC- make bed files for saige step2 & filt samples
# 1. run the following code from ttyd terminal
inital_qc_input_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/initial_qc"
pheno_input_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/input/"
output_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/freq_qc"

for chr in $(seq 1 22)
do
dx run app-swiss-army-knife \
-y \
-iin="${inital_qc_input_dir}/ukb21007_c${chr}_b0_v1.topmed_imputed.initial_qc.pgen" \
-iin="${inital_qc_input_dir}/ukb21007_c${chr}_b0_v1.topmed_imputed.initial_qc.psam" \
-iin="${inital_qc_input_dir}/ukb21007_c${chr}_b0_v1.topmed_imputed.initial_qc.pvar" \
-iin="${pheno_input_dir}/UKB.AD.ALL.postPCA_QC.sample_list.txt" \
--brief \
--name "freq_qc.imputed.chr${chr}" \
-icmd="plink2 --pfile ukb21007_c${chr}_b0_v1.topmed_imputed.initial_qc --maf 0.05 --set-all-var-ids chr@:#:\\\$r:\\\$a --keep-fam UKB.AD.ALL.postPCA_QC.sample_list.txt --make-bed --out ukb21007_c${chr}_b0_v1.topmed_imputed.freq_qc.saige_step2" \
--destination ${output_dir} \
--instance-type mem1_ssd2_v2_x4
done

# run SAIGE step 2 (using SAIGE GWAS- single variant association applet)
# 1. run the following code in ttyd terminal
plink_input_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/freq_qc"
step1_input_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/step1"
output_dir="project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/step2"

for chr in $(seq 1 22)
do
dx run saige_v1.4.2 \
-y \
-iinput="${plink_input_dir}/ukb21007_c${chr}_b0_v1.topmed_imputed.freq_qc.saige_step2.bim" \
-iinput="${plink_input_dir}/ukb21007_c${chr}_b0_v1.topmed_imputed.freq_qc.saige_step2.bed" \
-iinput="${plink_input_dir}/ukb21007_c${chr}_b0_v1.topmed_imputed.freq_qc.saige_step2.fam" \
-iinput="${step1_input_dir}/UKBB.AD_GWAS.saige_step1.varianceRatio.txt" \
-iinput="${step1_input_dir}/UKBB.AD_GWAS.saige_step1.rda" \
-icommand="step2_SPAtests.R \
            --bedFile=input/ukb21007_c${chr}_b0_v1.topmed_imputed.freq_qc.saige_step2.bed \
            --bimFile=input/ukb21007_c${chr}_b0_v1.topmed_imputed.freq_qc.saige_step2.bim \
            --famFile=input/ukb21007_c${chr}_b0_v1.topmed_imputed.freq_qc.saige_step2.fam \
            --GMMATmodelFile=input//UKBB.AD_GWAS.saige_step1.rda \
            --varianceRatioFile=input/UKBB.AD_GWAS.saige_step1.varianceRatio.txt \
            --LOCO=TRUE \
            --chrom=${chr} \
            --is_Firth_beta=TRUE \
            --pCutoffforFirth=0.05 \
            --is_output_moreDetails=TRUE \
            --SAIGEOutputFile=output/UKBB.AD_GWAS.saige_step2.chr${chr}" \
--brief \
--name "saige_step2.chr${chr}" \
--destination ${output_dir} \
--instance-type mem1_ssd1_v2_x4
done

# concatenate outputs
# 1. run the following code from ttyd terminal
dx download project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/step2/UKBB.AD_GWAS.saige_step2.chr*

rm *.index
for i in $(seq 1 22)
do
awk 'NR>1 {print $0}' "UKBB.AD_GWAS.saige_step2.chr"$i > "UKBB.AD_GWAS.saige_step2.chr"$i".no_header.txt"
done
head -n1 UKBB.AD_GWAS.saige_step2.chr22 > header
cat header UKBB.AD_GWAS.saige_step2.chr*.no_header.txt > UKBB.AD_GWAS.saige_step2.all_chr.txt

cut -f6,7,16,17,18,19,20,21,22,23 --complement  UKBB.AD_GWAS.saige_step2.all_chr.txt > UKBB.AD_GWAS.saige_step2.all_chr.for_export.txt
gzip UKBB.AD_GWAS.saige_step2.all_chr.for_export.txt

dx upload UKBB.AD_GWAS.saige_step2.all_chr.for_export.txt.gz UKBB.AD_GWAS.saige_step2.all_chr.txt --path project-GgYky4QJj5pkv6G9P8Zp6P26:/AD_GWAS/output/step2/