import streamlit as st
import pickle
import pandas as pd
import numpy as np

def load_pickle(file_path: str):
    """Load Pickle Files"""
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data


def getPropDetails(df : pd.DataFrame) -> tuple:
    """Get Property Configuration Details"""
    det1, det2, det3 = st.columns(3)
    with det1:
        property_type = st.selectbox('Property Type', ['House/Villa', 'Flat/Apartment', 'Builder Floor'])
    with det2:
        city = st.selectbox('City', ['Chandigarh', 'Mohali', 'Panchkula'])
    with det3:
        sector = st.selectbox('Sector', df[df['City'] == city]['Sector'].unique().tolist())
    
    return property_type, city, sector


def getPropConfig1(df: pd.DataFrame,property_type: str)-> tuple:
    """Get Property Configuration of Row 1"""
    propconf1, propconf2, propconf3 = st.columns(3)
    with propconf1:
        area = float(
            np.log(float(st.number_input("Plot Area(Sq.ft)" if property_type == 'House/Villa' else "Built Up Area(Sq.ft)",
                                        min_value=100.00))))
    with propconf2:
        bedRoom = int(st.selectbox("BedRooms", sorted(df['bedRoom'].unique())))

    with propconf3:
        bathRoom = int(st.selectbox("BathRooms", sorted(df['bathroom'].unique())))

    return area, bedRoom, bathRoom


def getPropConfig2()-> tuple:
    """Get Property Configurations of Row 2"""
    propconf4, propconf5, propconf6 = st.columns(3)
    with propconf4:
        balcony = st.selectbox("Balcony", ['1', '2', '3', 'More than 3'])
        if balcony == 'More than 3':
            balcony = 4
        else:
            balcony = int(balcony)
    # parking
    with propconf5:
        CoveredParking = int(st.selectbox("Covered Parking", list(range(0, 11))))
    with propconf6:
        OpenParking = int(st.selectbox("Open Parking", list(range(0, 11))))

    return balcony, CoveredParking, OpenParking


def dataDictionaries()-> tuple:
    """Contain various required dict data"""
    floorRise = {
        "Low Rise (0-4)": "Low-Rise",
        "Mid Rise (4-12)": "High-Rise",
        "High Rise (13-40)": "Mid-Rise",
        "Ultra High Rise (40+)": "Ultra-High-Rise"
    }
    floorNum = {
        'Low-Rise': (["Basement", "Ground"] + list(range(1, 5))),
        'High-Rise': (["Basement", "Ground"] + list(range(1, 13))),
        'Mid-Rise': (["Basement", "Ground"] + list(range(1, 41))),
        'Ultra-High-Rise': (["Basement", "Ground"] + list(range(1, 46)))
    }
    ageDict = {
        "Old Property (10+ Years)": "Old",
        "Moderately Old (5-10 Years)": "ModOld",
        "Relatively New (1-5 Years)": "RelNew",
        "New Property (0-1 Years)": "New",
        "Under Construction": "UndConst"
    }
    return floorRise, floorNum, ageDict


def getFloorFeatures() -> tuple:
    """Get Floor Data"""
    # get floorData
    floorRise_dict = dataDictionaries()[0]
    floorNum_dict = dataDictionaries()[1] 

    floor1, floor2 = st.columns(2)
    with floor1:
            FloorRise = st.selectbox("Floor Rise",
                                    ["Low Rise (0-4)", "Mid Rise (4-12)",
                                     "High Rise (13-40)", "Ultra High Rise (40+)"])
            FloorRise = floorRise_dict[FloorRise]
    with floor2:
        FloorNum = st.selectbox("Floor No.", floorNum_dict[FloorRise])

    # Correcting floor input for model
    if FloorNum == "Basement":
        FloorNum = -1
    elif FloorNum == "Ground":
        FloorNum = 0
    else:
        FloorNum = int(FloorNum)
    
    return FloorRise, FloorNum


def getFeat1(df: pd.DataFrame)-> tuple:
    """Get Property Features Row 1"""
    age_dict = dataDictionaries()[2]
    feat1, feat2, feat3 = st.columns(3)
    with feat1:
        agePossession = st.selectbox("Property Age", list(age_dict.keys()))
        agePossession = age_dict[agePossession]
    with feat2:
        facing = st.selectbox("Facing", sorted(df['facing'].unique()))
    with feat3:
        Flooring = st.selectbox("Flooring", df['Flooring'].value_counts().index)

    return agePossession, facing, Flooring


def getFeat2()-> tuple:
    """Get Property Features Row 2"""
    feat4, feat5, feat6 = st.columns(3)
    with feat4:
        Furnishing = st.selectbox("Furnishing", ['Semifurnished', 'Unfurnished', 'Furnished'])
    with feat5:
        pwrBkp = st.selectbox("Power Backup", ['Full', 'Partial', 'No'])
    with feat6:
        facilities = st.selectbox("Facilities", ["Basic", "Standard", "Premium", "Luxurious"])
    
    return Furnishing, pwrBkp, facilities


def convertDF(property_type:str, sector:str, city:str, area:float, bedRoom:int, bathRoom:int, balcony:int, facing:str,
                FloorNum:int, FloorRise:str, agePossession:str, Flooring:str, Furnishing:str, CoveredParking:int, OpenParking:int,
                pwrBkp:str, facilities:str)-> pd.DataFrame:
    """Get all the data collected and convert it to df for prediction"""
    data = [[property_type, sector, city, area, bedRoom, bathRoom, balcony, facing,
                FloorNum, FloorRise, agePossession, Flooring, Furnishing, CoveredParking, OpenParking,
                pwrBkp, facilities]]
    columns = ['property_type', 'Sector', 'City', 'Area', 'bedRoom', 'bathroom',
            'balcony', 'facing', 'FloorNo', 'FloorRise', 'agePossession',
            'Flooring', 'Furnishing', 'CoveredParking',
            'OpenParking', 'PowerBackup', 'Facilities Categories']
    one_df = pd.DataFrame(data, columns=columns)
    return one_df


def printPrediction(base:float)-> None:
    """Print Prediction readable format and choose quantity between Cr or Lac INR"""
    low = base - 0.1
    high = base + 0.1
    st.html("<h4>Predicted Price:</h4>")

    if base < 1:
        st.markdown("**Range:** ₹ {} Lacs - ₹ {} Lacs".format(round((low * 100), 2), round((high * 100), 2)))
        st.markdown("**Average Price:** ₹ {} Lacs".format(round((base * 100), 2)))
    else:
        st.markdown("**Range:** ₹ {} Cr - ₹ {} Cr".format(round(low, 2), round(high, 2)))
        st.markdown("**Average Price:** ₹ {} Cr".format(round(base, 2)))


def main():
    st.set_page_config(
        page_title="Property Price Predictor",
        page_icon="🏠"
    )

    # load dataframe and model
    df = load_pickle('assets/bin/df_v3.pkl')
    #model = load_pickle('model_pipeline_v2.pkl')
    model = load_pickle('assets/models/model.pkl')

    #Page Heading
    st.markdown(
        "<h1 style='text-align: center;'>Property Price Predictor</h1>",
        unsafe_allow_html=True
    )

    # Property Details
    property_type, city, sector = getPropDetails(df)

    # Property Configurations
    st.html("<h3>Property Configurations</h3>")

    # Get Property Configurations
    area, bedRoom, bathRoom = getPropConfig1(df,property_type)
    balcony, OpenParking, CoveredParking = getPropConfig2()
    
    # Floor Features
    # Assign Data according to model assumption(for House/Villa) else get from user
    if property_type == 'House/Villa': 
        FloorNum = 0
        FloorRise = "Low-Rise"
    else:
        FloorRise, FloorNum = getFloorFeatures()

    # Features
    st.html("<h3>Features</h3>")
    agePossession, facing, Flooring = getFeat1(df)
    Furnishing, pwrBkp, facilities = getFeat2()

    # Predict
    if st.button('Predict', type="primary"):
        # convert data into df for prediction
        predictData = convertDF(property_type, sector, city, area, bedRoom, bathRoom, balcony, facing,
                FloorNum, FloorRise, agePossession, Flooring, Furnishing, CoveredParking, OpenParking,
                pwrBkp, facilities)

        prediction = np.expm1(model.predict(predictData))[0]
        printPrediction(prediction)

if __name__ == "__main__":
    main()
