import numpy as np
import pandas as pd
import os
import logging

# logging configuration
logger = logging.getLogger('data_preprocessing')
logger.setLevel('DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel('DEBUG')

file_handler = logging.FileHandler('logs/data_preprocessing_errors.log')
file_handler.setLevel('ERROR')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


def load_data(path:str)->pd.DataFrame:
    """Load Data from file path"""
    try:
        df = pd.read_csv(path)
        logger.debug("Loaded Data from %s",path)
        return df
    except FileNotFoundError:
        logger.error(f"File not Found at {path}")
        raise
    except pd.errors.ParserError as e:
        logger.error('Failed to parse CSV File: %s',e)
        raise
    except Exception as e:
        logger.error("Unexpected error occured while loading the data: %s",e)
        raise


def drop_columns(df:pd.DataFrame)->pd.DataFrame:
    """Drop Unnecessary Columns from DataFrame"""
    try:
        cols_drop = ['Pooja Room','Servant Room','Study Room','Store Room',
                    'Other Room','Main Road','Park/Garden','Club','Overlook Others',
                    'Pool','PetFriendly','WheelChairFriendly','24*7 Water',
                    'MuniCorp Water','Borewell/Tank','GatedCommunity']
        df.drop(columns = cols_drop,inplace = True)
        logger.debug("Columns Dropped from DataFrame")
        return df
    except Exception as e:
        logger.error("Unexpected error occured while dropping columns: %s",e)
        raise


def transform_df(df):
    """Transform DataFrame"""
    try:
        df['price'] = np.log1p(df['price'])
        df['Area'] = np.log(df['Area'])
        logger.debug("Data Transformed in DataFrame")
        return df
    except Exception as e:
        logger.error("Unxpected error occured while transforming data: %s",e)
        raise


def save_df(df,path):
    """Save Dataframe to path"""
    try:
        df.to_csv(path,index=False)
        logger.debug(f"DataFrame saved to: {path}")
    except Exception as e:
        logger.error("Unexpected error occured while saving dataframe: %s",e)
        raise


def main():
    try:
        # Load Data
        df = load_data("./data/raw/raw.csv")

        # Process data
        df = drop_columns(df)
        df = transform_df(df)

        # Make Directory
        data_path = os.path.join("data","processed")
        os.makedirs(data_path)

        # Save DataFrame
        save_df(df,os.path.join(data_path,"data_processed.csv"))

    except Exception as e:
        logger.error("Failed to Process Data: %s",e)
        raise

if __name__ == "__main__":
    main()
