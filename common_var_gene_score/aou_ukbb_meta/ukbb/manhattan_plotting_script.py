import pandas as pd
from manhattan_plot import ManhattanPlot
import argparse as ap

# define arguments
def make_arg_parser():
    parser = ap.ArgumentParser(description = ".")

    parser.add_argument('--annot_input', required = True, help = 'path to annotation input filename')

    parser.add_argument('--sumstats_input', required = True, help = 'path to sumstats input filename')

    parser.add_argument('--title', required = True, help = 'title of plots')

    parser.add_argument('--sumstats_pval_col', required = True, help = 'pval column name in sumstats')

    parser.add_argument('--sumstats_chr_col', required = True, help = 'chromosome column name in sumstats')

    parser.add_argument('--sumstats_pos_col', required = True, help = 'position column name in sumstats')

    parser.add_argument('--sumstats_id_col', required = True, help = 'id column name in sumstats')

    parser.add_argument('--annot_id_col', required=True, help = 'id (can be gene) column name in annotation file')

    parser.add_argument('--annot_chr_col', required = True, help='chromosome column name in annotation file')

    parser.add_argument('--annot_pos_col', required = True, help = 'position column name in annotation file')

    parser.add_argument('--annot_extra_cols', required = False, help = 'space separated extra columns in annotation')

    parser.add_argument('--known_genes', required = True, help = 'path to file with list of known genes')

    parser.add_argument('--sig', required = True, help = 'significance threshold')

    parser.add_argument('--sug', required = True, help = 'suggestive threshold')

    parser.add_argument('--annot', required = True, help = 'annotation threshold')

    parser.add_argument('--plot_sig', required = True, help = 'whether to annotate significant genes (True) or suggestive genes (False)')

    parser.add_argument('--invert', required = True, help = 'whether to invert (True) or not invert (False) the plots')

    parser.add_argument('--output_prefix', required = True, help = 'output prefix')

    return parser

args = make_arg_parser().parse_args()

# parse arguments
annot_input_filename = args.annot_input
sumstats_input_filename = args.sumstats_input

plot_title = args.title

sumstats_pval_col = args.sumstats_pval_col
sumstats_chr_col = args.sumstats_chr_col
sumstats_pos_col = args.sumstats_pos_col
sumstats_id_col = args.sumstats_id_col

annot_id_col = args.annot_id_col
annot_chr_col = args.annot_chr_col
annot_pos_col = args.annot_pos_col
if args.annot_extra_cols:
    annot_extra_cols_list=annot_extra_cols.split(' ')

known_genes_file = args.known_genes

sig_thres = float(args.sig)
sug_thres = float(args.sug)
annot_thres = float(args.annot)

plot_sig_bool = eval(args.plot_sig)
invert_bool = eval(args.invert)

output_prefix = args.output_prefix

annotDF = pd.read_table(annot_input_filename)
annotDF = annotDF[[annot_id_col, annot_chr_col, annot_pos_col]]
annotDF = annotDF.rename(columns = {annot_id_col : 'ID',
                                    annot_chr_col :'#CHROM',
                                    annot_pos_col :'POS'})
annotDF['#CHROM'] = annotDF['#CHROM'].replace('X', 23).astype(int)

known_genes = open(known_genes_file).read().splitlines()

mp = ManhattanPlot(file_path = sumstats_input_filename,
                    title = plot_title,
                    test_rows = None)
mp.load_data(delim = '\t')
mp.clean_data(col_map = {sumstats_chr_col : '#CHROM',
                        sumstats_pos_col : 'POS',
                        sumstats_id_col : 'ID',
                        sumstats_pval_col : 'P'})
if args.annot_extra_cols:
    mp.add_annotations(annotDF, extra_cols = annot_extra_cols_list)
else:
    mp.add_annotations(annotDF)
mp.get_thinned_data()

# QQ plot
## create output file
qq_output_filename = output_prefix + '.QQ_plot.png'
mp.qq_plot(save = qq_output_filename, save_res = 150)

# Vertical With Table
## create output file
vert_man_output_filename = output_prefix + '.vertical_manhattan_plot.png'
mp.update_plotting_parameters(sug = sug_thres,
                                annot_thresh = annot_thres,
                                sig = sig_thres,
                                ld_block = 4E5,
                                merge_genes = False,
                                invert = invert_bool)

mp.full_plot(rep_genes = known_genes,
                 plot_sig = plot_sig_bool,
                 rep_boost = False,
                 keep_chr_pos = True,
                 save_res = 150,
                 save = vert_man_output_filename)

# Horizontal Without Table
## create output file
horiz_man_output_filename = output_prefix + '.horizontal_manhattan_plot.png'
mp.update_plotting_parameters(sug = sug_thres,
                                annot_thresh = annot_thres,
                                sig = sig_thres,
                                ld_block = 4E5,
                                merge_genes = False,
                                invert = invert_bool,
                                vertical = False)

mp.full_plot(rep_genes = known_genes,
                plot_sig = plot_sig_bool,
                rep_boost = False,
                with_table = True,
                save_res = 150,
                save = horiz_man_output_filename)