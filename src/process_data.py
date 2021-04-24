# process the raw train data
# save it in data/processed folder

import os
import argparse
import pandas as pd
from get_data import read_params
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from pickle import dump

def process_and_save_data(config_path):
    config = read_params(config_path)
    raw_train_data_path = config["split_data"]["train_path"]
    raw_test_data_path = config["split_data"]["test_path"]
    processed_train_data_path = config["preprocess"]["train_path"]
    processed_test_data_path = config["preprocess"]["test_path"]

    columns_to_drop = config["preprocess"]["columns_to_drop"]

    model_dir = config["model_dir"]

    df = pd.read_csv(raw_train_data_path, sep=",")
    df_test = pd.read_csv(raw_test_data_path, sep=",")
    temp = df.drop(columns_to_drop, axis=1)
    temp_test = df_test.drop(columns_to_drop, axis=1)

    numerical_features = [feature for feature in temp.columns if temp[feature].dtypes != 'O']
    discrete_feature = [feature for feature in numerical_features if len(temp[feature].unique()) < 25]
    continuous_feature = [feature for feature in numerical_features if feature not in discrete_feature]
    categorical_features = [feature for feature in temp.columns if temp[feature].dtypes == 'O']

    for feature in continuous_feature:
        if 0 in temp[feature].unique():
            pass
        else:
            temp[feature] = np.log(temp[feature])
            temp_test[feature] = np.log(temp_test[feature])
    #rint(categorical_features)
    temp = pd.concat([temp, pd.get_dummies(temp[categorical_features], drop_first=True)], axis=1)
    temp_test = pd.concat([temp_test, pd.get_dummies(temp_test[categorical_features], drop_first=True)], axis=1)
    temp.drop(categorical_features, axis=1, inplace=True)
    temp_test.drop(categorical_features, axis=1, inplace=True)
    temp.rename(columns={'Attrition_Yes': 'Attrition'}, inplace=True)
    temp_test.rename(columns={'Attrition_Yes': 'Attrition'}, inplace=True)

    data = temp.copy()
    data_test = temp_test.copy()
    feature_scale = [feature for feature in data.columns if feature not in continuous_feature]
    feature_scale_test = [feature for feature in data.columns if feature not in continuous_feature]

    # print(data.columns)
    scaler = MinMaxScaler()
    scaler.fit(data[continuous_feature])
    # transform the train and test set, and add Attrition variable
    data = pd.concat([data[feature_scale].reset_index(drop=True),
                      pd.DataFrame(scaler.transform(data[continuous_feature]), columns=continuous_feature)],
                     axis=1)
    # print(len(data.columns))
    data_test = pd.concat([data_test[feature_scale_test].reset_index(drop=True),
                      pd.DataFrame(scaler.transform(data_test[continuous_feature]), columns=continuous_feature)],
                     axis=1)
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "scaler.pkl")
    dump(scaler, open(model_path, 'wb'))
    data.to_csv(processed_train_data_path, sep=",", index=False, encoding='utf-8')
    data_test.to_csv(processed_test_data_path, sep=",", index=False, encoding='utf-8')

if __name__ =="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    process_and_save_data(parsed_args.config)
