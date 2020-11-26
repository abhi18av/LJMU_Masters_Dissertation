import pandas as pd
import random

import warnings
warnings.filterwarnings('ignore')


import h2o
h2o.init(min_mem_size='50G')

DATA_LOCATION = "../../data/"
MODELS_LOCATION = "../../models/ALL_FEATURES/"

#----------------------------------------------------------------------------------------------

train = h2o.import_file( DATA_LOCATION + "processed/final.train.tsv")
test = h2o.import_file( DATA_LOCATION + "processed/final.test.tsv")

# Identify predictors and response
train_predictor_cols = train.columns
train_response_col = "Resistance_Status"
train_predictor_cols.remove('SampleID')
train_predictor_cols.remove(train_response_col)
print("train frame - predictor column: ", train_predictor_cols[0], train_predictor_cols[-1])
print("train frame - response column: ", train_response_col)



# Identify predictors and response
test_predictor_cols = test.columns
test_response_col = "Resistance_Status"
test_predictor_cols.remove('SampleID')
test_predictor_cols.remove(test_response_col)
print("test frame - predictor columns: ", test_predictor_cols[0], test_predictor_cols[-1])
print("test frame - response column: ", test_response_col)

#----------------------------------------------------------------------------------------------


def extract_params_from_model(actual_params_dict, extra_params = [], additional_keys = {}):
    final_params = actual_params_dict

    columns_to_be_removed =   [
                                'model_id',
                                'validation_frame',
                                'response_column',
                                'ignored_columns',
                                'training_frame',
                                *extra_params
]

    for col_name in columns_to_be_removed:
        del  final_params[col_name]

    return {**final_params, **additional_keys}


#----------------------------------------------------------------------------------------------
from h2o.estimators import H2ONaiveBayesEstimator

base_nb= h2o.load_model(MODELS_LOCATION + "FINAL/top_nb/NaiveBayes_model_python_1605423034668_1")
# base_nb = best_nb_model

top_nb = H2ONaiveBayesEstimator(**extract_params_from_model(base_nb.actual_params))

top_nb.train(x=x, y=y, training_frame=train, validation_frame=test)

# h2o.save_model(top_nb, MODELS_LOCATION + "FINAL/top_nb")

test_perf = top_nb.model_performance(valid=True)

print('AUC on test data: ', test_perf.auc(), "\n\n============================")

# test_perf

#----------------------------------------------------------------------------------------------

from h2o.estimators import H2OGeneralizedLinearEstimator


base_glm= h2o.load_model(MODELS_LOCATION + "FINAL/top_glm/GLM_model_python_1605423034668_20")
# base_glm = best_glm_model

top_glm = H2OGeneralizedLinearEstimator(**extract_params_from_model(base_glm.actual_params, ['lambda']))

top_glm.train(x=x, y=y, training_frame=train, validation_frame=test)

# h2o.save_model(top_glm, MODELS_LOCATION + "FINAL/top_glm")

test_perf = top_glm.model_performance(valid=True)

print('AUC on test data: ', test_perf.auc(), "\n\n============================")

# test_perf


#----------------------------------------------------------------------------------------------
from h2o.estimators import H2OGradientBoostingEstimator


base_gbm= h2o.load_model(MODELS_LOCATION + "FINAL/top_gbm/GBM_model_python_1605423034668_39")
# base_gbm = best_gbm_model

top_gbm = H2OGradientBoostingEstimator(**extract_params_from_model(base_gbm.actual_params))

top_gbm.train(x=x, y=y, training_frame=train, validation_frame=test)

# h2o.save_model(top_gbm, MODELS_LOCATION + "FINAL/top_gbm")

test_perf = top_gbm.model_performance(valid=True)

print('AUC on test data: ', test_perf.auc(), "\n\n============================")

# test_perf


#----------------------------------------------------------------------------------------------
from h2o.estimators import H2OXGBoostEstimator


base_xgb = h2o.load_model(MODELS_LOCATION + "FINAL/top_xgb/XGBoost_model_python_1605423034668_274")
# base_xgb = best_xgb_model

top_xgb = H2OXGBoostEstimator(**extract_params_from_model(base_xgb.actual_params))

top_xgb.train(x=x, y=y, training_frame=train, validation_frame=test)

# h2o.save_model(top_xgb, MODELS_LOCATION + "FINAL/top_xgb")

test_perf = top_xgb.model_performance(valid=True)

print('AUC on test data: ', test_perf.auc(), "\n\n============================")

# test_perf

#----------------------------------------------------------------------------------------------

from h2o.estimators import H2ODeepLearningEstimator



# base_dl = best_dl_model
base_dl = h2o.load_model(MODELS_LOCATION + "FINAL/top_dl/DeepLearning_model_python_1605423034668_341")


top_dl = H2ODeepLearningEstimator(**extract_params_from_model(base_dl.actual_params))

top_dl.train(x=x, y=y, training_frame=train, validation_frame=test)

# h2o.save_model(top_dl, MODELS_LOCATION + "FINAL/top_dl")

test_perf = top_dl.model_performance(valid=True)

print('AUC on test data: ', test_perf.auc(), "\n\n============================")

# test_perf
 
#----------------------------------------------------------------------------------------------

from h2o.estimators import H2ORandomForestEstimator


base_drf = h2o.load_model(MODELS_LOCATION + "FINAL/top_drf/DRF_model_python_1605423034668_386")
# base_drf = best_drf_model

top_drf = H2ORandomForestEstimator(**extract_params_from_model(base_drf.actual_params, 
                                                                extra_params=['weights_column']))


top_drf.train(x=x, y=y, training_frame=train, validation_frame=test)

# h2o.save_model(top_drf, MODELS_LOCATION + "FINAL/top_drf")

test_perf = top_drf.model_performance(valid=True)

print('AUC on test data: ', test_perf.auc(), "\n\n============================")

#----------------------------------------------------------------------------------------------


all_model_hyperparams = {
'naivebayes' : {
             'pca': {
                'laplace': 0.6,
                'min_sdev': 0.1,
                'min_prob': 0.1,
                'eps_sdev': 0.1,
                'eps_prob': 0.3,
        },
            'non_pca': {
                'laplace': 0.3,
                'min_sdev': 0.9,
                'min_prob': 0.1,
                'eps_sdev': 1,
                'eps_prob': 0.1,
        }
    },

'glm' : {
             'pca': {

                'alpha': [
                0.0
            ],
                'theta': 1,
                'tweedie_link_power': 0,
                'tweedie_variance_power': 3,
        },
            'non_pca': {

                'alpha': [
                1.0
            ],
                'theta': 0.3,
                'tweedie_link_power': 0,
                'tweedie_variance_power': 9,
        }
    },


'gbm' : {
             'pca': {
	'learn_rate': 0.9,
	'learn_rate_annealing': 1,
	'distribution':	'bernoulli',
	'quantile_alpha': 0.3,
	'tweedie_power': 1.5,
	'balance_classes':	False,
	'ntrees': 150,
	'max_depth': 10,
	'sample_rate': 0.9,
	'col_sample_rate': 0.3,
	'col_sample_rate_per_tree': 1,
	'col_sample_rate_change_per_level': 1.3,
	'histogram_type': 'RoundRobin',
        },
            'non_pca': {

	'learn_rate': 0.1,
	'learn_rate_annealing': 0.9,
	'distribution':		'bernoulli',
	'quantile_alpha': 1,
	'tweedie_power': 1.9,
	'balance_classes':		False,
	'ntrees': 50,
	'max_depth': 5,
	'sample_rate': 0.9,
	'col_sample_rate': 0.3,
	'col_sample_rate_per_tree': 0.6,
	'col_sample_rate_change_per_level': 0.8,
	'histogram_type':		'Random',
        }
    },


'drf' : {
             'pca': {

	# 'mtries': 150, # doesn't work for some reason
	'balance_classes':	True,
	'ntrees': 100,
	'max_depth': 10,
	'sample_rate': 0.6,
	'col_sample_rate_per_tree': 0.3,
	'col_sample_rate_change_per_level': 0.8,
	'histogram_type':	'Auto',
        },
            'non_pca': {
	'mtries': -1,
	'balance_classes':		True,
	'ntrees': 50,
	'max_depth': 10,
	'sample_rate': 0.3,
	'col_sample_rate_per_tree': 0.6,
	'col_sample_rate_change_per_level': 1.7,
	'histogram_type':		'RoundRobin',
        }
    },


'xgboost' : {
             'pca': {

	'distribution':	'multinomial',
	'categorical_encoding':	'auto',
	'ntrees': 70,
	'booster':	'gbtree',
	'col_sample_rate': 0.6,
	'col_sample_rate_bylevel': 0.6,
	'col_sample_rate_bytree': 0.6,
	'learn_rate': 0.1,
	'grow_policy':	'lossguide',
	'max_depth': 6,
	'normalize_type':	'forest',
	'sample_type':	'uniform',
	'sample_rate': 1,
	'tree_method':	'hist',
	'tweedie_power': 1.5,
        },
            'non_pca': {

	'distribution':		'bernoulli',
	'categorical_encoding':		'label_encoder',
	'ntrees': 50,
	'booster':		'dart',
	'col_sample_rate': 0.8,
	'col_sample_rate_bylevel': 0.8,
	'col_sample_rate_bytree': 0.3,
	'learn_rate': 0.1,
	'grow_policy':		'depthwise',
	'max_depth': 6,
	'normalize_type':		'forest',
	'sample_type':		'weighted',
	'sample_rate': 1,
	'tree_method':		'hist',
	'tweedie_power': 1.5,
        }
    },

'deeplearning' : {
             'pca': {
	'distribution':	'bernoulli',
	'epochs': 20.399,
	'loss':	'CrossEntropy',
	'l1': 1e-5,
	'l2': 0,
	'sparse':	False,
	'balance_classes':	False,
	'average_activation': 10,
	'activation':	'TanH',
	'hidden': [
                500,
                500,
                500
            ],
	'input_dropout_ratio': 0.2,
	'rho': 0.95,
	'standardize': 	False,
        },
            'non_pca': {

	'distribution':		'bernoulli',
	'epochs': 31.1822,
	'loss':		'Automatic',
	'l1': 0,
	'l2': 0,
	'sparse':		False,
	'balance_classes':		False,
	'average_activation': 0,
	'activation':		'RectifierWithDropout',
	'hidden': [
                500,
                500,
                500
            ],
	'input_dropout_ratio': 0,
	'rho': 0.9,
	'standardize': 		True,
        }
    },
}



#----------------------------------------------------------------------------------------------

from h2o.estimators.stackedensemble import H2OStackedEnsembleEstimator

collection_of_models = [
                        top_nb,
                        top_glm,

                        # checkpoint-enabled models
                        top_gbm, # based on boosting, like XGB
                        top_xgb,
                        top_dl,
                        top_drf]


meta_algos = ["xgboost", "drf", "gbm", "glm", "naivebayes", "deeplearning"]

all_models_ensembles_list = []

for metalearner in meta_algos:
    print("\n\n>>>>> ", metalearner, " <<<<<<")

    if metalearner == 'xgboost' or metalearner == 'naivebayes':


        ensemble = H2OStackedEnsembleEstimator(
                                          base_models= collection_of_models,

                                          model_id= "stacked_ensemble_ALL_FEATURES_ALL_MODELS_metalearner_" + metalearner,


                                          metalearner_algorithm= metalearner,

                                          #    metalearner_params = all_model_hyperparams[metalearner]['non_pca'],

                                             metalearner_nfolds = 5,
                                             metalearner_fold_assignment = 'random',
                                             seed=1234
                                          )

    else:

        ensemble = H2OStackedEnsembleEstimator(
                                    base_models= collection_of_models,

                                    model_id= "stacked_ensemble_ALL_FEATURES_ALL_MODELS_metalearner_" + metalearner,


                                    metalearner_algorithm= metalearner,

                                       metalearner_params = all_model_hyperparams[metalearner]['non_pca'],

                                       metalearner_nfolds = 5,
                                       metalearner_fold_assignment = 'random',
                                       seed=1234
                                    )


   
    ensemble.train(x=x, y=y, training_frame=train, validation_frame=test)

    h2o.save_model(ensemble, MODELS_LOCATION + "FINAL/top_ensemble_ALL_MODELS_METALEARNER_" + metalearner)


    print("AUC on test data: ",  ensemble.model_performance(valid=True).auc())

    all_models_ensembles_list.append(ensemble)




#----------------------------------------------------------------------------------------------




from h2o.estimators.stackedensemble import H2OStackedEnsembleEstimator

collection_of_models = [


                        top_gbm, # based on boosting, like XGB
                        top_xgb,
                        top_dl,
                        top_drf]


meta_algos = [ "xgboost", "drf", "gbm", "glm", "naivebayes", "deeplearning"]

checkpoint_ensembles_list = []

for metalearner in meta_algos:
    print("\n\n>>>>> ", metalearner, " <<<<<<")

    if metalearner == 'xgboost' or metalearner == 'naivebayes':


        ensemble = H2OStackedEnsembleEstimator(
                                          base_models= collection_of_models,

                                       model_id= "stacked_ensemble_ALL_FEATURES_CHECKPOINT_MODELS_metalearner_" + metalearner,


                                          metalearner_algorithm= metalearner,

                                          #    metalearner_params = all_model_hyperparams[metalearner]['non_pca'],

                                             metalearner_nfolds = 5,
                                             metalearner_fold_assignment = 'random',
                                             seed=1234
                                          )


    else:
      
      ensemble = H2OStackedEnsembleEstimator(
                                    base_models= collection_of_models,

                                 model_id= "stacked_ensemble_ALL_FEATURES_CHECKPOINT_MODELS_metalearner_" + metalearner,


                                    metalearner_algorithm= metalearner,

                                       metalearner_params = all_model_hyperparams[metalearner]['non_pca'],

                                       metalearner_nfolds = 5,
                                       metalearner_fold_assignment = 'random',
                                       seed=1234
                                    )



    ensemble.train(x=x, y=y, training_frame=train, validation_frame=test)



    h2o.save_model(ensemble, MODELS_LOCATION + "FINAL/top_ensemble_CHECKPOINT_MODELS_METALEARNER_" + metalearner)



    print("AUC on test data: ",  ensemble.model_performance(valid=True).auc())

    checkpoint_ensembles_list.append(ensemble)




from h2o.estimators.stackedensemble import H2OStackedEnsembleEstimator

collection_of_models = [

                        top_xgb,
                        top_dl,
                        top_drf]


meta_algos = ["xgboost", "drf", "gbm", "glm", "naivebayes", "deeplearning"]

min_checkpointable_ensemble_list = []

for metalearner in meta_algos:
    print("\n\n>>>>> ", metalearner, " <<<<<<")

    if metalearner == 'xgboost' or metalearner == 'naivebayes':


        ensemble = H2OStackedEnsembleEstimator(
                                          base_models= collection_of_models,

                                       model_id= "stacked_ensemble_ALL_FEATURES_CHECKPOINT_nogbm_MODELS_metalearner_" + metalearner,


                                          metalearner_algorithm= metalearner,

                                          #    metalearner_params = all_model_hyperparams[metalearner]['non_pca'],

                                             metalearner_nfolds = 5,
                                             metalearner_fold_assignment = 'random',
                                             seed=1234
                                          )


    else:
      
      ensemble = H2OStackedEnsembleEstimator(
                                    base_models= collection_of_models,

                                       model_id= "stacked_ensemble_ALL_FEATURES_CHECKPOINT_nogbm_MODELS_metalearner_" + metalearner,


                                    metalearner_algorithm= metalearner,

                                       metalearner_params = all_model_hyperparams[metalearner]['non_pca'],

                                       metalearner_nfolds = 5,
                                       metalearner_fold_assignment = 'random',
                                       seed=1234
                                    )
           
    ensemble.train(x=x, y=y, training_frame=train, validation_frame=test)

    h2o.save_model(ensemble, MODELS_LOCATION + "FINAL/top_ensemble_CHECKPOINT_nogbm_MODELS_METALEARNER_" + metalearner)


    print("AUC on test data: ",  ensemble.model_performance(valid=True).auc())

    min_checkpointable_ensemble_list.append(ensemble)



