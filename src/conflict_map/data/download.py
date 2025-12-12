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
    url = f"https://github.com/nflverse/nflverse-data/releases/download/pbp/pbp_{season}.csv.gz"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    target = DATA_DIR / f"pbp_{season}.csv.gz"
    target.write_bytes(response.content)
    return target


def download_multiple_seasons(seasons: Iterable[int]) -> list[Path]:
    """
    Download multiple seasons of data.

    Returns a list of CSV paths.
    """
    paths: list[Path] = []
    for season in seasons:
        paths.append(download_season(season))
    return paths


def download_weekly(season: int, week: int) -> Path:
    """Download a single week of play by play into ``data/raw/weekly``.

    This keeps in-progress seasons lightweight while still enabling the
    weekly update pipeline. The nflverse weekly exports follow the naming
    convention ``pbp_<season>_week_<week>.csv.gz`` under the pbp_weekly release.
    """

    weekly_dir = DATA_DIR / "weekly"
    weekly_dir.mkdir(parents=True, exist_ok=True)
    url = f"https://github.com/nflverse/nflverse-data/releases/download/pbp_weekly/pbp_{season}_week_{week}.csv.gz"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    target = weekly_dir / f"pbp_{season}_week_{week}.csv.gz"
    target.write_bytes(response.content)
    return target
