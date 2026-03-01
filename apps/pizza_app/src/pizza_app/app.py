"""Streamlit interactive map app of the best pizzerias."""

from __future__ import annotations

from pathlib import Path

import streamlit as st
import folium
import pandas as pd
import sqlalchemy as sa
from folium import plugins as fo_plugins
from pandera import typing as pa_typing
from streamlit_folium import st_folium

from pizza_app import repositories, settings, schemas, enums

ROOT_PATH = Path(__file__).parent.parent.parent
sqlite_db_path = ROOT_PATH / "test_rankings_parsing.db"
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
        pizza_repo = repositories.PizzaPlatformDatabase(
            db_settings=settings.pizza_db
        )
    elif db_type == enums.DatabaseType.SQLITE:
        pizza_repo = repositories.PizzaPlatformDatabase.from_engine(
            engine=sa.create_engine(
                f"sqlite:///{sqlite_db_path}",
                poolclass=sa.pool.StaticPool,
            ),
        )
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

    return pizza_repo.read_pizzerias()


@st.cache_data(ttl=300, show_spinner="Loading Rankings from DB...")
def load_rankings(db_type: enums.DatabaseType) -> pa_typing.DataFrame[schemas.RankingSchema]:
    """Load data from db."""
    if db_type == enums.DatabaseType.POSTGRESQL:
        pizza_repo = repositories.PizzaPlatformDatabase(
            db_settings=settings.pizza_db
        )
    elif db_type == enums.DatabaseType.SQLITE:
        pizza_repo = repositories.PizzaPlatformDatabase.from_engine(
            engine=sa.create_engine(
                f"sqlite:///{sqlite_db_path}",
                poolclass=sa.pool.StaticPool,
            ),
        )
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

    return pizza_repo.read_rankings()


try:
    locations_df = load_locations(enums.DatabaseType.SQLITE)
    rankings_df = load_rankings(enums.DatabaseType.SQLITE)
except Exception as e:  # pylint: disable=broad-exception-caught
    st.error(f"Error loading pizzeria data: {e}")
    st.stop()

if locations_df.empty:
    st.warning("No pizzerias with coordinates found in the database.")
    st.stop()

if rankings_df.empty:
    st.warning("No pizzeria rankings found in the database.")
    st.stop()


# Streamlit FILTERS
with st.sidebar:
    st.header("Filters")
    search = st.text_input("Search by name", placeholder="e.g. Pepe in Grani")

    # TODO: filter by year (with check box for every year present in the data)

    # TODO: filter by category (with check box for every category present in the data))

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
    name = " ".join(word.capitalize() for word in row["name"].split('-'))
    pizzeria_rankings = rankings_df[rankings_df["pizzeria_name"] == row["name"]]
    results = [
        f"#{int(row.position)} of {row.category} {row.year}"
        if not pd.isna(row.position)
        else f"{row.category} {row.year}"
        for row in pizzeria_rankings.itertuples()
    ]
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=folium.Popup(f"<b><ul>{"".join(f"<li>{r}</li>" for r in results)}</ul></b>", max_width=250),
        tooltip=name,
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
