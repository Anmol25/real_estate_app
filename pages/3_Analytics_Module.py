import streamlit as st
import pandas as pd
import pickle
import plotly.express as px

st.set_page_config(
    page_title="Analytical Module",
    page_icon="🏠"
)

st.markdown(
    "<h1 style='text-align: center;'>Analytics Module</h1>",
    unsafe_allow_html=True
)
st.markdown("<p style='text-align: center;'>This module consist of analytical visualizations of the data used in "
            "previous modules.</p>", unsafe_allow_html=True)

with open('data/df_v3.pkl', 'rb') as file:
    main_df = pickle.load(file)

with open('data/sunburst_df.pkl', 'rb') as file:
    sb_df = pickle.load(file)

st.markdown(
    "<h3 style='text-align: center;'>Area VS Price ScatterPlot</h3>",
    unsafe_allow_html=True
)

input1, input2 = st.columns(2)
with input1:
    city_name = st.selectbox('City', ['Tricity', 'Chandigarh', 'Mohali', 'Panchkula'], key=1)
with input2:
    ptype = st.selectbox('Property Type', ['All', 'House/Villa', 'Flat/Apartment'], key=2)


def filter_df(df, city, property_type):
    if city == 'Tricity' and property_type == 'All':
        return df
    if city != 'Tricity' and property_type == 'All':
        return df[df['City'] == city]
    if city == 'Tricity' and property_type != 'All':
        return df[df['property_type'] == property_type]

    # Both city and property_type are specified
    return df[(df['City'] == city) & (df['property_type'] == property_type)]


# Area VS Price
fig1 = px.scatter(filter_df(main_df, city_name, ptype), x='Area', y='price', color='bedRoom', title="Area VS Price",
                  width=800, height=550)
st.plotly_chart(fig1)

st.markdown(
    "<h3 style='text-align: center;'>Sunburst Plot of Property Data</h3>",
    unsafe_allow_html=True
)

input3 = st.selectbox('Property Type', ['House/Villa', 'Flat/Apartment', 'Both'], key=3)

fig2 = px.sunburst(sb_df if input3 == 'Both' else sb_df[sb_df['property_type'] == input3],
                   path=['City', 'Sector'],
                   values='count',
                   color='Price Per Sqft',
                   color_continuous_scale='thermal',
                   title="House Count and Price per Sqft across Cities and Sectors",
                   height=650)

st.plotly_chart(fig2)
st.markdown("In this sunburst plot, size of an element represents elements contribution to size of dataset and "
            "color represent average price per sqft. of that element.")
