import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

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

# Area VS Price Scatterplot inputs
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


# Area VS Price Scatter Plot
fig1 = px.scatter(filter_df(main_df, city_name, ptype), x='Area', y='price', color='bedRoom', title="Area VS Price",
                  width=800, height=550)
fig1.update_layout(
    xaxis_title="Area(Sqft.)",
    yaxis_title="Price (Crores INR)"
)
st.plotly_chart(fig1)

st.markdown(
    "<h3 style='text-align: center;'>Sunburst Plot of Property Data</h3>",
    unsafe_allow_html=True
)

# Sunburst Plot
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

# BHK pie chart
st.markdown(
    "<h3 style='text-align: center;'>BHK Pie Chart</h3>",
    unsafe_allow_html=True
)
bhk_city = st.selectbox('City', ['Tricity', 'Chandigarh', 'Mohali', 'Panchkula'], key=4)
if bhk_city == 'Tricity':
    fig3 = px.pie(main_df, names='bedRoom')
    st.plotly_chart(fig3)
else:
    sect_list = main_df[main_df['City'] == bhk_city]['Sector'].unique().tolist()
    sect_list.insert(0, 'Overall')
    sector = st.selectbox('Sector', sect_list, key=5)
    if sector == 'Overall':
        fig3 = px.pie(main_df[main_df['City'] == bhk_city], names='bedRoom')
        st.plotly_chart(fig3)
    else:
        fig3 = px.pie(main_df[main_df['Sector'] == sector], names='bedRoom')
        st.plotly_chart(fig3)

# BedRoom Boxplot
st.markdown(
    "<h3 style='text-align: center;'>Bedroom Boxplot</h3>",
    unsafe_allow_html=True
)
box_city = st.selectbox('City', ['Tricity', 'Chandigarh', 'Mohali', 'Panchkula'], key=6)
box_df = main_df[(main_df['bedRoom'] < 5)]
fig4 = px.box((box_df if (box_city == 'Tricity') else box_df[box_df['City'] == box_city]), x='bedRoom', y='price',
              title=f'{box_city}\'s Bedroom Boxplot')
fig4.update_layout(
    xaxis_title="BedRooms",
    yaxis_title="Price (Crores INR)"
)
st.plotly_chart(fig4)

# KDE Plot of price
st.markdown(
    "<h3 style='text-align: center;'>KDE plot of prices</h3>",
    unsafe_allow_html=True
)
kde_city = st.selectbox('City', ['Tricity', 'Chandigarh', 'Mohali', 'Panchkula'], key=7)
fig5 = plt.figure(figsize=(10, 5))
sns.kdeplot((main_df if kde_city == 'Tricity' else main_df[main_df['City'] == kde_city]), x='price',
            hue='property_type')
plt.title(f'KDE Plot of Property Price in {kde_city}')
plt.xlabel('Price(Crores INR)')
st.pyplot(fig5)
