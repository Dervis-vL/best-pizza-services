"""Tests root level fixtures for the pizza app."""

from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / "vars.env")
