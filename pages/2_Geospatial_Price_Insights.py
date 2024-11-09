import streamlit as st
import pandas as pd
import pickle
import plotly.express as px

def load_pickle(file_path: str):
    """Load Pickle Files"""
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

def mapConfigs() -> dict:
    """Contain all coordinates and other data for plotting map"""
    # Coordinates & Zoom
    map_params = {
        # lat, long, zoom
        "Tricity": [30.698599, 76.767719, 10.4],
        "Chandigarh": [30.736744, 76.784830, 11.45],
        "Mohali": [30.699839, 76.747052, 10.4],
        "Panchkula": [30.705016, 76.877993, 11.35]
    }
    return map_params

def getInput() -> tuple:
    """Getting Input data for map"""
    input1,input2 = st.columns(2)
    with input1:
        property_type = st.selectbox('Property Type', ['House/Villa', 'Flat/Apartment'])
    with input2:
        city = st.selectbox('City', ['Tricity', 'Chandigarh', 'Mohali', 'Panchkula'])
    return property_type, city


def getPlotData(property_type: str,city: str,df: pd.DataFrame,
              map_group: pd.core.groupby.generic.DataFrameGroupBy) -> pd.DataFrame:
    """Filter Data on basis of city and property type"""
    if city == "Tricity":
        return df[df['property_type'] == property_type]
    else:
        plot_data = map_group.get_group((property_type, city))
        return plot_data


def main():
    st.set_page_config(
        page_title="Geospatial Price Insights",
        page_icon="🏠"
    )

    # Load GeoJSON and Map_data and Coordinates
    tricity_map = load_pickle('assets/geojson/sector_json.pkl')
    df = load_pickle('assets/bin/map_df.pkl')
    map_params = mapConfigs()
    
    # Grouping data for plotting for single city
    map_group = df.groupby(['property_type', 'City'])

    st.markdown(
        "<h1 style='text-align: center;'>Geospatial Price Insights</h1>",
        unsafe_allow_html=True
    )

    # Getting Input for map
    property_type, city = getInput()

    # Get Plot Data
    plot_data = getPlotData(property_type,city,df,map_group)
    
    # Ploting map
    fig = px.choropleth_mapbox(plot_data, locations="Sector", geojson=tricity_map,
                                color="price_per_sqft",
                                mapbox_style="open-street-map", color_continuous_scale="deep",
                                center={"lat": map_params[city][0], "lon": map_params[city][1]},
                                zoom=map_params[city][2],
                                width=700, height=750)
    
    # Adjusting ColorBar
    fig.update_layout(
        coloraxis_colorbar={
            'title': 'Price Per Sqft.', 'orientation': 'h', 'x': 0.5,
            'y': 1, 'xanchor': 'center', 'yanchor': 'bottom',
            'len': 1, 'thickness': 20,
        }
    )

    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()

