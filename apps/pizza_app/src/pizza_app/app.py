"""Streamlit interactive map app of the best pizzerias."""

from __future__ import annotations

import subprocess
import sys

import streamlit as st

from pizza_app import filters as pizza_filters
from pizza_app import list as list_view
from pizza_app import map as pizza_map
from pizza_app import constants, enums, utils


# Page CONFIG
st.set_page_config(
    page_title=constants.AppContext.TAB_TITLE,
    page_icon=constants.AppContext.TAB_ICON,
    layout=constants.AppContext.LAYOUT,
)

# Page HEADER
st.title(constants.AppContext.PAGE_TITLE)
st.caption(constants.AppContext.CAPTION)
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


# FILTERS (renders sidebar, returns filtered dataframe)
filtered = pizza_filters.render_filters(locations_df, rankings_df)


# View TOGGLE
view = st.segmented_control(
    label=enums.SegmentedControl.toggle_label(),
    options=enums.SegmentedControl.values(),
    default=enums.SegmentedControl.MAP.value,
    key=enums.SegmentedControl.toggle_key(),
    bind=constants.AppContext.BIND,
    label_visibility="collapsed",
)


# Render VIEW
if view == enums.SegmentedControl.LIST:
    list_view.render_list(filtered, rankings_df)
elif view == enums.SegmentedControl.MAP:
    pizza_map.render_map(filtered, rankings_df)


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
