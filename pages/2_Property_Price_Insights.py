import streamlit as st
import pickle
import plotly.express as px

st.set_page_config(
    page_title="Property Price Insights",
    page_icon="🏠"
)


# Loading GeoJSON
with open('geojson/sector_json.pkl', 'rb') as file:
    tricity_map = pickle.load(file)

# Loading Map_data
with open('data/map_df.pkl', 'rb') as file:
    df = pickle.load(file)

# Coordinates & Zoom
map_params = {
    # lat, long, zoom
    "Tricity": [30.698599, 76.767719, 10.4],
    "Chandigarh": [30.736744, 76.784830, 11.45],
    "Mohali": [30.699839, 76.747052, 10.4],
    "Panchkula": [30.705016, 76.877993, 11.35]
}

map_group = df.groupby(['property_type', 'City'])

st.markdown(
    "<h1 style='text-align: center;'>Property Price Insights</h1>",
    unsafe_allow_html=True
)

# Getting Input for map
input1,input2 = st.columns(2)
with input1:
    property_type = st.selectbox('Property Type', ['House/Villa', 'Flat/Apartment'])
with input2:
    city = st.selectbox('City', ['Tricity', 'Chandigarh', 'Mohali', 'Panchkula'])

# Ploting map
if city == "Tricity":
    fig = px.choropleth_mapbox(df[df['property_type'] == property_type], locations="Sector", geojson=tricity_map,
                               color="price_per_sqft",
                               mapbox_style="open-street-map", color_continuous_scale="deep",
                               center={"lat": map_params[city][0], "lon": map_params[city][1]},
                               zoom=map_params[city][2],
                               width=700, height=750)

else:
    plot_data = map_group.get_group((property_type, city))
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
