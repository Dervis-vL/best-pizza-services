"""Smoke test: the package imports and knows its version."""

import pizza_data_stats


def test_version() -> None:
    """Dummy test."""
    assert pizza_data_stats.__version__
