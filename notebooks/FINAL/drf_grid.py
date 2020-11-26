import pandas as pd

import json

import warnings
warnings.filterwarnings('ignore')


import h2o
h2o.init(min_mem_size='25G')

DATA_LOCATION = "../../data/"
MODELS_LOCATION = "../../models/ALL_FEATURES/FINAL"


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

MAX_GRID_MODELS = 10


x = train_predictor_cols
y = train_response_col




from h2o.grid.grid_search import H2OGridSearch
from h2o.estimators import H2ORandomForestEstimator



hyper_params = {
'mtries': [-1, 30, 60, 90, 150, 200, 350, 500],
'balance_classes': [True, False],
'ntrees': [10, 20, 50, 100, 150],
'max_depth': [5, 10, 15, 20], # defaults to 20
'sample_rate': [ 0.1, 0.3, 0.6, 0.9],
'col_sample_rate_per_tree': [ 0.1, 0.3, 0.6, 0.8, 1],
'col_sample_rate_change_per_level': [ 0.1, 0.3, 0.6, 0.8, 1, 1.3, 1.5, 1.7, 1.9],
'histogram_type': ["AUTO", "UniformAdaptive", "Random", "QuantilesGlobal", "RoundRobin"]

#'score_tree_interval',
#'min_split_improvement',
#'class_sampling_factors',
#'max_after_balance_size',
#'min_rows', # defaults to 1
#'nbins', # default is 20
#'nbins_top_level', # requires too much tuning
#'nbins_cats', # requires too much tuning
#'r2_stopping',
#'seed',
#'build_tree_one_node',
#'sample_rate_per_class':[ 0.1, 0.9],
}

search_criteria = {"strategy": "RandomDiscrete", 
                   "max_models": MAX_GRID_MODELS}



base_model = H2ORandomForestEstimator(

                                 nfolds=nfolds, 
                                 fold_assignment = "random",
                                 keep_cross_validation_predictions = True,
                                 seed=1234)




# Train the grid
rf_grid = H2OGridSearch(model=base_model,
                     hyper_params=hyper_params,
                     search_criteria=search_criteria,
                     parallelism=1)


print("Begin the DRF model training")

rf_grid.train(x=x, y=y, training_frame=train, validation_frame=test) 

h2o.save_grid(MODELS_LOCATION + "drf_grid", rf_grid.grid_id)

print("Saved the DRF model")

