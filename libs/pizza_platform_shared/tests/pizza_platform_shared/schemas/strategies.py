"""Hypothesis strategies shared across schema tests."""

from hypothesis import strategies as st


def st_optional_text(max_size: int) -> st.SearchStrategy[str | None]:
    """Optional text field up to max_size characters."""
    return st.one_of(st.none(), st.text(max_size=max_size))


def st_finite_float() -> st.SearchStrategy[float]:
    """Finite float — no NaN or infinity."""
    return st.floats(allow_nan=False, allow_infinity=False)


def st_optional_float() -> st.SearchStrategy[float | None]:
    """Optional finite float."""
    return st.one_of(st.none(), st_finite_float())
