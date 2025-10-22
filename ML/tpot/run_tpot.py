def main():
    # load packages
    print('loading packages')
    import pandas as pd
    import numpy as np
    import tpot
    import tpot2
    import tpot.objectives
    from tpot.config import get_search_space
    from sklearn.model_selection import train_test_split
    import dill as pickle
    import seaborn as sns
    import matplotlib.pyplot as plt
    import argparse as ap
    from datetime import datetime
    from memory_profiler import memory_usage
    import inspect
    from sklearn.metrics import get_scorer

    # create memory usage function
    def print_mem_usage():
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        lineno = caller_frame.f_lineno
        filename = caller_frame.f_code.co_filename
        mem = memory_usage(-1, interval = 0.1, timeout = 1)
        print(f"[{filename}:{lineno}] Current memory usage: {mem[0]:.2f} MiB")
    
    print_mem_usage()
    
    # define arguments
    print('defining arguments')
    def make_arg_parser():
        parser = ap.ArgumentParser(description = ".")

        parser.add_argument('--predictor', required = True, help = 'predictor file')

        return parser

    args = make_arg_parser().parse_args()

    # parse arguments
    predictor_file = args.predictor

    # read in inputs
    print('reading in input files')
    predictor = pd.read_csv(predictor_file, sep = ' ')
    adsp_pheno = pd.read_csv('/project/ritchie/projects/AD_KMI/ML/athena/input/ADSP_phenotype.txt', sep = ' ')
    print_mem_usage()

    # clean inputs
    print('cleaning inputs')
    predictor_merge = predictor.merge(adsp_pheno, on = ['ID'], how = 'inner')
    predictor_clean = predictor_merge.drop(columns = ['ID', 'AD'])
    predictor_pheno = predictor_merge[['AD']]
    print_mem_usage()

    # create train and test splits
    print('creating train and test splits')
    x_train, x_test, y_train, y_test = train_test_split(predictor_clean,
                                                        predictor_pheno,
                                                        random_state = 1,
                                                        test_size = 0.3)
    print_mem_usage()

    # define model parameters
    print('defining model parameters')
    linear_with_cross_val_predict_sp = tpot.config.template_search_spaces.get_template_search_spaces(search_space = "linear",
                                                                                                    classification = True,
                                                                                                    inner_predictors = True,
                                                                                                    cross_val_predict_cv = 5)

    est = tpot.TPOTEstimator(
        search_space = 'linear',
        scorers = ['roc_auc_ovr',
                    'average_precision',
                    'f1',
                    'balanced_accuracy',
                    tpot.objectives.complexity_scorer],
        scorers_weights = [1, 1, 1, 1, -1],
        classification = True,
        early_stop = 5,
        verbose = 3,
        max_time_mins = None,
        n_jobs = 20,
        cv = 5,
        memory = 'auto',
        memory_limit = '9GB',
        population_size = 1000,
        generations = 100
    )
    print_mem_usage()

    # fit model
    start_time = datetime.now()
    print('start time =', start_time.strftime("%Y-%m-%d %H:%M:%S"))
    print('fitting model')
    est.fit(x_train, y_train)
    end_time = datetime.now()
    print('end time =', end_time.strftime("%Y-%m-%d %H:%M:%S"))
    print('elapsed time = ', end_time - start_time)
    print_mem_usage()

    # test model
    print('testing model')
    auroc = get_scorer('roc_auc_ovr')
    auprc = get_scorer('average_precision')
    f1 = get_scorer('f1')
    balanced_acc = get_scorer('balanced_accuracy')
    print_mem_usage()

    print(auroc(est, x_test, y_test))
    print(auprc(est, x_test, y_test))
    print(f1(est, x_test, y_test))
    print(balanced_acc(est, x_test, y_test))

if __name__ == "__main__":
    main()