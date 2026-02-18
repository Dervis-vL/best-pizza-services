"""Dataclass for coordinates."""

from __future__ import annotations

from pydantic import BaseModel

class CoordResult(BaseModel):
    """A successfully extracted coordinate pair."""
    lat: float
    lng: float

    def as_tuple(self) -> tuple[float, float]:
        return (self.lat, self.lng)

    @classmethod
    def from_tuple(cls, coordinates: tuple[float, float]) -> CoordResult:
        """Create a CoordResult object from a tuple."""
        return cls(
            lat=coordinates[0],
            lng=coordinates[1],
        )
