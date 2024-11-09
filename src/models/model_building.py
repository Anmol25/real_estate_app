import numpy as np
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold, cross_validate
from sklearn.compose import ColumnTransformer
from catboost import CatBoostRegressor
import pickle
import json
import os
import yaml
import logging

# logging configuration
logger = logging.getLogger('model_building')
logger.setLevel('DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel('DEBUG')

file_handler = logging.FileHandler('logs/model_building_errors.log')
file_handler.setLevel('ERROR')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def load_params(params_path: str) -> int:
    """Load parameters from a YAML file."""
    try:
        with open(params_path,'r') as file:
            params = yaml.safe_load(file)
        return params
    except FileNotFoundError:
        logger.error('File not Found %s',e)
        raise
    except yaml.YAMLError as e:
        logger.error("YAMLE error : %s",e)
        raise
    except Exception as e:
        logger.error("Unexpected error occured while loading params file: %s",e)
        raise


def load_data(path:str)-> pd.DataFrame:
    """Load DataFrame from desired path"""
    try:
        df = pd.read_csv(path)
        logger.debug("Data loaded from %s",path)
        return df
    except pd.errors.ParserError as e:
        logger.error('Failed to parse CSV File: %s',e)
        raise
    except Exception as e:
        logger.error("Unexpected error occured while loading the data: %s",e)
        raise


def create_transformer()-> ColumnTransformer:
    """Create Column Transformer"""
    try:
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
    except Exception as e:
        logger.error("Unexpected error while creating Column Transformer: %s",e)
        raise


def create_model(params:dict)->Pipeline:
    """Create Model Pipeline"""
    try:
        transformer = create_transformer()
        model = Pipeline(
            [('encoding',transformer),
            ('scaler',StandardScaler()),
            ('cat_boost',CatBoostRegressor(verbose = False,
                                        depth = params['depth'],
                                        iterations = params['iterations'],
                                        learning_rate = params['learning_rate']))]    
        )
        logger.debug("Model Created.")
        return model
    except Exception as e:
        logger.error("Unexpected error occured while creating model %s",e)
        raise


def evaluate_model(model : Pipeline, X : pd.DataFrame, y : pd.Series) -> dict:
    """Evaluate model using kfold crossval""" 
    try:
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        scoring = ['r2', 'neg_mean_absolute_error']
        scores = cross_validate(model, X, y, cv=kf, scoring=scoring,return_train_score = True)

        metrics = {
            "Test_MAE": np.expm1(-np.mean(scores['test_neg_mean_absolute_error'])),
            "Test_R2": np.mean(scores['test_r2']),
            "Train_MAE": np.expm1(-np.mean(scores['train_neg_mean_absolute_error'])),
            "Train_R2" : np.mean(scores['train_r2'])
        }
        logger.debug("Model Evaluated.")
        return metrics
    except Exception as e:
        logger.error("Unexpected error occured while evaluating model %s",e)
        raise


def save_model(model : Pipeline, path : str)->None:
    """Save model through pickle"""
    try:
        with open(path,'wb') as file:
            pickle.dump(model,file)
        logger.debug("Model saved at %s",path)
    except Exception as e:
        logger.error("Unexpected error occured while saving model %s",e)
        raise


def save_metrics(metrics : dict, path : str) -> None:
    try:
        with open(path, 'w') as file:
            json.dump(metrics, file, indent=4)
        logger.debug("Metrics saved at %s",path)
    except Exception as e:
        logger.error("Unexpected error occured while saving metrics %s",e)
        raise


def main():
    try:
        # Load Params
        params = load_params('params.yaml')['model_building']

        # Load Data
        train_data = load_data("./data/processed/data_processed.csv")

        #Split Data in X and Y
        X = train_data.iloc[:,:-1]
        y = train_data.iloc[:,-1]

        # Create and evaluate model
        model = create_model(params)
        metrics = evaluate_model(model,X,y)

        # Train Model
        model.fit(X,y)

        # Make Directory to save Model
        os.makedirs("models")

        # Save Model and Metrics
        save_model(model, "models/model.pkl")
        save_metrics(metrics,"reports/metrics.json")
    except Exception as e:
        logger.error("Failed to Create Model: %s",e)
        print(f"Error: {e}")


if __name__ == "__main__":
    main()