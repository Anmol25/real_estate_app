import streamlit as st
import pandas as pd
st.set_page_config(
    page_title="Chandigarh Tricity Real Estate Analytics App",
    page_icon="👋",
)

st.markdown(
    "<h1 style='text-align: center;'>Chandigarh Tricity Real Estate App</h1>",
    unsafe_allow_html=True
)
st.markdown("Welcome to our Home Price Prediction App, tailored specifically for the Chandigarh Tricity region. This app offers accurate property price predictions for homes across the cities of Chandigarh, Mohali, Panchkula, and nearby surrounding areas. Whether you're a buyer, seller, or investor, our app uses advanced machine learning models to provide you with reliable price estimates, helping you make data-driven decisions in the real estate market.")
st.markdown("This is the following map of Tricity:")
st.image(image="images/tricity.png")
st.sidebar.success("Select a demo above.")