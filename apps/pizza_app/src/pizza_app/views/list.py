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
            rankings_df[schemas.RankingSchema.pizzeria_name]
            == row[schemas.PizzeriaSchema.slug]
        ]

        with st.container(border=True):
            name_col, rankings_col = st.columns([1, 2])

            with name_col:
                city = row[schemas.PizzeriaSchema.city]
                country = row[schemas.PizzeriaSchema.country]
                st.markdown(f"### {row[schemas.PizzeriaSchema.name].title()}")
                st.markdown(f"{city}, {country}")

            with rankings_col:
                table_rows = ""
                for category, group in pizzeria_rankings.groupby(
                    schemas.RankingSchema.category, sort=False
                ):
                    entries = list(group.itertuples())
                    for i, entry in enumerate(entries):
                        style_cell = "padding-right:1rem;vertical-align:top"
                        style_row = "padding-right:1rem;color:gray"
                        pos = (
                            f"<b>#{int(entry.position)}</b>"
                            if not pd.isna(entry.position)
                            else "—"
                        )
                        category_cell = (
                            f'<td rowspan="{len(entries)}" style="{style_cell}">'
                            f"{category}:</td>"
                            if i == 0
                            else ""
                        )
                        table_rows += (
                            f"<tr>{category_cell}"
                            f'<td style="{style_row}">{entry.year}</td>'
                            f"<td>{pos}</td></tr>"
                        )
                st.markdown(f"<table>{table_rows}</table>", unsafe_allow_html=True)
