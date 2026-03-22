"""Scratch file for testing reverse geolocation logic."""

import pathlib

import pandas as pd
import pandera.pandas as pa
import sqlalchemy as sa
from sqlalchemy import orm
from pandera import typing as pa_typing

from geolocation import GeolocationService
from pizza_platform_shared import models

ROOT_DIR = pathlib.Path(__file__).parent
DATABASE_PATH = ROOT_DIR / "test_rankings_parsing.db"


class LocationSchema(pa.DataFrameModel):
    """Validates a DataFrame of pizzerias that have known coordinates.

    Columns:
        id: Display name of the pizzeria.
        address: The address matching the coordinates
        city: The city matching the coordinates
        country: The country matching the coordinates
        lat:  Latitude, must be within valid geographic range.
        lng:  Longitude, must be within valid geographic range.
    """

    id: pa_typing.Series[int] = pa.Field(nullable=False, ge=1)
    adress: pa_typing.Series[str] = pa.Field(nullable=True)
    city: pa_typing.Series[str] = pa.Field(nullable=True)
    country: pa_typing.Series[str] = pa.Field(nullable=True)
    latitude: pa_typing.Series[float] = pa.Field(nullable=False, ge=-90, le=90)
    longitude: pa_typing.Series[float] = pa.Field(nullable=False, ge=-180, le=180)

    class Config:  # pylint: disable=too-few-public-methods
        """Config."""
        strict = True
        coerce = True
        name = "LocationSchema"


def set_reverse_geolocation():
    """Set the geolocation data based on the lat/lon coordinates in the database."""
    # create sqlite engine
    engine = sa.create_engine(
        f"sqlite:///{DATABASE_PATH}",
        poolclass=sa.pool.StaticPool,
    )

    # Create read locations query function
    def read_locations(engine: sa.Engine) -> pa_typing.DataFrame[LocationSchema]:
        """Get locations."""
        query = sa.select(
            models.Locations.id,
            models.Locations.adress,
            models.Locations.country,
            models.Locations.city,
            models.Locations.latitude,
            models.Locations.longitude,
        ).where(
            models.Locations.latitude.is_not(None)
            & models.Locations.longitude.is_not(None)
            & models.Locations.country.is_(None)
        ).order_by(models.Locations.id)

        try:
            with engine.connect() as conn:
                pizzerias_df = pd.read_sql(query, conn)
        except Exception as e:
            raise RuntimeError(f"Error reading from database: {e}") from e
        return LocationSchema.validate(pizzerias_df)


    # read all locations from the db
    locations_df = read_locations(engine=engine)

    # pass each lat/lon to the geolocation service
    geo_service = GeolocationService(user_agent="best-pizza-services/1.0")

    # loop over locations
    for i, row in locations_df.iterrows():
        reverse_location = geo_service.reverse_geocode(
            lat=row["latitude"],
            lon=row["longitude"],
        )

        locations_df.loc[
            i, ["country", "city"]
        ] = [
            reverse_location.country,
            reverse_location.city,
        ]

        # Update the db row with the geolocation datas
        with orm.Session(engine) as session:
            location = session.get(models.Locations, row["id"])
            if location:
                now = sa.func.now()  # pylint: disable=not-callable
                location.updated_at = now
                location.city = reverse_location.city
                location.country = reverse_location.country
                session.commit()
            else:
                msg = f"RankingEdition with id {row["id"]} not found."
                raise ValueError(msg)


if __name__ == "__main__":
    set_reverse_geolocation()
