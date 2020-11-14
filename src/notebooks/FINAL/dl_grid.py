import pandas as pd

import json

import warnings
warnings.filterwarnings('ignore')


import h2o
h2o.init(min_mem_size='25G')

DATA_LOCATION = "../../data/"
MODELS_LOCATION = "../../models/ALL_FEATURES/FINAL/"


print("Read train and test data")


train = h2o.import_file(DATA_LOCATION + "processed/final.train.tsv")

test = h2o.import_file(DATA_LOCATION + "processed/final.test.tsv")



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




# For binary classification, response should be a factor
train[train_response_col] = train[train_response_col].asfactor()
test[test_response_col] = test[test_response_col].asfactor()


# Number of CV folds (to generate level-one data for stacking)
nfolds = 5

MAX_GRID_MODELS = 20


x = train_predictor_cols
y = train_response_col




from h2o.grid.grid_search import H2OGridSearch


from h2o.grid.grid_search import H2OGridSearch
from h2o.estimators import H2ODeepLearningEstimator



hyper_params = {
#   'adaptive_rate',
#   'categorical_encoding',
#   'classification_stop',
#   'class_sampling_factors',
#   'col_major',
#   'elastic_averaging_moving_rate',
#   'elastic_averaging_regularization',
#   'elastic_averaging',
#   'epsilon',
#   'fast_mode',
#   'force_load_balance',
#   'initial_biases',
#   'initial_weights',
#   'initial_weight_distribution',
#   'initial_weight_scale',

#   'max_after_balance_size',
#   'max_categorical_features',
#   'max_w2',
#   'missing_values_handling',
#   'momentum_ramp',
#   'momentum_stable',
#   'momentum_start',
#   'nesterov_accelerated_gradient',
#   'overwrite_with_best_model',
#   'quantile_alpha',
#   'quiet_mode',
#   'rate_annealing',
#   'rate_decay',
#   'rate',
#   'regression_stop',
#   'replicate_training_data',
#   'reproducible',
#   'score_duty_cycle',
#   'score_interval',
#   'score_training_samples',
#   'score_validation_samples',
#   'score_validation_sampling',
#   'seed',
#   'shuffle_training_data',
#   'single_node_mode',
#   'sparsity_beta',
#   'target_ratio_comm_to_comp',
#   'train_samples_per_iteration',
#   'tweedie_power',
#   'use_all_factor_levels',
#   'variable_importances ',


   'l1': [0, 1e-5, 1e-2],
   'l2': [0, 1e-5, 1e-2],
   'sparse': [ True, False],
   'balance_classes': [ True, False],
       	   'average_activation': [0, 0.5, 1, 3, 5, 7, 10],
	      'epochs': [10, 20, 30],
              "activation" : ['Rectifier', 'RectifierWithDropout', 'TanHWithDropout', 'TanH', 'Maxout', 'MaxoutWithDropout'] ,
              'distribution': ['bernoulli', 'multinomial'],
              "hidden_dropout_ratios": [0, 0.1, 0.2, [0.5, 0.5], [0.5, 0.5]]  ,
              "hidden": [[10, 10, 10], [50], [500, 500], [500, 500, 500]]  ,
              "input_dropout_ratio":[0, 0.10, 0.15, 0.20]  ,
              "rho" : [0.95, 0.90] ,
              "standardize" : [True, False] ,
              'loss': ['Absolute', 'Quadratic', 'Huber', 'CrossEntropy'],
}

search_criteria = {"strategy": "RandomDiscrete", 
                   "max_models": MAX_GRID_MODELS}



base_model = H2ODeepLearningEstimator(

					stopping_metric= 'auc',

                                        keep_cross_validation_predictions = True,
                                        nfolds= nfolds,
                                        fold_assignment = "random",
                                        seed=1234)






# Train the grid
dl_grid = H2OGridSearch(model=base_model,
                     hyper_params=hyper_params,
                     search_criteria=search_criteria)




print("Begin the DL model training")

dl_grid.train(x=x, y=y, training_frame=train, validation_frame=test)

h2o.save_grid(MODELS_LOCATION + "dl_grid", dl_grid.grid_id)

print("Saved the DL model")


