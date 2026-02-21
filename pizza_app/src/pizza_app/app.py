"""Streamlit interactive map app of the best pizzerias."""

from __future__ import annotations

import streamlit as st
import folium
from streamlit_folium import st_folium

from pizza_app import repositories, settings


# Page CONFIG
st.set_page_config(
    page_title="🍕 Top Pizzerias Platform",
    page_icon="🍕",
    layout="wide",
)

st.title("🍕 Pizzerias — World Map")
st.caption("Locations sourced from 50 Top Pizza rankings.")