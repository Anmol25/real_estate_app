import numpy as np
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score,KFold, cross_validate
from sklearn.compose import ColumnTransformer
from catboost import CatBoostRegressor
import pickle
import json
import os
import yaml


def load_params(params_path: str) -> int:
    """Load parameters from a YAML file."""
    with open(params_path,'r') as file:
        params = yaml.safe_load(file)
    return params

def load_data(path:str)-> pd.DataFrame:
    df = pd.read_csv(path)
    return df

def create_transformer()-> ColumnTransformer:
    all_cat_cols = ['property_type','Sector','City','facing','FloorRise',
                    'agePossession','Flooring','GatedCommunity','Furnishing',
                    'PowerBackup','Facilities Categories']
    cols_order = ['agePossession','Furnishing','PowerBackup','Facilities Categories']
    cols_no_order = ['property_type','Sector','City','facing','FloorRise','Flooring']

    cols_order_cats = [['Old','ModOld','RelNew','New','UndConst'],
                       ['Unfurnished','Semifurnished','Furnished'],
                       ['No','Partial','Full'],
                       ['Basic','Standard','Premium','Luxurious']]
    
    transformer = ColumnTransformer(
        [
            ('order_cols',OrdinalEncoder(categories=cols_order_cats),cols_order),
            ('no_order_cols',OrdinalEncoder(handle_unknown='use_encoded_value',
                                            unknown_value=-1), cols_no_order)
        ],
        remainder='passthrough'
    )
    return transformer


def create_model(params):
    transformer = create_transformer()
    model = Pipeline(
        [('encoding',transformer),
        ('scaler',StandardScaler()),
        ('cat_boost',CatBoostRegressor(verbose = False,
                                       depth = params['depth'],
                                       iterations = params['iterations'],
                                       learning_rate = params['learning_rate']))]    
    )
    return model

def evaluate_model(model,X,y):
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    scoring = ['r2', 'neg_mean_absolute_error']
    scores = cross_validate(model, X, y, cv=kf, scoring=scoring,return_train_score = True)

    metrics = {
        "Test_MAE": np.expm1(-np.mean(scores['test_neg_mean_absolute_error'])),
        "Test_R2": np.mean(scores['test_r2']),
        "Train_MAE": np.expm1(-np.mean(scores['train_neg_mean_absolute_error'])),
        "Train_R2" : np.mean(scores['train_r2'])
    }

    return metrics

def save_model(model,path):
    with open(path,'wb') as file:
        pickle.dump(model,file)


def save_metrics(metrics,path):
    with open(path, 'w') as file:
        json.dump(metrics, file, indent=4)


def main():
    params = load_params('params.yaml')['model_building']
    train_data = load_data("./data/processed/data_processed.csv")
    X = train_data.iloc[:,:-1]
    y = train_data.iloc[:,-1]

    model = create_model(params)
    metrics = evaluate_model(model,X,y)
    model.fit(X,y)
    os.makedirs("models")

    save_model(model, "models/model.pkl")
    save_metrics(metrics,"reports/metrics.json")


if __name__ == "__main__":
    main()