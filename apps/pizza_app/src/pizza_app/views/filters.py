"""All Streamlit app related filters logic."""

from __future__ import annotations

import streamlit as st
from pandera import typing as pa_typing

from pizza_app import constants, schemas, utils
from pizza_platform_shared import enums as shared_enums


def render_filters(
    locations_df: pa_typing.DataFrame[schemas.PizzeriaSchema],
    rankings_df: pa_typing.DataFrame[schemas.RankingSchema],
) -> pa_typing.DataFrame[schemas.PizzeriaSchema]:
    """Render the sidebar filters and return the filtered pizzerias dataframe."""
    if constants.QueryParam.COUNTRY not in st.session_state:
        st.session_state[constants.QueryParam.COUNTRY] = constants.Filters.DEFAULT
    if constants.QueryParam.CITY not in st.session_state:
        st.session_state[constants.QueryParam.CITY] = constants.Filters.DEFAULT

    with st.sidebar:
        st.header(constants.Filters.HEADER)
        search = st.text_input(
            "Search by name",
            placeholder=constants.Filters.PLACEHOLDER,
        )

        pre_years = [
            year.value
            for year in shared_enums.Year
            if st.session_state.get(f"{constants.QueryParam.YEAR}{year.value!s}", True)
        ]
        pre_categories = (
            [
                cat.value
                for cat in shared_enums.Categories
                if st.session_state.get(
                    f"{constants.QueryParam.CATEGORY}{cat.name}",
                    True,
                )
            ]
            + [
                cat.value
                for cat in shared_enums.CategoriesExcellent
                if st.session_state.get(
                    f"{constants.QueryParam.CATEGORY}{cat.name}",
                    False,
                )
            ]
            + [
                cat.value
                for cat in shared_enums.CategoriesSpecial
                if st.session_state.get(
                    f"{constants.QueryParam.CATEGORY}{cat.name}",
                    False,
                )
            ]
        )
        pre_valid_names = set(
            rankings_df[
                rankings_df[schemas.RankingSchema.year].isin(pre_years)
                & rankings_df[schemas.RankingSchema.category].isin(pre_categories)
            ][schemas.RankingSchema.pizzeria_name],
        )
        relevant_locations = locations_df[
            locations_df[schemas.PizzeriaSchema.slug].isin(pre_valid_names)
        ]

        countries = sorted(
            relevant_locations[schemas.PizzeriaSchema.country].dropna().unique().tolist(),
        )
        selected_country = st.selectbox(
            "Search by country",
            options=[constants.Filters.DEFAULT, *countries],
            key=constants.QueryParam.COUNTRY,
            on_change=utils.on_country_change,
            bind=constants.QueryParam.BIND,
        )

        if st.session_state[constants.QueryParam.COUNTRY] != constants.Filters.DEFAULT:
            city_pool = relevant_locations[
                relevant_locations[schemas.PizzeriaSchema.country]
                == st.session_state[constants.QueryParam.COUNTRY]
            ]
        else:
            city_pool = relevant_locations

        cities = sorted(
            city_pool[schemas.PizzeriaSchema.city].dropna().unique().tolist(),
        )
        selected_city = st.selectbox(
            "Search by city",
            options=[constants.Filters.DEFAULT, *cities],
            key=constants.QueryParam.CITY,
            on_change=utils.make_on_city_change(
                relevant_locations=relevant_locations,
                city_col=schemas.PizzeriaSchema.city,
                country_col=schemas.PizzeriaSchema.country,
            ),
            bind=constants.QueryParam.BIND,
        )

        st.subheader(constants.Filters.YEARS)
        selected_years = [
            year.value
            for year in shared_enums.Year
            if st.checkbox(
                label=str(year.value),
                value=True,
                key=f"{constants.QueryParam.YEAR}{year.value!s}",
                bind=constants.QueryParam.BIND,
            )
        ]

        st.subheader(constants.Filters.CATEGORIES)
        selected_categories = [
            cat.value
            for cat in shared_enums.Categories
            if st.checkbox(
                label=cat.value,
                value=True,
                key=f"{constants.QueryParam.CATEGORY}{cat.name}",
                bind=constants.QueryParam.BIND,
            )
        ]

        st.subheader(constants.Filters.EXCELLENT_CATEGORIES)
        for cat in shared_enums.CategoriesExcellent:
            if st.checkbox(
                label=cat.value,
                value=False,
                key=f"{constants.QueryParam.CATEGORY}{cat.name}",
                bind=constants.QueryParam.BIND,
            ):
                selected_categories.append(cat.value)  # noqa: PERF401

        st.subheader(constants.Filters.SPECIAL_AWARDS)
        for cat in shared_enums.CategoriesSpecial:
            if st.checkbox(
                label=cat.value,
                value=False,
                key=f"{constants.QueryParam.CATEGORY}{cat.name}",
                bind=constants.QueryParam.BIND,
            ):
                selected_categories.append(cat.value)  # noqa: PERF401

    filtered_rankings = rankings_df[
        rankings_df[schemas.RankingSchema.year].isin(selected_years)
        & rankings_df[schemas.RankingSchema.category].isin(selected_categories)
    ]
    valid_names = set(filtered_rankings[schemas.RankingSchema.pizzeria_name])

    country_mask = (
        (locations_df[schemas.PizzeriaSchema.country] == selected_country)
        if selected_country != constants.Filters.DEFAULT
        else True
    )

    city_mask = (
        (locations_df[schemas.PizzeriaSchema.city] == selected_city)
        if selected_city != constants.Filters.DEFAULT
        else True
    )

    if search:
        filtered = locations_df[
            locations_df[schemas.PizzeriaSchema.slug].isin(valid_names)
            & locations_df[schemas.PizzeriaSchema.slug].str.contains(
                search,
                case=False,
                na=False,
            )
            & country_mask
            & city_mask
        ]
    else:
        filtered = locations_df[
            locations_df[schemas.PizzeriaSchema.slug].isin(valid_names) & country_mask & city_mask
        ]

    st.sidebar.metric("Showing", f"{len(filtered)} / {len(locations_df)} pizzerias")

    return filtered
