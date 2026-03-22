"""Map module containing building and marker logic."""

from __future__ import annotations

import folium
import pandas as pd
from folium import plugins as fo_plugins
from pandera import typing as pa_typing
from streamlit_folium import st_folium

from pizza_app import schemas


def render_map(
    filtered: pa_typing.DataFrame[schemas.PizzeriaSchema],
    rankings_df: pa_typing.DataFrame[schemas.RankingSchema],
) -> None:
    """Build and render the Folium pizzeria map."""

    if filtered.empty:
        avg_lat, avg_lng = 0, 0
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
            rankings_df[schemas.RankingSchema.pizzeria_name] == row[schemas.PizzeriaSchema.slug]
        ]
        table_rows = ""
        for category, group in pizzeria_rankings.groupby(
            schemas.RankingSchema.category, sort=False
        ):
            entries = list(group.itertuples())
            for i, entry in enumerate(entries):
                pos = f"#{int(entry.position)}" if not pd.isna(entry.position) else "—"
                category_cell = (
                    f'<td rowspan="{len(entries)}" style="padding-right:8px;vertical-align:top">'
                    f"<b>{category}:</b></td>"
                    if i == 0
                    else ""
                )
                table_rows += (
                    f"<tr>{category_cell}"
                    f'<td style="padding-right:8px">{entry.year}</td>'
                    f"<td>{pos}</td></tr>"
                )
        folium.Marker(
            location=[row[schemas.PizzeriaSchema.latitude], row[schemas.PizzeriaSchema.longitude]],
            popup=folium.Popup(f"<table>{table_rows}</table>", max_width=300),
            tooltip=row[schemas.PizzeriaSchema.name],
            icon=folium.Icon(color="red", icon="cutlery", prefix="fa"),
        ).add_to(cluster)

    st_folium(m, width="stretch", height=650, returned_objects=[])
