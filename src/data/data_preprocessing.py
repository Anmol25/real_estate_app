import numpy as np
import pandas as pd
import pickle
import os

def load_data(path:str)->pd.DataFrame:
    df = pd.read_csv(path)
    return df


def main():
    df = load_data("./data/raw/raw.csv")
    
    # Removing unnecessary columns
    cols_drop = ['Pooja Room','Servant Room','Study Room','Store Room',
                 'Other Room','Main Road','Park/Garden','Club','Overlook Others',
                 'Pool','PetFriendly','WheelChairFriendly','24*7 Water',
                   'MuniCorp Water','Borewell/Tank','GatedCommunity']
    df.drop(columns = cols_drop,inplace = True)
    
    #Transforming Columns
    df['price'] = np.log1p(df['price'])
    df['Area'] = np.log(df['Area'])

    data_path = os.path.join("data","processed")
    os.makedirs(data_path)

    df.to_csv(os.path.join(data_path,"data_processed.csv"),index=False)

if __name__ == "__main__":
    main()
