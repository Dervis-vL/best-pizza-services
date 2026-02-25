"""Streamlit interactive map app of the best pizzerias."""

from __future__ import annotations

from pathlib import Path

import streamlit as st
import folium
from folium import plugins as fo_plugins
from pandera import typing as pa_typing
from streamlit_folium import st_folium

from pizza_app import repositories, settings, schemas, enums

sqlite_db_path = Path(__file__).parent.parent.parent.parent / "dev" / "db" / "test_pizza_divers_data_set_two.db"
sqlite_db_path.exists()


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
def load_locations(db_type: enums.DatabaseType) -> pa_typing.DataFrame[schemas.PizzeriaSchema]:
    """Load data from db."""
    if db_type == enums.DatabaseType.POSTGRESQL:
        connection_string = settings.pizza_db.connection_string
        schema_name = settings.pizza_db.schema_name
    elif db_type == enums.DatabaseType.SQLITE:
        connection_string = f"sqlite:///{sqlite_db_path}"
        schema_name = None
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

    pizza_repo = repositories.PizzaPlatformDatabase(
        connection_string=connection_string,
        schema_name=schema_name,
    )

    return pizza_repo.read()


try:
    locations_df = load_locations(enums.DatabaseType.SQLITE)
except Exception as e:
    st.error(f"Error loading pizzeria data: {e}")
    st.stop()


if locations_df.empty:
    st.warning("No pizzerias with coordinates found in the database.")
    st.stop()


# Streamlit FILTERS
with st.sidebar:
    st.header("Filters")
    search = st.text_input("Search by name", placeholder="e.g. Pepe in Grani")

if search:
    filtered = locations_df[locations_df["name"].str.contains(search, case=False, na=False)]
else:
    filtered = locations_df

st.sidebar.metric("Showing", f"{len(filtered)} / {len(locations_df)} pizzerias")


# Folium MAP
avg_lat = filtered["latitude"].mean()
avg_lng = filtered["longitude"].mean()

m = folium.Map(
    location=[avg_lat, avg_lng],
    zoom_start=5,
    tiles="CartoDB Positron",  # Clean, light, free, no API key needed
)

# Cluster plugin keeps the map readable with many markers
cluster = fo_plugins.MarkerCluster().add_to(m)

for _, row in filtered.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=folium.Popup(f"<b>{row['name']}</b>", max_width=250),
        tooltip=row["name"],
        icon=folium.Icon(color="red", icon="cutlery", prefix="fa"),
    ).add_to(cluster)


# START
st_folium(m, width="stretch", height=650, returned_objects=[])

with st.expander("📋 Show all locations as table"):
    st.dataframe(filtered, width="stretch", hide_index=True)


def main() -> None:
    """Entry point — exists so the pyproject script works, but Streamlit
    must be invoked via `streamlit run`, not as a plain Python script."""
    import subprocess
    import sys

    subprocess.run(
        ["streamlit", "run", __file__, *sys.argv[1:]],
        check=True,
    )