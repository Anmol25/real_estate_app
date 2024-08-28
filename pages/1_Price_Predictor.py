import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Price Predictor")

with open('data/df.pkl', 'rb') as file:
    df = pickle.load(file)

with open('model_pipeline.pkl', 'rb') as file:
    model = pickle.load(file)

st.title("House Price Predictor")
# Features
property_type = st.selectbox('Property Type', ['House/Villa', 'Flat/Apartment', 'Builder Floor'])
city = st.selectbox('City', ['Chandigarh', 'Mohali', 'Panchkula'])
sector = st.selectbox('Sector', df[df['City'] == city]['Sector'].unique().tolist())
st.html("<h3>Property Configurations</h3>")
area = float(
    np.log(float(st.number_input("Plot Area(Sq.ft)" if property_type == 'House/Villa' else "Built Up Area(Sq.ft)",
                                 min_value=100.00))))
bedRoom = int(st.selectbox("BedRooms", sorted(df['bedRoom'].unique())))
bathRoom = int(st.selectbox("BathRooms", sorted(df['bathroom'].unique())))
balcony = st.selectbox("Balcony", ['1', '2', '3', 'More than 3'])
if balcony == 'More than 3':
    balcony = 4
else:
    balcony = int(balcony)

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

if property_type == 'House/Villa':
    FloorNo = 0
    FloorRise = "Low-Rise"
else:
    FloorRise = st.selectbox("Floor Rise",
                             ["Low Rise (0-4)", "Mid Rise (4-12)", "High Rise (13-40)", "Ultra High Rise (40+)"])
    FloorRise = floor_rise_dict[FloorRise]
    FloorNo = st.selectbox("Floor No.", floor_no_dict[FloorRise])

if FloorNo == "Basement":
    FloorNo = -1
elif FloorNo == "Ground":
    FloorNo = 0
else:
    FloorNo = int(FloorNo)

# Property Age
age_dict = {
    "Old Property (10+ Years)": "Old",
    "Moderately Old (5-10 Years)": "ModOld",
    "Relatively New (1-5 Years)": "RelNew",
    "New Property (0-1 Years)": "New",
    "Under Construction": "UndConst"
}
# parking
CoveredParking = int(st.selectbox("Covered Parking", list(range(0, 11))))
OpenParking = int(st.selectbox("Open Parking", list(range(0, 11))))

agePossession = st.selectbox("Property Age", list(age_dict.keys()))
agePossession = age_dict[agePossession]

# Features
st.html("<h3>Features</h3>")
facing = st.selectbox("Facing", sorted(df['facing'].unique()))
Flooring = st.selectbox("Flooring", df['Flooring'].value_counts().index)
gated = st.selectbox("Gated Community", ['Yes', 'No'])
Furnishing = st.selectbox("Furnishing", ['Semifurnished', 'Unfurnished', 'Furnished'])

# water

st.markdown("Water Supply")
water1, water2, water3 = st.columns(3)
with water1:
    water_247 = (1 if st.checkbox("24/7 Water") else 0)
with water2:
    mc_water = (1 if st.checkbox("Municipal Corporation") else 0)
with water3:
    bwell = (1 if st.checkbox("Borewell/Tank") else 0)

# PowerBackup
pwrBkp = st.selectbox("Power Backup", ['Full', 'Partial', 'No'])
facilities = st.selectbox("Facilities", ["Basic", "Standard", "Premium", "Luxurious"])

if st.button('Predict', type="primary"):
    data = [[property_type, sector, city, area, bedRoom, bathRoom, balcony, facing,
             FloorNo, FloorRise, agePossession, Flooring, gated, Furnishing, CoveredParking, OpenParking,
             water_247, mc_water, bwell, pwrBkp, facilities]]

    columns = ['property_type', 'Sector', 'City', 'Area', 'bedRoom', 'bathroom',
               'balcony', 'facing', 'FloorNo', 'FloorRise', 'agePossession',
               'Flooring', 'GatedCommunity', 'Furnishing', 'CoveredParking',
               'OpenParking', '24*7 Water', 'MuniCorp Water', 'Borewell/Tank',
               'PowerBackup', 'Facilities Categories']

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
