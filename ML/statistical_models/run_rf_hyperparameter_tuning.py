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

    parser.add_argument('--sample', required = True, help = 'type of sampling', choices = ['random', 'even_omics'])

    parser.add_argument('--output_tag', required = True, help = 'phrase to add into output filename')

    return parser

args = make_arg_parser().parse_args()

# parse arguments
input_prefix = args.input_prefix
key_name = args.key_name
sample = args.sample
output_tag = args.output_tag

# read in input files
print('reading in input files', flush = True)
input_dir = 'ML/statistical_models/input/'
input_suffix = '.statistical_models_input.txt'

input_df = pd.read_csv((input_dir + input_prefix + input_suffix),
sep = '\t').replace([np.inf, -np.inf], np.nan).dropna(axis = 1)
print(input_df.shape)

all_omics = pd.read_csv('ML/statistical_models/input/AD_KMI.multiomics.sample_list.txt',
sep = '\t')

# make dictionary
print('running models', flush = True)
file_dict = {key_name : input_df}

# make empty lists
train_auroc_list = []
train_auprc_list = []
train_f1_list = []
train_balanced_acc_list = []

val_auroc_list = []
val_auprc_list = []
val_f1_list = []
val_balanced_acc_list = []

test_auroc_list = []
test_auprc_list = []
test_f1_list = []
test_balanced_acc_list = []

selected_features_list = []
best_params_list = []
feature_importance_list = []

# define output dir
output_dir = 'ML/statistical_models/rf_output/iterations/'

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

    val_auroc_dict = {key: [] for key in file_dict.keys()}
    val_auprc_dict = {key: [] for key in file_dict.keys()}
    val_f1_dict = {key: [] for key in file_dict.keys()}
    val_balanced_acc_dict = {key: [] for key in file_dict.keys()}

    test_auroc_dict = {key: [] for key in file_dict.keys()}
    test_auprc_dict = {key: [] for key in file_dict.keys()}
    test_f1_dict = {key: [] for key in file_dict.keys()}
    test_balanced_acc_dict = {key: [] for key in file_dict.keys()}

    selected_features_dict = {key: [] for key in file_dict.keys()}
    best_params_dict = {key: [] for key in file_dict.keys()}
    feature_importance_dict = {key: [] for key in file_dict.keys()}

    # define colname
    colname = 'ITER_' + str(iter)
    
    # loop through dfs
    for key, df in file_dict.items():

        # split dataset
        if sample == 'random':
            train = df.sample(frac = 0.7, random_state = iter)
            no_train = df.drop(train.index)
            val = no_train.sample(frac = 0.5, random_state = iter)
            test = no_train.drop(val.index)
        elif sample == 'even_omics':
            # split into omics and no omics
            target = df[df['ID'].isin(all_omics['ID'])]
            no_target = df[~df['ID'].isin(all_omics['ID'])]

            # get even omics samples
            target_train = target.sample(n = 255, random_state = iter)
            target_no_train = target.drop(target_train.index)
            target_val = target_no_train.sample(frac = 0.5, random_state = iter)
            target_test = target_no_train.drop(target_val.index)

            # get gene score sample numbers
            train_total = int(len(df) * 0.7)
            train_remaining = train_total - 254

            # get rest of splits with gene score samples
            no_target_train = no_target.sample(n = train_remaining, random_state = iter)
            no_target_no_train = no_target.drop(no_target_train.index)
            no_target_val = no_target_no_train.sample(frac = 0.5, random_state = iter)
            no_target_test = no_target_no_train.drop(no_target_val.index)

            # concat
            train = pd.concat([target_train, no_target_train], axis = 0)
            no_train = pd.concat([target_no_train, no_target_no_train], axis = 0)
            val = pd.concat([target_val, no_target_val], axis = 0)
            test = pd.concat([target_test, no_target_test], axis = 0)
        else:
            sys.exit('check sample argument')

        # make predictors list
        predictors = train.columns.tolist()
        predictors.remove('ID')
        predictors.remove('AD')

        # scale data
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(train[predictors])
        X_val_scaled = scaler.transform(val[predictors])
        X_test_scaled = scaler.transform(test[predictors])

        # create 5-fold CV for training
        kf = StratifiedKFold(n_splits = 5, shuffle = True, random_state = iter)

        # create empty lists for training
        cv_train_auroc_list = []
        cv_train_auprc_list = []
        cv_train_f1_list = []
        cv_train_balanced_acc_list = []
        cv_train_selected_features = []

        # loop through CVs
        for train_idx, val_idx in kf.split(X_train_scaled, train[['AD']]):

            # split data
            X_cv_train_scaled, X_cv_val_scaled = X_train_scaled[train_idx], X_train_scaled[val_idx]
            y_cv_train, y_cv_val = train['AD'].iloc[train_idx], train['AD'].iloc[val_idx]

            # build model
            train_model = RandomForestClassifier(n_estimators = 100, random_state = iter, n_jobs = -1, class_weight = 'balanced')

            # perform feature selection
            feature_selector = train_model.fit(X_cv_train_scaled, y_cv_train)

            # select features
            #selector = SelectFromModel(feature_selector, threshold = "median", prefit = True)
            importances = feature_selector.feature_importances_
            threshold = np.percentile(importances, 75)
            selector = SelectFromModel(feature_selector, threshold = threshold, prefit = True)
            
            # append selected feature mask to list
            selected_mask = selector.get_support()
            cv_train_selected_features.append(selected_mask)
        
            # select features in CVs
            X_cv_train_selected = selector.transform(X_cv_train_scaled)
            X_cv_val_selected = selector.transform(X_cv_val_scaled)

            # rebuild model
            train_model = RandomForestClassifier(n_estimators = 100, random_state = iter, n_jobs = -1, class_weight = 'balanced')

            # fit model with selected features
            train_model.fit(X_cv_train_selected,  y_cv_train)

            # predict
            y_cv_val_pred_bin = train_model.predict(X_cv_val_selected)
            y_cv_val_pred_cont = train_model.predict_proba(X_cv_val_selected)[:, 1]

            # compute metrics
            auroc = roc_auc_score(y_cv_val, y_cv_val_pred_cont)
            auprc = average_precision_score(y_cv_val, y_cv_val_pred_cont)
            f1 = f1_score(y_cv_val, y_cv_val_pred_bin)
            balanced_acc = balanced_accuracy_score(y_cv_val, y_cv_val_pred_bin)

            # append to lists
            cv_train_auroc_list.append(auroc)
            cv_train_auprc_list.append(auprc)
            cv_train_f1_list.append(f1)
            cv_train_balanced_acc_list.append(balanced_acc)
        
        # compute mean metrics across CVs
        auroc = np.mean(cv_train_auroc_list)
        auprc = np.mean(cv_train_auprc_list)
        f1 = np.mean(cv_train_f1_list)
        balanced_acc = np.mean(cv_train_balanced_acc_list)

        # append to dictionary
        train_auroc_dict[key].append(auroc)
        train_auprc_dict[key].append(auprc)
        train_f1_dict[key].append(f1)
        train_balanced_acc_dict[key].append(balanced_acc)

        # create feature mask of features that appeared in at least 3/5 CVs
        feature_matrix = np.vstack(cv_train_selected_features)
        feature_counts = np.sum(feature_matrix, axis = 0)
        #final_features = feature_counts >= 3
        final_features = feature_counts >= 4

        # append to dictionary
        selected_features = np.array(predictors)[final_features]
        feature_names = selected_features
        selected_features = ', '.join(selected_features)
        selected_features_dict[key].append(selected_features)
        print(len(selected_features), flush = True)

        # select features in val and test
        X_val_selected = X_val_scaled[:, final_features]
        X_test_selected = X_test_scaled[:, final_features]
        print(X_val_selected.shape[1], flush = True)
        
        # make base model
        model = RandomForestClassifier(random_state = iter, n_jobs = -1, class_weight = 'balanced')

        # make hyperparameter grid
        param_grid = {
            'n_estimators': [300, 400, 500, 600],
            'max_depth': [3, 5, 8],
            'min_samples_leaf': [10, 20, 50, 100],
            'max_features': ['sqrt', 'log2']
        }

        # hyperparameter tuning
        random_search = RandomizedSearchCV(estimator = model, param_distributions = param_grid, cv = 5, random_state = iter, scoring = 'balanced_accuracy', n_jobs = -1, n_iter = 10)
        random_search.fit(X_val_selected, val['AD'])

        # select best model
        best_model = random_search.best_estimator_
        best_params_dict[key].append((pd.DataFrame(random_search.best_params_, index = [0]).T.reset_index().rename(columns = {'index' : 'hyperparameter'})))
        #print("Best Parameters:", random_search.best_params_, flush = True)

        # gini index for feature importance
        importances = best_model.feature_importances_
        feature_importance = pd.DataFrame({'feature' : feature_names, colname : importances})
        feature_importance = feature_df.merge(feature_importance, on = 'feature', how = 'left').sort_values(by = ['order']).drop(columns = ['order'])
        feature_importance_dict[key].append(feature_importance)

        # predict validation model
        y_val_pred_bin = best_model.predict(X_val_selected)
        y_val_pred_cont = best_model.predict_proba(X_val_selected)[:, 1]

        # test in validation set
        y_val_pred_bin = best_model.predict(X_val_selected)
        y_val_pred_cont = best_model.predict_proba(X_val_selected)[:, 1]

        auroc = roc_auc_score(val['AD'], y_val_pred_cont)
        auprc = average_precision_score(val['AD'], y_val_pred_cont)
        f1 = f1_score(val['AD'], y_val_pred_bin)
        balanced_acc = balanced_accuracy_score(val['AD'], y_val_pred_bin)

        val_auroc_dict[key].append(auroc)
        val_auprc_dict[key].append(auprc)
        val_f1_dict[key].append(f1)
        val_balanced_acc_dict[key].append(balanced_acc)

        # test in testing set
        y_test_pred_bin = best_model.predict(X_test_selected)
        y_test_pred_cont = best_model.predict_proba(X_test_selected)[:, 1]

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

    val_auroc_df = pd.DataFrame.from_dict(val_auroc_dict, orient = 'index', columns = [colname])
    val_auprc_df = pd.DataFrame.from_dict(val_auprc_dict, orient = 'index', columns = [colname])
    val_f1_df = pd.DataFrame.from_dict(val_f1_dict, orient = 'index', columns = [colname])
    val_balanced_acc_df = pd.DataFrame.from_dict(val_balanced_acc_dict, orient = 'index', columns = [colname])
    
    test_auroc_df = pd.DataFrame.from_dict(test_auroc_dict, orient = 'index', columns = [colname])
    test_auprc_df = pd.DataFrame.from_dict(test_auprc_dict, orient = 'index', columns = [colname])
    test_f1_df = pd.DataFrame.from_dict(test_f1_dict, orient = 'index', columns = [colname])
    test_balanced_acc_df = pd.DataFrame.from_dict(test_balanced_acc_dict, orient = 'index', columns = [colname])

    selected_features_df = pd.DataFrame.from_dict(selected_features_dict, orient = 'index', columns = [colname])
    best_params_df =  pd.concat({k: v[0] for k, v in best_params_dict.items()}).reset_index(level = 1, drop = True).rename(columns = {0 : colname})
    feature_importance_df =  pd.concat({k: v[0] for k, v in feature_importance_dict.items()}).reset_index(level = 1, drop = True)

    # append to lists
    train_auroc_list.append(train_auroc_df)
    train_auprc_list.append(train_auprc_df)
    train_f1_list.append(train_f1_df)
    train_balanced_acc_list.append(train_balanced_acc_df)

    val_auroc_list.append(val_auroc_df)
    val_auprc_list.append(val_auprc_df)
    val_f1_list.append(val_f1_df)
    val_balanced_acc_list.append(val_balanced_acc_df)

    test_auroc_list.append(test_auroc_df)
    test_auprc_list.append(test_auprc_df)
    test_f1_list.append(test_f1_df)
    test_balanced_acc_list.append(test_balanced_acc_df)

    selected_features_list.append(selected_features_df)
    best_params_list.append(best_params_df)
    feature_importance_list.append(feature_importance_df)

# concatenate dfs
print('concatenating and exporting', flush = True)
train_auroc_final = pd.concat(train_auroc_list, axis = 1)
train_auprc_final = pd.concat(train_auprc_list, axis = 1)
train_f1_final = pd.concat(train_f1_list, axis = 1)
train_balanced_acc_final = pd.concat(train_balanced_acc_list, axis = 1)

val_auroc_final = pd.concat(val_auroc_list, axis = 1)
val_auprc_final = pd.concat(val_auprc_list, axis = 1)
val_f1_final = pd.concat(val_f1_list, axis = 1)
val_balanced_acc_final = pd.concat(val_balanced_acc_list, axis = 1)

test_auroc_final = pd.concat(test_auroc_list, axis = 1)
test_auprc_final = pd.concat(test_auprc_list, axis = 1)
test_f1_final = pd.concat(test_f1_list, axis = 1)
test_balanced_acc_final = pd.concat(test_balanced_acc_list, axis = 1)

selected_features_final = pd.concat(selected_features_list, axis = 1)
best_params_final = pd.concat(best_params_list, axis = 1)
feature_importance_final = pd.concat(feature_importance_list, axis = 1)

# compute avg metrics
train_auroc_final['TRAIN_AUROC_MEAN'] = train_auroc_final.mean(axis = 1)
train_auprc_final['TRAIN_AUPRC_MEAN'] = train_auprc_final.mean(axis = 1)
train_f1_final['TRAIN_F1_MEAN'] = train_f1_final.mean(axis = 1)
train_balanced_acc_final['TRAIN_BALANCED_ACCURACY_MEAN'] = train_balanced_acc_final.mean(axis = 1)

val_auroc_final['VAL_AUROC_MEAN'] = val_auroc_final.mean(axis = 1)
val_auprc_final['VAL_AUPRC_MEAN'] = val_auprc_final.mean(axis = 1)
val_f1_final['VAL_F1_MEAN'] = val_f1_final.mean(axis = 1)
val_balanced_acc_final['VAL_BALANCED_ACCURACY_MEAN'] = val_balanced_acc_final.mean(axis = 1)

test_auroc_final['TEST_AUROC_MEAN'] = test_auroc_final.mean(axis = 1)
test_auprc_final['TEST_AUPRC_MEAN'] = test_auprc_final.mean(axis = 1)
test_f1_final['TEST_F1_MEAN'] = test_f1_final.mean(axis = 1)
test_balanced_acc_final['TEST_BALANCED_ACCURACY_MEAN'] = test_balanced_acc_final.mean(axis = 1)

# make combined df with means
mean_comb = pd.concat([train_auroc_final[['TRAIN_AUROC_MEAN']],
                       val_auroc_final[['VAL_AUROC_MEAN']],
                       test_auroc_final[['TEST_AUROC_MEAN']],
                       train_auprc_final[['TRAIN_AUPRC_MEAN']],
                       val_auprc_final[['VAL_AUPRC_MEAN']],
                       test_auprc_final[['TEST_AUPRC_MEAN']],
                       train_f1_final[['TRAIN_F1_MEAN']],
                       val_f1_final[['VAL_F1_MEAN']],
                       test_f1_final[['TEST_F1_MEAN']],
                       train_balanced_acc_final[['TRAIN_BALANCED_ACCURACY_MEAN']],
                       val_balanced_acc_final[['VAL_BALANCED_ACCURACY_MEAN']],
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
output_dir = 'ML/statistical_models/rf_output/'

train_auroc_final.to_csv(output_dir + 'indiv_metrics/TRAIN.AUROC.RF' + '.' + key_name + '.' + output_tag + '.csv')
train_auprc_final.to_csv(output_dir + 'indiv_metrics/TRAIN.AUPRC.RF' + '.' + key_name + '.' + output_tag + '.csv')
train_f1_final.to_csv(output_dir + 'indiv_metrics/TRAIN.F1_SCORE.RF' + '.' + key_name + '.' + output_tag + '.csv')
train_balanced_acc_final.to_csv(output_dir + 'indiv_metrics/TRAIN.BALANCED_ACCURACY.RF' + '.' + key_name + '.' + output_tag + '.csv')

val_auroc_final.to_csv(output_dir + 'indiv_metrics/VAL.AUROC.RF' + '.' + key_name + '.' + output_tag + '.csv')
val_auprc_final.to_csv(output_dir + 'indiv_metrics/VAL.AUPRC.RF' + '.' + key_name + '.' + output_tag + '.csv')
val_f1_final.to_csv(output_dir + 'indiv_metrics/VAL.F1_SCORE.RF' + '.' + key_name + '.' + output_tag + '.csv')
val_balanced_acc_final.to_csv(output_dir + 'indiv_metrics/VAL.BALANCED_ACCURACY.RF' + '.' + key_name + '.' + output_tag + '.csv')

test_auroc_final.to_csv(output_dir + 'indiv_metrics/TEST.AUROC.RF' + '.' + key_name + '.' + output_tag + '.csv')
test_auprc_final.to_csv(output_dir + 'indiv_metrics/TEST.AUPRC.RF' + '.' + key_name + '.' + output_tag + '.csv')
test_f1_final.to_csv(output_dir + 'indiv_metrics/TEST.F1_SCORE.RF' + '.' + key_name + '.' + output_tag + '.csv')
test_balanced_acc_final.to_csv(output_dir + 'indiv_metrics/TEST.BALANCED_ACCURACY.RF' + '.' + key_name + '.' + output_tag + '.csv')

mean_comb.to_csv(output_dir + 'ALL_SPLITS.MEAN_METRICS.RF' + '.' + key_name + '.' + output_tag + '.csv')

selected_features_final.to_csv((output_dir + 'Selected_Features.RF' + '.' + key_name + '.' + output_tag + '.txt'), sep = '\t')
best_params_final.to_csv(output_dir + 'Best_Params.RF' + '.' + key_name + '.' + output_tag + '.csv')
feature_importance_final.to_csv(output_dir + 'Feature_Importance.Gini_Index.RF' + '.' + key_name + '.' + output_tag + '.csv', na_rep = 'NaN')
print_mem_usage()