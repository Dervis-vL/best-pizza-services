"""Streamlit interactive map app of the best pizzerias."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

import streamlit as st
import folium
import pandas as pd
import sqlalchemy as sa
from folium import plugins as fo_plugins
from pandera import typing as pa_typing
from streamlit_folium import st_folium
from pizza_platform_shared import enums as shared_enums
from pizza_platform_shared import settings as shared_settings

from pizza_app import constants, repositories, schemas

ROOT_PATH = Path(__file__).parent.parent.parent
sqlite_db_path = ROOT_PATH / "test_rankings_parsing.db"
sqlite_db_path.exists()


# Page CONFIG
st.set_page_config(
    page_title="🍕 Top Pizzerias Platform",
    page_icon="🍕",
    layout="wide",
)

# Page HEADER
st.title("🍕 Pizzerias — World Map")
st.caption("Locations sourced from 50 Top Pizza rankings.")
st.write(
    "Explore the world's best pizzerias, ranked and reviewed by "
    "[50 Top Pizza](https://www.50toppizza.com). Use the sidebar filters to narrow down by year "
    "and/or category — whether you're after the global top 50, a regional list, or special awards. "
    "You might just find an acclaimed slice closer to home than you'd expect."
)

# Data LOAD
@st.cache_data(ttl=300, show_spinner="Loading Pizzerias from DB...")
def load_locations(
    db_type: shared_enums.DatabaseType
) -> pa_typing.DataFrame[schemas.PizzeriaSchema]:
    """Load data from db."""
    if db_type == shared_enums.DatabaseType.POSTGRESQL:
        pizza_repo = repositories.PizzaPlatformDatabase(
            db_settings=shared_settings.pizza_db
        )
    elif db_type == shared_enums.DatabaseType.SQLITE:
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
def load_rankings(db_type: shared_enums.DatabaseType) -> pa_typing.DataFrame[schemas.RankingSchema]:
    """Load data from db."""
    if db_type == shared_enums.DatabaseType.POSTGRESQL:
        pizza_repo = repositories.PizzaPlatformDatabase(
            db_settings=shared_settings.pizza_db
        )
    elif db_type == shared_enums.DatabaseType.SQLITE:
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
    locations_df = load_locations(shared_enums.DatabaseType.SQLITE)
    rankings_df = load_rankings(shared_enums.DatabaseType.SQLITE)
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
    st.header(constants.Filters.HEADER)
    search = st.text_input("Search by name", placeholder=constants.Filters.PLACEHOLDER)

    st.subheader(constants.Filters.YEARS)
    selected_years = []
    for year in shared_enums.Year:
        if st.checkbox(label=str(year.value), value=True, key=f"year_{year.name}"):
            selected_years.append(year.value)

    st.subheader(constants.Filters.CATEGORIES)
    selected_categories = []
    for cat in shared_enums.Categories:
        if st.checkbox(label=cat.value, value=True, key=f"cat_{cat.name}"):
            selected_categories.append(cat.value)

    st.subheader(constants.Filters.EXCELLENT_CATEGORIES)
    for cat in shared_enums.CategoriesExcellent:
        if st.checkbox(label=cat.value, value=False, key=f"cat_{cat.name}"):
            selected_categories.append(cat.value)

    st.subheader(constants.Filters.SPECIAL_AWARDS)
    for cat in shared_enums.CategoriesSpecial:
        if st.checkbox(label=cat.value, value=False, key=f"cat_{cat.name}"):
            selected_categories.append(cat.value)

filtered_rankings = rankings_df[
    rankings_df[schemas.RankingSchema.year].isin(selected_years) &
    rankings_df[schemas.RankingSchema.category].isin(selected_categories)
]
valid_names = set(filtered_rankings[schemas.RankingSchema.pizzeria_name])

if search:
    filtered = locations_df[
        locations_df[schemas.PizzeriaSchema.name].isin(valid_names) &
        locations_df[schemas.PizzeriaSchema.name].str.contains(search, case=False, na=False)
    ]
else:
    filtered = locations_df[locations_df[schemas.PizzeriaSchema.name].isin(valid_names)]


st.sidebar.metric("Showing", f"{len(filtered)} / {len(locations_df)} pizzerias")


# Folium MAP
if filtered.empty:
    avg_lat, avg_lng = 0, 0  # Default to (0,0) if no locations match filters
else:
    avg_lat = filtered[schemas.PizzeriaSchema.latitude].mean()
    avg_lng = filtered[schemas.PizzeriaSchema.longitude].mean()

m = folium.Map(
    location=[avg_lat, avg_lng],
    zoom_start=5,
    tiles="CartoDB Positron",  # Clean, light, free, no API key needed
)

# Cluster plugin keeps the map readable with many markers
cluster = fo_plugins.MarkerCluster().add_to(m)

for _, row in filtered.iterrows():
    row: pa_typing.DataFrame[schemas.PizzeriaSchema]
    pizzeria_rankings = rankings_df[
        rankings_df[schemas.RankingSchema.pizzeria_name] == row[schemas.PizzeriaSchema.name]
    ]
    results = [
        f"#{int(row.position)} of {row.category} {row.year}"
        if not pd.isna(row.position)
        else f"{row.category} {row.year}"
        for row in pizzeria_rankings.itertuples()
    ]
    folium.Marker(
        location=[row[schemas.PizzeriaSchema.latitude], row[schemas.PizzeriaSchema.longitude]],
        popup=folium.Popup(
            f"<b><ul>{"".join(f"<li>{r}</li>" for r in results)}</ul></b>", max_width=250
        ),
        tooltip=" ".join(word.capitalize() for word in row[schemas.PizzeriaSchema.name].split('-')),
        icon=folium.Icon(color="red", icon="cutlery", prefix="fa"),
    ).add_to(cluster)


# START
st_folium(m, width="stretch", height=650, returned_objects=[])

with st.expander("📋 Show all locations as table"):
    st.dataframe(filtered, width="stretch", hide_index=True)

# DISCLAIMER
st.divider()
st.caption(
    "**Disclaimer.** All ranking data displayed in this application is sourced exclusively from "
    "[50 Top Pizza](https://www.50toppizza.com) and remains the intellectual property of its "
    "respective owners. This application does not claim any rights over the data. The data has "
    "not been altered, manipulated, or editorially modified in any way — it is reproduced as "
    "published. This application is an independent, non-commercial project and is not affiliated "
    "with, endorsed by, or officially connected to 50 Top Pizza or any of its associated "
    "organisations."
)


def main() -> None:
    """Entry point — exists so the pyproject script works, but Streamlit
    must be invoked via `streamlit run`, not as a plain Python script."""

    subprocess.run(
        ["streamlit", "run", __file__, *sys.argv[1:]],
        check=True,
    )
