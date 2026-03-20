# load packages
import pandas as pd
from sklearn.metrics import pairwise_distances

# read in input files
go = pd.read_csv('/project/ritchie/projects/AD_KMI/pathway_score/pathway_annotation/raw_databases/goa_human.gaf.gz',
                 sep = '\t',
                 comment = '!',
                 header = None,
                 low_memory = False)

ref = pd.read_csv('/project/ritchie/projects/ADSP_Projects/ADSP_Annotations/VEP_annotation_manual_113/ensembl_start_stop/Homo_sapiens.GRCh38.113.refseq.exp_validated.gene_map.csv')

# remove uniprot kb IDs
#go_clean = go[~go[10].str.contains('UniProtKB', na = False)]

# remove names (non-genes)
#go_protein = go_clean[go_clean[10].str.contains(':', na = False)]
#go_protein = (go_protein.assign(GENE = go_protein[10].str.split('|')).explode('GENE').reset_index(drop = True))
#go_protein = go_protein[go_protein['GENE'].str.contains(':')]
#go_protein = (go_protein.assign(GENE = go_protein['GENE'].str.split(':')).explode('GENE').reset_index(drop = True))
#go_protein = go_protein[~go_protein['GENE'].str.contains('protein|pump|complex|variant|isozyme|polymerase|reductase|sodium|chromatin|isocitrate|phosphate|cyclin|methylcrotonyl|heterotrimer|enhancer|UniProtKB', case = False)]

# replace special characters
go[10] = go[10].str.replace('[', '')
go[10] = go[10].str.replace(']', '')
go[10] = go[10].str.replace(')', '')
go[10] = go[10].str.replace('(', ' ')
go[10] = go[10].str.replace("'", '')

# explode gene
print(len(go.index))
go_clean = (go.assign(GENE = go[10].str.split('|')).explode('GENE').reset_index(drop = True))
print(len(go_clean.index))
go_clean = (go_clean.assign(GENE = go_clean['GENE'].str.split(':')).explode('GENE').reset_index(drop = True))
print(len(go_clean.index))
go_clean = (go_clean.assign(GENE = go_clean['GENE'].str.split(';')).explode('GENE').reset_index(drop = True))
print(len(go_clean.index))
go_clean = (go_clean.assign(GENE = go_clean['GENE'].str.split(',')).explode('GENE').reset_index(drop = True))
print(len(go_clean.index))
go_clean = (go_clean.assign(GENE = go_clean['GENE'].str.split('/')).explode('GENE').reset_index(drop = True))
print(len(go_clean.index))
go_clean = (go_clean.assign(GENE = go_clean['GENE'].str.split(' ')).explode('GENE').reset_index(drop = True))
print(len(go_clean.index))

# subset and rename
go_clean = go_clean[[4, 'GENE']]
go_clean = go_clean.rename(columns = {4 : 'PATHWAY_ID'})

# fix some typos
go_clean['GENE'] = go_clean['GENE'].str.replace('^2 x ', '2x', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace('F3x', 'F 3x', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace('B1x2x', 'B 2x', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace(r'GPIA\*', 'GPIA', regex = True)

# remove "2x" symbols
go_clean['GENE'] = go_clean['GENE'].str.replace('^1x', '', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace('^2x', '', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace('^3x', '', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace('^4x', '', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace('^5x', '', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace('^6x', '', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace('^7x', '', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace('^8x', '', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace('^9x', '', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace('^12x', '', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace('^14x', '', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace('^16x', '', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace('^20x', '', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace('^24x', '', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace('^40x', '', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace('^78x', '', regex = True)

go_clean['GENE'] = go_clean['GENE'].str.replace(' 2x', '', regex = True)
go_clean['GENE'] = go_clean['GENE'].str.replace(' 3x', '', regex = True)

# remove duplicates
go_clean = go_clean.drop_duplicates()

# drop missing
go_clean = go_clean.dropna()

# remove protein names
##go_clean = go_clean[~go_clean['GENE'].str.contains('protein|pump|complex|variant|isozyme|polymerase|reductase|sodium|chromatin|isocitrate|phosphate|cyclin|methylcrotonyl|heterotrimer|enhancer|UniProtKB|caspase|tetramer|dimer|active|lectin|receptor|oxidase|hexamer|factor|matrix|carboxylase|compex|kinase|proteasome|dehydrogenase|particle|chaperonin|translocase|module|trimer|antigen|oligome|methylosome|pentamer|inflammasome|ligase|type|channel|PIDDosome|monomer|subunit|adenosyltransferase|complec|collagen|activated|gastric|epsilon|mammalian|mannosyltransferase|complement|system|sensor|alpha|class|rnase|HERVK_113|FOS37502_2|apoptosome|GGTase|dependent|acetylglucosamine|phosphotransferase|Amyloid-beta|Aminoacyl|ATPase|FDPase|mediator|DNA-PK|RB-like|2-7|FOXO3-14-3-3ZETA|FOXO3A-14-3-3ZETA|GRASP65', case = False)]

# remove protein symbols
#go_clean = go_clean[~go_clean['GENE'].str.contains('^UNQ')]

# remove miRNA symbols
#go_clean = go_clean[~go_clean['GENE'].str.contains('miR')]

# remove mitochondral signals
#go_clean = go_clean[~go_clean['GENE'].str.contains('^mt')]
#go_clean = go_clean[~go_clean['GENE'].str.contains('^MT-')]

# remove symbols that start with "x0"
#go_clean = go_clean[~go_clean['GENE'].str.contains('^x0')]

# remove symbols that start with lowercase p
#go_clean = go_clean[~go_clean['GENE'].str.contains('^p')]
#go_clean = go_clean[~go_clean['GENE'].str.contains('^ p')]

# remove symbols that start with hCG
#go_clean = go_clean[~go_clean['GENE'].str.contains('^hCG')]

# remove symbols with 5 prime or 3 prime in them
#go_clean = go_clean[~go_clean['GENE'].str.contains("5\'|3\'", regex = True)]

# remove chr symbols
#go_clean = go_clean[~go_clean['GENE'].str.contains('^Chr')]

# remove symbols that start with tcag7
#go_clean = go_clean[~go_clean['GENE'].str.contains('^tcag7')]

# remove cyt bc1
#go_clean = go_clean[~go_clean['GENE'].isin(['cyt bc1'])]

# remove periods
#go_clean = go_clean[~go_clean['GENE'].str.contains(r'\.', regex = True)]

# remove GluN1
#go_clean = go_clean[~go_clean['GENE'].str.contains('GluN1')]

# remove Ichi
#go_clean = go_clean[~go_clean['GENE'].isin([' Ichi'])]

# remove b2i
#go_clean = go_clean[~go_clean['GENE'].isin([' b2i'])]

# remove ENaC
#go_clean = go_clean[~go_clean['GENE'].isin([' ENaC'])]

# remove PA700
#go_clean = go_clean[~go_clean['GENE'].isin([' PA700'])]

# remove histone proteins
#go_clean = go_clean[~go_clean['GENE'].str.contains('^H4')]

# remove DRB (5
#go_clean = go_clean[~go_clean['GENE'].str.contains('DRB \(5')]

# remove APC/C
#go_clean = go_clean[~go_clean['GENE'].isin(['APC/C'])]

# remove spaces
go_clean['GENE'] = go_clean['GENE'].str.strip()

# filter to ref genes
go_ref = go_clean[go_clean['GENE'].isin(ref['GENE'])]

# create grouped df
#go_group = (go_clean.groupby("PATHWAY_ID")["GENE"].apply(set))

# create input matrix
go_binary = (go_ref.assign(value = 1).pivot_table(index = "PATHWAY_ID", columns = "GENE", values = "value", fill_value = 0))
print(go_binary.shape)

# calculate jaccard similarity
print('calculating jaccard similarity', flush = True)
jaccard_mat = 1 - pairwise_distances(go_binary.values, metric = "jaccard")

# make df
print('making df', flush = True)
jaccard_mat_df = pd.DataFrame(jaccard_mat, index = go_binary.index, columns = go_binary.index)

# export
print('exporting df', flush = True)
jaccard_mat_df.to_csv('go/go_pathways.GRCh38.113.refseq.exp_validated.jaccard_similarity_matrix.csv')