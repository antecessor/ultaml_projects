"""
Get a pandas data frame and train a XGBoost model on it.
"""
import argparse
import os
import pickle
import time
import warnings
import zipfile

import numpy as np
import xgboost as xgb


from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from projects.data.DataPreparation import DataPreparation
from projects.data.data_structs.DataType import DataType

from projects.models.results_structs.ClassificationResults import ClassificationResults
from projects.models.results_structs.RegressionResults import RegressionResults
from projects.models.tabular.xgboost.TrainingConfig import TrainingConfig

warnings.filterwarnings("ignore")


def get_args():
    parser = argparse.ArgumentParser()
    # get TrainingConfig as arguments
    trainingConfig = TrainingConfig()

    parser.add_argument("--data_path", type=str, default=trainingConfig.data_path)
    parser.add_argument("--max_depth", type=int, default=trainingConfig.max_depth)
    parser.add_argument("--eta", type=float, default=trainingConfig.eta)
    parser.add_argument("--objective", type=str, default=trainingConfig.objective)
    parser.add_argument("--num_class", type=int, default=trainingConfig.num_class)
    parser.add_argument("--validation", type=str, default=trainingConfig.validation)
    parser.add_argument("--epochs", type=int, default=10)
    return parser.parse_args()


def train(args):
    if str(args.validation).__contains__("hold_out"):
        validation_size = float(str(args.validation).split("_")[2])
    else:
        validation_size = 30

    all_data = DataPreparation.load_data(args.data_path, DataType.TABULAR).data
    # ignore string columns
    all_data = all_data.select_dtypes(exclude=['object', 'string'])
    all_y = all_data.iloc[:, -1]
    all_x = all_data.iloc[:, :-1]
    # split data randomly into train and test
    train_x, test_x, train_y, test_y = train_test_split(all_x, all_y,
                                                        test_size=validation_size / 100)
    evalset = [(train_x, train_y), (test_x, test_y)]
    dtrain = xgb.DMatrix(train_x, label=train_y)
    dtest = xgb.DMatrix(test_x, label=test_y)
    param = {'max_depth': args.max_depth, 'eta': args.eta, 'objective': args.objective,
             'num_class': args.num_class,
             'eval_metric': 'logloss'}
    epochs = args.epochs
    watchlist = [(dtest, 'eval'), (dtrain, 'train')]
    evals_result = {}
    start = time.time()
    bst = xgb.train(param, dtrain, epochs, watchlist,
                    evals_result=evals_result)
    end = time.time()
    training_time = end - start
    start = time.time()
    preds = bst.predict(dtest)
    end = time.time()
    testing_time = end - start
    # check if it is a classification or regression problem
    if args.objective == "reg:squarederror":
        mse = mean_squared_error(test_y, preds)
        result = RegressionResults(mse=mse, rmse=np.sqrt(mse),
                                   mae=float(
                                       np.mean(np.abs(preds - test_y))),
                                   r2=1 - mse / np.var(test_y),
                                   train_loss=list(evals_result['train'][
                                                       'logloss']),
                                   val_loss=list(evals_result['eval']['logloss']),
                                   train_time_seconds=training_time,
                                   test_time_seconds=testing_time)


    else:
        # classification
        best_preds = np.asarray([np.argmax(line) for line in preds])
        accuracy = float(np.sum(best_preds == test_y)) / float(test_y.shape[0])
        precision = float(np.sum(best_preds == test_y)) / float(best_preds.shape[0])
        recall = float(np.sum(best_preds == test_y)) / float(test_y.shape[0])
        auc = (recall + precision) / 2
        f1 = 2 * (precision * recall) / (precision + recall)
        confusion_matrix = np.zeros((args.num_class, args.num_class))
        feature_importance = bst.get_fscore()
        for i in range(test_y.shape[0]):
            confusion_matrix[int(test_y[i]), int(best_preds[i])] += 1
        confusion_matrix = confusion_matrix.tolist()
        result = ClassificationResults(accuracy=accuracy,
                                       precision=precision,
                                       recall=recall, f1=f1, auc=auc,
                                       confusion_matrix=confusion_matrix,
                                       feature_importance=feature_importance,

                                       train_loss=list(evals_result['train'][
                                           'logloss']),
                                       val_loss=list(evals_result['eval'][
                                           'logloss']),
                                       train_time_seconds=training_time,
                                       test_time_seconds=testing_time)

    # save as pickle
    print(result.to_json())
    results_path = os.path.join(args.data_path, "results.pkl")
    with open(results_path, 'wb') as f:
        pickle.dump(result.to_json(), f)

    # save model
    trained_model_dir = os.path.join(args.data_path, "trained_model")
    if not os.path.exists(trained_model_dir):
        os.makedirs(trained_model_dir)
    model_path = os.path.join(trained_model_dir, "trained_model.pkl")
    with open(model_path, 'wb') as f:
        pickle.dump(bst, f)
    print("model saved to: " + model_path)
    # zip trained_model directory using zip library

    zip_path = os.path.join(args.data_path, "trained_model.zip")
    with zipfile.ZipFile(zip_path, 'w') as zip:
        for file in os.listdir(trained_model_dir):
            zip.write(os.path.join(trained_model_dir, file), file)




if __name__ == "__main__":
    args = get_args()
    train(args)
