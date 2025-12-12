"""
Loading and basic cleaning of raw play by play data.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import pandas as pd

from ..config import RAW_DATA_DIR
from .download import DATA_DIR


def _resolve_raw_path(base_dir: Path, stem: str) -> Path:
    for ext in (".csv", ".csv.gz"):
        candidate = base_dir / f"{stem}{ext}"
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"{base_dir / (stem + '.csv')} does not exist. Download it first.")


def load_raw_season(season: int, data_dir: Path | None = None) -> pd.DataFrame:
    """
    Load a single season of raw play by play data from DATA_DIR.

    The function should:
    - Read the corresponding CSV into a DataFrame.
    - Perform minimal cleaning (standardize column names, parse datatypes).
    """
    base_dir = data_dir or DATA_DIR
    csv_path = _resolve_raw_path(base_dir, f"pbp_{season}")
    df = pd.read_csv(csv_path)
    return df


def load_raw_multiple_seasons(seasons: Iterable[int], data_dir: Path | None = None) -> pd.DataFrame:
    """
    Load and concatenate multiple seasons of raw play by play data.
    """
    frames = [load_raw_season(s, data_dir=data_dir) for s in seasons]
    return pd.concat(frames, ignore_index=True)


def load_weekly_updates(
    season: int, weeks: Sequence[int], weekly_dir: Path | None = None
) -> pd.DataFrame:
    """Load weekly play-by-play CSVs for an in-progress season.

    Files are expected under ``data/raw/weekly`` by default with the naming
    pattern ``pbp_<season>_week_<week>.csv`` or ``.csv.gz``.
    """

    base_dir = weekly_dir or (RAW_DATA_DIR / "weekly")
    frames: list[pd.DataFrame] = []
    for week in weeks:
        csv_path = _resolve_raw_path(base_dir, f"pbp_{season}_week_{week}")
        frames.append(pd.read_csv(csv_path))

    return pd.concat(frames, ignore_index=True)
