"""Scratch file for testing reverse geolocation logic."""

import pathlib

import pandas as pd
import pandera.pandas as pa
import sqlalchemy as sa
from sqlalchemy import orm
from pandera import typing as pa_typing

from geolocation import GeolocationService, models
from pizza_platform_shared import models as shared_models

### CONFIG
# FLAGS
TO_DB = False

# PATHS
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


def create_sqlite_engine(db_path: str) -> sa.Engine:
    """Returns an sqlite engine."""
    return sa.create_engine(
        f"sqlite:///{db_path}",
        poolclass=sa.pool.StaticPool,
    )


def read_locations(engine: sa.Engine) -> pa_typing.DataFrame[LocationSchema]:
    """Get locations."""
    query = sa.select(
        shared_models.Locations.id,
        shared_models.Locations.adress,
        shared_models.Locations.country,
        shared_models.Locations.city,
        shared_models.Locations.latitude,
        shared_models.Locations.longitude,
    ).where(
        shared_models.Locations.latitude.is_not(None)
        & shared_models.Locations.longitude.is_not(None)
        & shared_models.Locations.country.is_(None)
    ).order_by(shared_models.Locations.id)

    try:
        with engine.connect() as conn:
            pizzerias_df = pd.read_sql(query, conn)
    except Exception as e:
        raise RuntimeError(f"Error reading from database: {e}") from e
    return LocationSchema.validate(pizzerias_df)


def get_reversed_geoloc(
    geo_service: GeolocationService, lat: float, lon: float
) -> models.LocationResult:
    """Returns the reversed geolocation."""
    return geo_service.reverse_geocode(lat=lat, lon=lon)


def set_reverse_geolocation():
    """Set the geolocation data based on the lat/lon coordinates in the database."""
    # create sqlite engine
    engine = create_sqlite_engine(db_path=DATABASE_PATH)

    # read all locations from the db
    locations_df = read_locations(engine=engine)

    # pass each lat/lon to the geolocation service
    geo_service = GeolocationService(user_agent="best-pizza-services/1.0")

    # loop over locations
    for i, row in locations_df.iterrows():
        reverse_location = get_reversed_geoloc(
            geo_service=geo_service,
            lat=row["latitude"],
            lon=row["longitude"],
        )

        locations_df.loc[
            i, ["country", "city"]
        ] = [
            reverse_location.country,
            reverse_location.city,
        ]

        if TO_DB:
            # Update the db row with the geolocation datas
            with orm.Session(engine) as session:
                location = session.get(shared_models.Locations, row["id"])
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
    # run all
    # set_reverse_geolocation()

    # run custom
    LAT = 50.8494279
    LON = 4.374104
    geo_loc_service = GeolocationService(user_agent="best-pizza-services/1.0")
    location_rev = get_reversed_geoloc(
            geo_service=geo_loc_service,
            lat=LAT,
            lon=LON,
        )
    print(location_rev)
