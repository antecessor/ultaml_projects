"""
Get a pandas data frame and train a XGBoost model on it.
"""
import argparse
import os
import pickle
import warnings
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from projects.data.DataPreparation import DataPreparation
from projects.data.data_structs.DataType import DataType
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
    all_data = all_data.select_dtypes(exclude=['object','string'])
    all_y = all_data.iloc[:, -1]
    all_x = all_data.iloc[:, :-1]
    # split data randomly into train and test
    train_x, test_x, train_y, test_y = train_test_split(all_x, all_y, test_size=validation_size / 100)

    dtrain = xgb.DMatrix(train_x, label=train_y)
    dtest = xgb.DMatrix(test_x, label=test_y)
    param = {'max_depth': args.max_depth, 'eta': args.eta, 'objective': args.objective, 'num_class': args.num_class}
    epochs = args.epochs
    bst = xgb.train(param, dtrain, epochs)
    preds = bst.predict(dtest)
    # evaluate predictions
    # check if it is a classification or regression problem
    if args.objective == "reg:squarederror":
        mse = mean_squared_error(test_y, preds)
        print("MSE: %.2f" % mse)
    else:
        # classification
        best_preds = np.asarray([np.argmax(line) for line in preds])
        print("Accuracy = %.2f" % (float(np.sum(best_preds == test_y)) / float(test_y.shape[0])))




if __name__ == "__main__":
    args = get_args()
    train(args)
