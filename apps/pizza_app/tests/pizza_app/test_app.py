"""Streamlit app-level tests using AppTest."""

from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

APP_PATH = Path(__file__).parent.parent.parent / "src" / "pizza_app" / "app.py"


def test_app_shows_error_on_db_failure() -> None:
    """Test that the app shows an error and stops when the DB is unreachable."""
    # GIVEN a repo that raises on data load
    at = AppTest.from_file(str(APP_PATH))

    with patch("pizza_app.utils.create_repo", side_effect=RuntimeError("DB unavailable")):
        # WHEN the app runs
        at.run()

    # THEN an error message is displayed and no exception propagates
    assert not at.exception
    assert len(at.error) > 0
