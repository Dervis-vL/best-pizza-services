"""Streamlit app-level tests using AppTest."""

from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest


class TestApp:
    """Tests for the pizza app."""

    APP_PATH = Path(__file__).parent.parent.parent / "src" / "pizza_app" / "app.py"

    def test_app_shows_error_on_db_failure(self) -> None:
        """Test that the app shows an error and stops when the DB is unreachable."""
        # GIVEN an AppTest instance and a PizzaDataAdapter that raises on instantiation
        at = AppTest.from_file(str(self.APP_PATH))

        # WHEN the app runs with the adapter simulating a DB failure
        with patch(
            "pizza_app.infrastructure.PizzaDataAdapter",
            side_effect=RuntimeError("DB unavailable"),
        ):
            at.run()

        # THEN an error message is displayed and no exception propagates
        assert not at.exception
        assert len(at.error) > 0
