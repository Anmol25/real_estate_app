import streamlit as st
import pandas as pd
import json
import plotly.express as px


st.set_page_config(
    page_title="Chandigarh Tricity Real Estate Analytics App",
    page_icon="👋",
)

st.markdown(
    "<h1 style='text-align: center;'>Chandigarh Tricity Real Estate App</h1>",
    unsafe_allow_html=True
)
# introduction
st.markdown("Welcome to our Home Price Prediction App, tailored specifically for the Chandigarh Tricity region. This app offers accurate property price predictions for homes across the cities of Chandigarh, Mohali, Panchkula, and nearby surrounding areas. Whether you're a buyer, seller, or investor, our app uses advanced machine learning models to provide you with reliable price estimates, helping you make data-driven decisions in the real estate market.")

# Map
st.markdown(
    "<h3 style='text-align: center;'>Map of Tricity</h3>",
    unsafe_allow_html=True
)
tricity_map = json.load(open("geojson/tricity.geojson","r"))
tricity_df = {
    "City" : ["Chandigarh","Panchkula","Mohali (incl. adj areas)"],
    "id" : ["Chandigarh","Panchkula","Mohali"]
}
tricity_df = pd.DataFrame(tricity_df)
fig = px.choropleth_mapbox(tricity_df,locations="id",geojson=tricity_map,color="City",
                           mapbox_style="open-street-map", center = {"lat":30.689281,"lon":76.786950}, featureidkey="properties.Name",width=700,height=700,
                          zoom = 10.25,opacity=0.3,color_discrete_sequence=["red", "yellow", "blue"])
fig.update_traces(
    marker_line_width=2,
    marker_line_color='black'
)

st.plotly_chart(fig,use_container_width=True)