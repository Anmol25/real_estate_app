import streamlit as st
import pandas as pd
import json
import plotly.express as px

def load_data() -> tuple:
    """Load geojson of map boundaries and create datapoints for plotting"""
    map = json.load(open("assets/geojson/tricity.geojson", "r"))
    df = {
        "City": ["Chandigarh", "Panchkula", "Mohali (incl. adj areas)"],
        "id": ["Chandigarh", "Panchkula", "Mohali"]
    }
    df = pd.DataFrame(df)
    return map, df


def main():
    # load map data
    tricity_map = load_data()[0]
    tricity_df = load_data()[1]

    st.set_page_config(
        page_title="Chandigarh Tricity Real Estate App",
        page_icon="🏠"
    )

    # Page Heading
    st.markdown(
        "<h1 style='text-align: center;'>Chandigarh Tricity Real Estate App</h1>",
        unsafe_allow_html=True
    )

    # introduction
    st.markdown("Welcome to our Home Price Prediction App, tailored specifically for the Chandigarh Tricity region. This "
                "app offers accurate property price predictions for homes across the cities of Chandigarh, Mohali, "
                "Panchkula, and nearby surrounding areas. Whether you're a buyer, seller, or investor, our app uses "
                "advanced machine learning models to provide you with reliable price estimates, helping you make "
                "data-driven decisions in the real estate market.")

    # Plot Map
    st.markdown(
        "<h3 style='text-align: center;'>Map of Tricity</h3>",
        unsafe_allow_html=True
    )
    
    fig = px.choropleth_mapbox(tricity_df, locations="id", geojson=tricity_map, color="City",
                            mapbox_style="open-street-map", center={"lat": 30.689281, "lon": 76.786950},
                            featureidkey="properties.Name", width=700, height=700,
                            zoom=10.25, opacity=0.5, color_discrete_sequence=["red", "yellow", "blue"])
    
    fig.update_traces(
        marker_line_width=2,
        marker_line_color='black'
    )

    fig.update_layout(
        legend=dict(
            orientation="h", yanchor="bottom", y=1,
            xanchor="center", x=0.5
        )
    )

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()