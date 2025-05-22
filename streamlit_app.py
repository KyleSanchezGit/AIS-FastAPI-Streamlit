import os
import requests
import pandas as pd
import streamlit as st
import pydeck as pdk
from dotenv import load_dotenv

st.title("AIS FastAPI Streamlit")
st.write(
    "A map display based on locally hosted Docker container running FastAPI. Data is fetched from a remote API. The map is interactive and can be filtered by number of records. Source code: https://github.com/ksubc/AIS-FastAPI-Streamlit."
)

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000/vessels/")

st.set_page_config(page_title="AIS Map", layout="wide")
st.title("🗺️ AIS Vessel Tracker")

# Sidebar controls
limit = st.sidebar.slider("Number of records", 10, 1000, 200)

# Fetch data
resp = requests.get(API_URL, params={"limit": limit})
resp.raise_for_status()
data = resp.json()
df = pd.DataFrame(data)

if df.empty:
    st.warning("No data to display")
    st.stop()

st.subheader("Raw Data")
st.dataframe(df)

# Map
st.subheader("Vessel Positions")
df = df.dropna(subset=["latitude", "longitude"])
midpoint = (df["latitude"].mean(), df["longitude"].mean())

deck = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=midpoint[0], longitude=midpoint[1], zoom=6, pitch=30
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position="[longitude, latitude]",
            get_radius=500,
            get_fill_color="[200, 30, 0, 140]",
        )
    ],
)
st.pydeck_chart(deck)



