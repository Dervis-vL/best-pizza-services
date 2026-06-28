"""CLI driving adapter; assembles worker Typer app."""

import logging

import typer

from pizza_worker import settings
from pizza_worker.cli.run_pending import run_pending

app = typer.Typer(help="Pizza platform batch worker.", no_args_is_help=True)

app.command(name="run-pending")(run_pending)


@app.callback()
def _configure() -> None:
    """Configure logging once before any command runs."""
    logging.basicConfig(
        level=settings.worker.log_level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
