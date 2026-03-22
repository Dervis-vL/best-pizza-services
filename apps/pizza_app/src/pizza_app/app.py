"""Streamlit interactive map app of the best pizzerias."""

from __future__ import annotations

import subprocess
import sys

import streamlit as st

from pizza_app import (
    infrastructure,
    constants,
    dataclasses,
    enums,
    utils,
    views,
)


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
    pizza_adapter = infrastructure.PizzaDataAdapter(repo=utils.create_repo())
    pizza_data: dataclasses.PizzaData = pizza_adapter.load_pizza_data()
except Exception as e:  # pylint: disable=broad-exception-caught
    st.error(f"Error loading pizzeria data: {e}")
    st.stop()


# FILTERS (renders sidebar, returns filtered dataframe)
filtered = views.render_filters(pizza_data.locations, pizza_data.rankings)


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
    views.render_list(filtered, pizza_data.rankings)
elif view == enums.SegmentedControl.MAP:
    views.render_map(filtered, pizza_data.rankings)


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
