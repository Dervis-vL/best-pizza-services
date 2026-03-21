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
st.write(constants.AppContext.HEADER)

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
    bind=constants.QueryParam.BIND,
    label_visibility="collapsed",
)


# Render VIEW
if view == enums.SegmentedControl.LIST:
    list_view.render_list(filtered, rankings_df)
elif view == enums.SegmentedControl.MAP:
    pizza_map.render_map(filtered, rankings_df)


# DISCLAIMER
st.divider()
st.caption(constants.AppContext.DISCLAIMER)


def main() -> None:
    """Entry point; exists so the pyproject script works, but Streamlit
    must be invoked via `streamlit run`, not as a plain Python script."""

    subprocess.run(
        ["streamlit", "run", __file__, *sys.argv[1:]],
        check=True,
    )
