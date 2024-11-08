import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


def load_pickle(file_path: str):
    """Load Pickle Files"""
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data


def aVp_Input()-> tuple:
    """Get Input for Area VS Price Scatter Plot"""
    input1, input2 = st.columns(2)
    with input1:
        city_name = st.selectbox('City', ['Tricity', 'Chandigarh', 'Mohali', 'Panchkula'], key=1)
    with input2:
        ptype = st.selectbox('Property Type', ['All', 'House/Villa', 'Flat/Apartment'], key=2)
    return city_name, ptype


def filterDF_aVp(df: pd.DataFrame, city: str, property_type: str)-> pd.DataFrame:
    """Filter DataFrame for Area VS Price ScatterPlot"""
    if city == 'Tricity' and property_type == 'All':
        return df
    if city != 'Tricity' and property_type == 'All':
        return df[df['City'] == city]
    if city == 'Tricity' and property_type != 'All':
        return df[df['property_type'] == property_type]

    # Both city and property_type are specified
    return df[(df['City'] == city) & (df['property_type'] == property_type)]


def filterDF_SB(input: str,df: pd.DataFrame)-> pd.DataFrame:
    """Filter DataFrame for SunBurst Plot"""
    if input == "Both":
        return df
    else:
        return (df[df['property_type'] == input])


def filterDF_Pie(df:pd.DataFrame)-> pd.DataFrame:
    """Take input and Filter DataFrame for PieChart"""
    bhk_city = st.selectbox('City', ['Tricity', 'Chandigarh', 'Mohali', 'Panchkula'], key=4)
    if bhk_city == 'Tricity':
        return df
    else:
        # filter on basis of city and extract sectors
        filterCity = df[df['City'] == bhk_city]
        sect_list = filterCity['Sector'].unique().tolist()
        sect_list.insert(0, 'Overall')
        # Take input from user about Sector
        sector = st.selectbox('Sector', sect_list, key=5)

        if sector == 'Overall':
            return filterCity
        else:
            # Filter on Basis of Sector
            filterSector = df[df['Sector'] == sector]
            return filterSector


def filterDF_Box(df:pd.DataFrame) -> tuple:
    """Take Input and Filter on Basis of City for BoxPlot"""
    city = st.selectbox('City', ['Tricity', 'Chandigarh', 'Mohali', 'Panchkula'], key=6)
    box_df = df[(df['bedRoom'] < 5)] # limit only till 4 bedRooms
    if city == "Tricity":
        return box_df, city
    else:
        filterCity = box_df[box_df['City'] == city]
        return filterCity, city


def filterDF_KDE(df:pd.DataFrame) -> tuple:
    """Take Input and Filter on Basis of City for KDE plot"""
    city = st.selectbox('City', ['Tricity', 'Chandigarh', 'Mohali', 'Panchkula'], key=7)
    if city == "Tricity":
        return df , city
    else:
        filterCity = df[df['City'] == city]
        return filterCity, city

def main():
    st.set_page_config(
        page_title="Analytical Module",
        page_icon="🏠"
    )

    st.markdown(
        "<h1 style='text-align: center;'>Analytical Module</h1>",
        unsafe_allow_html=True
    )
    st.markdown("<p style='text-align: center;'>This module consist of analytical visualizations of the data used in "
                "previous modules.</p>", unsafe_allow_html=True)

    # Load main dataframe and suburst dataframe
    main_df = load_pickle('data/bin/df_v3.pkl')
    sb_df = load_pickle('data/bin/sunburst_df.pkl')
    

    ## Area VS Price Scatter Plot
    st.markdown(
        "<h3 style='text-align: center;'>Area VS Price ScatterPlot</h3>",
        unsafe_allow_html=True
    )
    # Area VS Price Scatterplot inputs
    city_name, ptype = aVp_Input()
    fig1 = px.scatter(filterDF_aVp(main_df, city_name, ptype), x='Area', y='price', color='bedRoom', title="Area VS Price",
                    width=800, height=550)
    fig1.update_layout(
        xaxis_title="Area(Sqft.)",
        yaxis_title="Price (Crores INR)"
    )
    st.plotly_chart(fig1)


    # Sunburst Plot
    st.markdown(
        "<h3 style='text-align: center;'>Sunburst Plot of Property Data</h3>",
        unsafe_allow_html=True
    )
    input3 = st.selectbox('Property Type', ['House/Villa', 'Flat/Apartment', 'Both'], key=3)
    fig2 = px.sunburst(filterDF_SB(input3,sb_df),
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
    pieDF = filterDF_Pie(main_df)
    # Plot Pie Chart
    fig3 = px.pie(pieDF, names='bedRoom')
    st.plotly_chart(fig3)


    # BedRoom Boxplot
    st.markdown(
        "<h3 style='text-align: center;'>Bedroom Boxplot</h3>",
        unsafe_allow_html=True
    )
    boxDF, box_city = filterDF_Box(main_df)
    # Plot Boxplot
    fig4 = px.box(boxDF, x='bedRoom', y='price',
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
    kdeDF, kde_city = filterDF_KDE(main_df)
    # Plot KDE plot
    fig5 = plt.figure(figsize=(10, 5))
    sns.kdeplot(kdeDF, x='price',
                hue='property_type')
    plt.title(f'KDE Plot of Property Price in {kde_city}')
    plt.xlabel('Price(Crores INR)')
    st.pyplot(fig5)


if __name__ == "__main__":
    main()