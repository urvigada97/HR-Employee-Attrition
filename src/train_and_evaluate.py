# load the train and test set
# train algo
# save the metrics, params

import os
import warnings
import sys
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import recall_score, precision_score, f1_score, roc_auc_score
from get_data import read_params
import argparse
import joblib
import json
from urllib.parse import urlparse

def eval_metrics(actual, pred):
    Recall = recall_score(actual, pred, average="weighted")
    Precision = precision_score(actual, pred, average="weighted")
    F1_Score = f1_score(actual, pred, average="weighted")
    AUC = roc_auc_score(actual, pred, average="weighted")
    return Recall, Precision, F1_Score, AUC

def train_and_evaluate(config_path):
    config = read_params(config_path)
    test_data_path = config["preprocess"]["test_path"]
    train_data_path = config["preprocess"]["train_path"]
    model_dir = config["model_dir"]

    c = config["estimators"]["SVC"]["params"]["C"]
    gamma = config["estimators"]["SVC"]["params"]["gamma"]

    target = [config["base"]["target_col"]]

    train = pd.read_csv(train_data_path, sep=",")
    test = pd.read_csv(test_data_path, sep=",")

    train_y = train[target]
    test_y = test[target]

    train_x = train.drop(target, axis=1)
    test_x = test.drop(target, axis=1)

    svc = SVC(C = c, gamma=gamma)
    svc.fit(train_x, train_y)

    predicted_attrition = svc.predict(test_x)
    (Recall, Precision, F1_Score, AUC) = eval_metrics(test_y, predicted_attrition)

    print("SVC model (C=%f, gamma=%f):" % (c, gamma))
    print("  Recall: %s" % Recall)
    print("  Precision: %s" % Precision)
    print("  F1_Score: %s" % F1_Score)
    print("  AUC: %s" % AUC)

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")

    joblib.dump(svc, model_path)


if __name__ =="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_and_evaluate(parsed_args.config)