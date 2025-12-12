"""
Functions to download and store public NFL play by play data.

This module defines utilities to place CSV files in ``data/raw``. The default
``download_season`` is left as a TODO because the project intentionally avoids
shipping a brittle or rate-limited source—swap in your preferred public
endpoint (e.g., nflfastR exports) and keep it fully unauthenticated.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable
import requests

from ..config import RAW_DATA_DIR

DATA_DIR = RAW_DATA_DIR


def ensure_data_dir() -> None:
    """Create the raw data directory if it does not already exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def download_season(season: int) -> Path:
    """
    Download play by play data for a given season into DATA_DIR.

    Returns the local path to the downloaded CSV.
    """
    ensure_data_dir()
    # TODO: Wire this to a stable public CSV source (e.g., nflfastR exports on GitHub).
    # Example approach (to be customized):
    # url = f"https://github.com/nflverse/nflfastR-data/blob/master/data/pbp_{season}.csv.gz?raw=1"
    # response = requests.get(url, timeout=30)
    # response.raise_for_status()
    # target = DATA_DIR / f"pbp_{season}.csv.gz"
    # target.write_bytes(response.content)
    # return target
    raise NotImplementedError("Implement download_season with a real public CSV source")


def download_multiple_seasons(seasons: Iterable[int]) -> list[Path]:
    """
    Download multiple seasons of data.

    Returns a list of CSV paths.
    """
    paths: list[Path] = []
    for season in seasons:
        paths.append(download_season(season))
    return paths
