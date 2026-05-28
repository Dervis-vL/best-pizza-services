"""Base schemas for the pizza app, including mixins."""

import pandas as pd
import pydantic as pyd


class FromParentMixin:
    """Mixin for Pandera DataFrameModels that are populated from a parent model's relationship."""

    @classmethod
    def from_parent(
        cls,
        parents: pyd.BaseModel | list[pyd.BaseModel],
        relationship: str,
        fk_field: str,
        pk_field: str = "id",
    ) -> pd.DataFrame:
        """Create a DataFrame from a parent (pydantic) model's relationship."""
        if isinstance(parents, pyd.BaseModel):
            parents = [parents]

        records = [
            {**child.model_dump(), fk_field: getattr(parent, pk_field)}
            for parent in parents
            for child in getattr(parent, relationship)
        ]
        return cls.validate(pd.DataFrame(records))  # type: ignore[attr-defined]"
