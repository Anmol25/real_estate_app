import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Property Price Predictor",
    page_icon="🏠"
)

with open('data/df_v2.pkl', 'rb') as file:
    df = pickle.load(file)

with open('model_pipeline_v2.pkl', 'rb') as file:
    model = pickle.load(file)

st.markdown(
    "<h1 style='text-align: center;'>Property Price Predictor</h1>",
    unsafe_allow_html=True
)

# Property Details
det1, det2, det3 = st.columns(3)

with det1:
    property_type = st.selectbox('Property Type', ['House/Villa', 'Flat/Apartment', 'Builder Floor'])
with det2:
    city = st.selectbox('City', ['Chandigarh', 'Mohali', 'Panchkula'])
with det3:
    sector = st.selectbox('Sector', df[df['City'] == city]['Sector'].unique().tolist())

# Property Configurations
st.html("<h3>Property Configurations</h3>")

propconf1, propconf2, propconf3 = st.columns(3)

with propconf1:
    area = float(
        np.log(float(st.number_input("Plot Area(Sq.ft)" if property_type == 'House/Villa' else "Built Up Area(Sq.ft)",
                                     min_value=100.00))))
with propconf2:
    bedRoom = int(st.selectbox("BedRooms", sorted(df['bedRoom'].unique())))

with propconf3:
    bathRoom = int(st.selectbox("BathRooms", sorted(df['bathroom'].unique())))

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

# Floor Features
floor_rise_dict = {
    "Low Rise (0-4)": "Low-Rise",
    "Mid Rise (4-12)": "High-Rise",
    "High Rise (13-40)": "Mid-Rise",
    "Ultra High Rise (40+)": "Ultra-High-Rise"
}

floor_no_dict = {
    'Low-Rise': (["Basement", "Ground"] + list(range(1, 5))),
    'High-Rise': (["Basement", "Ground"] + list(range(1, 13))),
    'Mid-Rise': (["Basement", "Ground"] + list(range(1, 41))),
    'Ultra-High-Rise': (["Basement", "Ground"] + list(range(1, 46)))
}

floor1, floor2 = st.columns(2)

if property_type == 'House/Villa':
    FloorNo = 0
    FloorRise = "Low-Rise"
else:
    with floor1:
        FloorRise = st.selectbox("Floor Rise",
                                 ["Low Rise (0-4)", "Mid Rise (4-12)", "High Rise (13-40)", "Ultra High Rise (40+)"])
        FloorRise = floor_rise_dict[FloorRise]
    with floor2:
        FloorNo = st.selectbox("Floor No.", floor_no_dict[FloorRise])

if FloorNo == "Basement":
    FloorNo = -1
elif FloorNo == "Ground":
    FloorNo = 0
else:
    FloorNo = int(FloorNo)

# Features
st.html("<h3>Features</h3>")

# Property Age
age_dict = {
    "Old Property (10+ Years)": "Old",
    "Moderately Old (5-10 Years)": "ModOld",
    "Relatively New (1-5 Years)": "RelNew",
    "New Property (0-1 Years)": "New",
    "Under Construction": "UndConst"
}

feat1, feat2, feat3 = st.columns(3)
with feat1:
    agePossession = st.selectbox("Property Age", list(age_dict.keys()))
    agePossession = age_dict[agePossession]
with feat2:
    facing = st.selectbox("Facing", sorted(df['facing'].unique()))
with feat3:
    Flooring = st.selectbox("Flooring", df['Flooring'].value_counts().index)


feat4, feat5, feat6 = st.columns(3)
with feat4:
    Furnishing = st.selectbox("Furnishing", ['Semifurnished', 'Unfurnished', 'Furnished'])
with feat5:
    pwrBkp = st.selectbox("Power Backup", ['Full', 'Partial', 'No'])
with feat6:
    facilities = st.selectbox("Facilities", ["Basic", "Standard", "Premium", "Luxurious"])

# Predict
if st.button('Predict', type="primary"):
    data = [[property_type, sector, city, area, bedRoom, bathRoom, balcony, facing,
             FloorNo, FloorRise, agePossession, Flooring, Furnishing, CoveredParking, OpenParking,
             pwrBkp, facilities]]

    columns = ['property_type', 'Sector', 'City', 'Area', 'bedRoom', 'bathroom',
               'balcony', 'facing', 'FloorNo', 'FloorRise', 'agePossession',
               'Flooring', 'Furnishing', 'CoveredParking',
               'OpenParking', 'PowerBackup', 'Facilities Categories']

    one_df = pd.DataFrame(data, columns=columns)
    base = np.expm1(model.predict(one_df))[0]
    low = base - 0.1
    high = base + 0.1
    st.html("<h4>Predicted Price:</h4>")

    if base < 1:
        st.markdown("**Range:** ₹ {} Lacs - ₹ {} Lacs".format(round((low * 100), 2), round((high * 100), 2)))
        st.markdown("**Average Price:** ₹ {} Lacs".format(round((base * 100), 2)))
    else:
        st.markdown("**Range:** ₹ {} Cr - ₹ {} Cr".format(round(low, 2), round(high, 2)))
        st.markdown("**Average Price:** ₹ {} Cr".format(round(base, 2)))
