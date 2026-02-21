"""Streamlit interactive map app of the best pizzerias."""

from __future__ import annotations

import streamlit as st
import folium
from pandera import typing as pa_typing
from streamlit_folium import st_folium

from pizza_app import repositories, settings, schemas


# Page CONFIG
st.set_page_config(
    page_title="🍕 Top Pizzerias Platform",
    page_icon="🍕",
    layout="wide",
)

st.title("🍕 Pizzerias — World Map")
st.caption("Locations sourced from 50 Top Pizza rankings.")

# Data LOAD
@st.cache_data(ttl=300, show_spinner="Loading Pizzerias from DB...")
def load_locations() -> pa_typing.DataFrame[schemas.PizzeriaSchema]:
    """Load data from db."""
    pizza_repo = repositories.PizzaPlatformDatabase(settings=settings.pizza_db)
    return pizza_repo.read()