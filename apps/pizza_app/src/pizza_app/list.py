"""List view module for displaying pizzerias as cards."""

from __future__ import annotations

import pandas as pd
import streamlit as st
from pandera import typing as pa_typing

from pizza_app import schemas


def render_list(
    filtered: pa_typing.DataFrame[schemas.PizzeriaSchema],
    rankings_df: pa_typing.DataFrame[schemas.RankingSchema],
) -> None:
    """Render each pizzeria as a card with location and ranking details."""

    if filtered.empty:
        st.info("No pizzerias match the current filters.")
        return

    for _, row in filtered.iterrows():
        pizzeria_rankings = rankings_df[
            rankings_df[schemas.RankingSchema.pizzeria_name] == row[schemas.PizzeriaSchema.slug]
        ]

        with st.container(border=True):
            name_col, rankings_col = st.columns([1, 2])

            with name_col:
                st.markdown(f"### {row[schemas.PizzeriaSchema.name].title()}")
                st.markdown(
                    f"{row[schemas.PizzeriaSchema.city]}, {row[schemas.PizzeriaSchema.country]}"
                )

            with rankings_col:
                for ranking_row in pizzeria_rankings.itertuples():
                    if not pd.isna(ranking_row.position):
                        label = f"**#{int(ranking_row.position)}** {ranking_row.category} {ranking_row.year}"
                    else:
                        label = f"{ranking_row.category} {ranking_row.year}"
                    st.markdown(f"- {label}")
