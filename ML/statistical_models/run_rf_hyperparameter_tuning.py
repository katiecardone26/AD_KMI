# load packages
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, average_precision_score, f1_score, balanced_accuracy_score
import sys
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
import gc
from memory_profiler import memory_usage
import time
import inspect
from datetime import datetime
import argparse as ap

start_time = datetime.now()
print("Start time:", start_time, flush = True)

# define memory usage function
def print_mem_usage():
    frame = inspect.currentframe()
    caller_frame = frame.f_back
    lineno = caller_frame.f_lineno
    filename = caller_frame.f_code.co_filename
    mem = memory_usage(-1, interval = 0.1, timeout = 1)
    print(f"[{filename}:{lineno}] Current memory usage: {mem[0]:.2f} MiB")
    
print_mem_usage()

# define arguments
def make_arg_parser():
    parser = ap.ArgumentParser(description = ".")

    parser.add_argument('--input_prefix', required = True, help = 'input prefix')

    parser.add_argument('--key_name', required = True, help = 'key name')

    parser.add_argument('--output_tag', required = True, help = 'phrase to add into output filename')

    return parser

args = make_arg_parser().parse_args()

# parse arguments
input_prefix = args.input_prefix
key_name = args.key_name
output_tag = args.output_tag

# read in input files
print('reading in input files', flush = True)
input_dir = '/ML/statistical_models/input/'
input_suffix = '.statistical_models_input.txt'

input_df = pd.read_csv((input_dir + input_prefix + input_suffix),
sep = '\t').replace([np.inf, -np.inf], np.nan).dropna(axis = 1)
print(input_df.shape)

# make dictionary
print('running models', flush = True)
file_dict = {key_name : input_df}

# make empty lists
train_auroc_list = []
train_auprc_list = []
train_f1_list = []
train_balanced_acc_list = []

test_auroc_list = []
test_auprc_list = []
test_f1_list = []
test_balanced_acc_list = []

best_params_list = []
feature_importance_list = []

# define output dir
output_dir = '/ML/statistical_models/rf_output/iterations/'

# make feature df
features = input_df.columns.tolist()
features.remove('ID')
features.remove('AD')
feature_df = pd.DataFrame({'feature' : features, 'order' : list(range(0, (len(features))))})

# loop through iterations
for iter in list(range(1, 101)):
    print(iter, flush = True)

    # create empty dictionaries
    train_auroc_dict = {key: [] for key in file_dict.keys()}
    train_auprc_dict = {key: [] for key in file_dict.keys()}
    train_f1_dict = {key: [] for key in file_dict.keys()}
    train_balanced_acc_dict = {key: [] for key in file_dict.keys()}

    test_auroc_dict = {key: [] for key in file_dict.keys()}
    test_auprc_dict = {key: [] for key in file_dict.keys()}
    test_f1_dict = {key: [] for key in file_dict.keys()}
    test_balanced_acc_dict = {key: [] for key in file_dict.keys()}

    best_params_dict = {key: [] for key in file_dict.keys()}
    feature_importance_dict = {key: [] for key in file_dict.keys()}

    # define colname
    colname = 'ITER_' + str(iter)

    # loop through dfs
    for key, df in file_dict.items():

        train = df.sample(frac = 0.7, random_state = iter)
        test = df.drop(train.index)
        
        # make predictors list
        predictors = train.columns.tolist()
        predictors.remove('ID')
        predictors.remove('AD')

        # scale data
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(train[predictors])
        X_test_scaled = scaler.transform(test[predictors])
        print(X_train_scaled.shape[1], flush = True)
        
        # make base model
        model = RandomForestClassifier(random_state = iter, n_jobs = -1, class_weight = 'balanced')

        # make hyperparameter grid
        param_grid = {
            'n_estimators': [30, 50, 100, 200, 300, 400, 500, 600],
            'max_depth': [2, 3, 5, 8],
            'min_samples_leaf': [20, 30, 50, 100],
            'max_features': ['sqrt', 'log2']
        }

        # hyperparameter tuning
        random_search = RandomizedSearchCV(estimator = model, param_distributions = param_grid, cv = 5, random_state = iter, scoring = 'balanced_accuracy', n_jobs = -1, n_iter = 10)
        #random_search.fit(X_val_selected, val['AD'])
        random_search.fit(X_train_scaled, train['AD'])

        # select best model
        best_model = random_search.best_estimator_
        best_params_dict[key].append((pd.DataFrame(random_search.best_params_, index = [0]).T.reset_index().rename(columns = {'index' : 'hyperparameter'})))
        #print("Best Parameters:", random_search.best_params_, flush = True)

        # gini index for feature importance
        importances = best_model.feature_importances_
        feature_names = predictors
        feature_importance = pd.DataFrame({'feature' : feature_names, colname : importances})
        feature_importance = feature_df.merge(feature_importance, on = 'feature', how = 'left').sort_values(by = ['order']).drop(columns = ['order'])
        feature_importance_dict[key].append(feature_importance)

        # predict training model
        y_train_pred_bin = best_model.predict(X_train_scaled)
        y_train_pred_cont = best_model.predict_proba(X_train_scaled)[:, 1]

        # test in validation set
        auroc = roc_auc_score(train['AD'], y_train_pred_cont)
        auprc = average_precision_score(train['AD'], y_train_pred_cont)
        f1 = f1_score(train['AD'], y_train_pred_bin)
        balanced_acc = balanced_accuracy_score(train['AD'], y_train_pred_bin)

        train_auroc_dict[key].append(auroc)
        train_auprc_dict[key].append(auprc)
        train_f1_dict[key].append(f1)
        train_balanced_acc_dict[key].append(balanced_acc)

        # test in testing set
        y_test_pred_bin = best_model.predict(X_test_scaled)
        y_test_pred_cont = best_model.predict_proba(X_test_scaled)[:, 1]

        auroc = roc_auc_score(test['AD'], y_test_pred_cont)
        auprc = average_precision_score(test['AD'], y_test_pred_cont)
        f1 = f1_score(test['AD'], y_test_pred_bin)
        balanced_acc = balanced_accuracy_score(test['AD'], y_test_pred_bin)

        test_auroc_dict[key].append(auroc)
        test_auprc_dict[key].append(auprc)
        test_f1_dict[key].append(f1)
        test_balanced_acc_dict[key].append(balanced_acc)

    # make dataframes
    train_auroc_df = pd.DataFrame.from_dict(train_auroc_dict, orient = 'index', columns = [colname])
    train_auprc_df = pd.DataFrame.from_dict(train_auprc_dict, orient = 'index', columns = [colname])
    train_f1_df = pd.DataFrame.from_dict(train_f1_dict, orient = 'index', columns = [colname])
    train_balanced_acc_df = pd.DataFrame.from_dict(train_balanced_acc_dict, orient = 'index', columns = [colname])

    test_auroc_df = pd.DataFrame.from_dict(test_auroc_dict, orient = 'index', columns = [colname])
    test_auprc_df = pd.DataFrame.from_dict(test_auprc_dict, orient = 'index', columns = [colname])
    test_f1_df = pd.DataFrame.from_dict(test_f1_dict, orient = 'index', columns = [colname])
    test_balanced_acc_df = pd.DataFrame.from_dict(test_balanced_acc_dict, orient = 'index', columns = [colname])

    best_params_df =  pd.concat({k: v[0] for k, v in best_params_dict.items()}).reset_index(level = 1, drop = True).rename(columns = {0 : colname})
    feature_importance_df =  pd.concat({k: v[0] for k, v in feature_importance_dict.items()}).reset_index(level = 1, drop = True)

    # append to lists
    train_auroc_list.append(train_auroc_df)
    train_auprc_list.append(train_auprc_df)
    train_f1_list.append(train_f1_df)
    train_balanced_acc_list.append(train_balanced_acc_df)

    test_auroc_list.append(test_auroc_df)
    test_auprc_list.append(test_auprc_df)
    test_f1_list.append(test_f1_df)
    test_balanced_acc_list.append(test_balanced_acc_df)

    best_params_list.append(best_params_df)
    feature_importance_list.append(feature_importance_df)

# concatenate dfs
print('concatenating and exporting', flush = True)
train_auroc_final = pd.concat(train_auroc_list, axis = 1)
train_auprc_final = pd.concat(train_auprc_list, axis = 1)
train_f1_final = pd.concat(train_f1_list, axis = 1)
train_balanced_acc_final = pd.concat(train_balanced_acc_list, axis = 1)

test_auroc_final = pd.concat(test_auroc_list, axis = 1)
test_auprc_final = pd.concat(test_auprc_list, axis = 1)
test_f1_final = pd.concat(test_f1_list, axis = 1)
test_balanced_acc_final = pd.concat(test_balanced_acc_list, axis = 1)

best_params_final = pd.concat(best_params_list, axis = 1)
feature_importance_final = pd.concat(feature_importance_list, axis = 1)

# compute avg metrics
train_auroc_final['TRAIN_AUROC_MEAN'] = train_auroc_final.mean(axis = 1)
train_auprc_final['TRAIN_AUPRC_MEAN'] = train_auprc_final.mean(axis = 1)
train_f1_final['TRAIN_F1_MEAN'] = train_f1_final.mean(axis = 1)
train_balanced_acc_final['TRAIN_BALANCED_ACCURACY_MEAN'] = train_balanced_acc_final.mean(axis = 1)

test_auroc_final['TEST_AUROC_MEAN'] = test_auroc_final.mean(axis = 1)
test_auprc_final['TEST_AUPRC_MEAN'] = test_auprc_final.mean(axis = 1)
test_f1_final['TEST_F1_MEAN'] = test_f1_final.mean(axis = 1)
test_balanced_acc_final['TEST_BALANCED_ACCURACY_MEAN'] = test_balanced_acc_final.mean(axis = 1)

# make combined df with means
mean_comb = pd.concat([train_auroc_final[['TRAIN_AUROC_MEAN']],
                       test_auroc_final[['TEST_AUROC_MEAN']],
                       train_auprc_final[['TRAIN_AUPRC_MEAN']],
                       test_auprc_final[['TEST_AUPRC_MEAN']],
                       train_f1_final[['TRAIN_F1_MEAN']],
                       test_f1_final[['TEST_F1_MEAN']],
                       train_balanced_acc_final[['TRAIN_BALANCED_ACCURACY_MEAN']],
                       test_balanced_acc_final[['TEST_BALANCED_ACCURACY_MEAN']]], axis = 1)
mean_comb  = mean_comb.round(3)

# clean up best params and feature importance dfs
hyperparameter = best_params_final.iloc[:, [0]]
best_params_final = best_params_final.drop(columns = ['hyperparameter'])
best_params_final = pd.concat([hyperparameter, best_params_final], axis = 1)

feature = feature_importance_final.iloc[:, [0]]
feature_importance_final = feature_importance_final.drop(columns = ['feature'])
feature_importance_final = pd.concat([feature, feature_importance_final], axis = 1)

# export dfs
output_dir = '/ML/statistical_models/rf_output/'

train_auroc_final.to_csv(output_dir + 'indiv_metrics/TRAIN.AUROC.RF' + '.' + key_name + '.' + output_tag + '.csv')
train_auprc_final.to_csv(output_dir + 'indiv_metrics/TRAIN.AUPRC.RF' + '.' + key_name + '.' + output_tag + '.csv')
train_f1_final.to_csv(output_dir + 'indiv_metrics/TRAIN.F1_SCORE.RF' + '.' + key_name + '.' + output_tag + '.csv')
train_balanced_acc_final.to_csv(output_dir + 'indiv_metrics/TRAIN.BALANCED_ACCURACY.RF' + '.' + key_name + '.' + output_tag + '.csv')

test_auroc_final.to_csv(output_dir + 'indiv_metrics/TEST.AUROC.RF' + '.' + key_name + '.' + output_tag + '.csv')
test_auprc_final.to_csv(output_dir + 'indiv_metrics/TEST.AUPRC.RF' + '.' + key_name + '.' + output_tag + '.csv')
test_f1_final.to_csv(output_dir + 'indiv_metrics/TEST.F1_SCORE.RF' + '.' + key_name + '.' + output_tag + '.csv')
test_balanced_acc_final.to_csv(output_dir + 'indiv_metrics/TEST.BALANCED_ACCURACY.RF' + '.' + key_name + '.' + output_tag + '.csv')

mean_comb.to_csv(output_dir + 'ALL_SPLITS.MEAN_METRICS.RF' + '.' + key_name + '.' + output_tag + '.csv')

best_params_final.to_csv(output_dir + 'Best_Params.RF' + '.' + key_name + '.' + output_tag + '.csv')
feature_importance_final.to_csv(output_dir + 'Feature_Importance.Gini_Index.RF' + '.' + key_name + '.' + output_tag + '.csv', na_rep = 'NaN')
print_mem_usage()