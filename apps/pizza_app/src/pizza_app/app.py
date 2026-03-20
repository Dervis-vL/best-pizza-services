"""Streamlit interactive map app of the best pizzerias."""

from __future__ import annotations

import subprocess
import sys

import streamlit as st
import folium
import pandas as pd
from folium import plugins as fo_plugins
from pandera import typing as pa_typing
from streamlit_folium import st_folium
from pizza_platform_shared import enums as shared_enums

from pizza_app import constants, schemas, utils


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

# READ data
try:
    repo = utils.create_repo()
    locations_df = utils.load_locations(_db_repo=repo)
    rankings_df = utils.load_rankings(_db_repo=repo)
except Exception as e:  # pylint: disable=broad-exception-caught
    st.error(f"Error loading pizzeria data: {e}")
    st.stop()

if locations_df.empty:
    st.warning("No pizzerias with coordinates found in the database.")
    st.stop()

if rankings_df.empty:
    st.warning("No pizzeria rankings found in the database.")
    st.stop()


# Session state initialization
if "selected_country" not in st.session_state:
    st.session_state["selected_country"] = "All"
if "selected_city" not in st.session_state:
    st.session_state["selected_city"] = "All"


# Streamlit FILTERS
with st.sidebar:
    st.header(constants.Filters.HEADER)
    search = st.text_input("Search by name", placeholder=constants.Filters.PLACEHOLDER)

    pre_years = [
        year.value for year in shared_enums.Year
        if st.session_state.get(f"year_{year.name}", True)
    ]
    pre_categories = (
        [cat.value for cat in shared_enums.Categories if st.session_state.get(
            f"cat_{cat.name}", True
        )] +
        [cat.value for cat in shared_enums.CategoriesExcellent if st.session_state.get(
            f"cat_{cat.name}", False
        )] +
        [cat.value for cat in shared_enums.CategoriesSpecial if st.session_state.get(
            f"cat_{cat.name}", False
        )]
    )
    pre_valid_names = set(
        rankings_df[
            rankings_df[schemas.RankingSchema.year].isin(pre_years) &
            rankings_df[schemas.RankingSchema.category].isin(pre_categories)
        ][schemas.RankingSchema.pizzeria_name]
    )
    relevant_locations = locations_df[
        locations_df[schemas.PizzeriaSchema.name].isin(pre_valid_names)
    ]

    countries = sorted(
        relevant_locations[schemas.PizzeriaSchema.country].dropna().unique().tolist()
    )
    selected_country = st.selectbox(
        "Search by country",
        options=["All"] + countries,
        key="selected_country",
        on_change=utils.on_country_change,
        bind="query-params",
    )

    if st.session_state["selected_country"] != "All":
        city_pool = relevant_locations[
            relevant_locations[
                schemas.PizzeriaSchema.country
            ] == st.session_state["selected_country"]
        ]
    else:
        city_pool = relevant_locations

    cities = sorted(city_pool[schemas.PizzeriaSchema.city].dropna().unique().tolist())
    selected_city = st.selectbox(
        "Search by city",
        options=["All"] + cities,
        key="selected_city",
        on_change=utils.make_on_city_change(
            relevant_locations=relevant_locations,
            city_col=schemas.PizzeriaSchema.city,
            country_col=schemas.PizzeriaSchema.country,
        ),
        bind="query-params",
    )

    st.subheader(constants.Filters.YEARS)
    selected_years = []
    for year in shared_enums.Year:
        if st.checkbox(
            label=str(year.value), value=True, key=f"year_{year.name}", bind="query-params"
        ):
            selected_years.append(year.value)

    st.subheader(constants.Filters.CATEGORIES)
    selected_categories = []
    for cat in shared_enums.Categories:
        if st.checkbox(
            label=cat.value, value=True, key=f"cat_{cat.name}", bind="query-params"
        ):
            selected_categories.append(cat.value)

    st.subheader(constants.Filters.EXCELLENT_CATEGORIES)
    for cat in shared_enums.CategoriesExcellent:
        if st.checkbox(
            label=cat.value, value=False, key=f"cat_{cat.name}", bind="query-params"
        ):
            selected_categories.append(cat.value)

    st.subheader(constants.Filters.SPECIAL_AWARDS)
    for cat in shared_enums.CategoriesSpecial:
        if st.checkbox(
            label=cat.value, value=False, key=f"cat_{cat.name}", bind="query-params"
        ):
            selected_categories.append(cat.value)


filtered_rankings = rankings_df[
    rankings_df[schemas.RankingSchema.year].isin(selected_years) &
    rankings_df[schemas.RankingSchema.category].isin(selected_categories)
]
valid_names = set(filtered_rankings[schemas.RankingSchema.pizzeria_name])

country_mask = (
    (locations_df[schemas.PizzeriaSchema.country] == selected_country)
    if selected_country != "All"
    else True
)

city_mask = (
    (locations_df[schemas.PizzeriaSchema.city] == selected_city)
    if selected_city != "All"
    else True
)

if search:
    filtered = locations_df[
        locations_df[schemas.PizzeriaSchema.name].isin(valid_names) &
        locations_df[schemas.PizzeriaSchema.name].str.contains(search, case=False, na=False) &
        country_mask &
        city_mask
    ]
else:
    filtered = locations_df[
        locations_df[schemas.PizzeriaSchema.name].isin(valid_names) &
        country_mask &
        city_mask
    ]

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
