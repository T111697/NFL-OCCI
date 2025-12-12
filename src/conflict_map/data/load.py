"""
Loading and basic cleaning of raw play by play data.
"""
from __future__ import annotations

from typing import Iterable
import pandas as pd

from .download import DATA_DIR


def load_raw_season(season: int) -> pd.DataFrame:
    """
    Load a single season of raw play by play data from DATA_DIR.

    The function should:
    - Read the corresponding CSV into a DataFrame.
    - Perform minimal cleaning (standardize column names, parse datatypes).
    """
    csv_path = DATA_DIR / f"pbp_{season}.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"{csv_path} does not exist. Download it first.")
    df = pd.read_csv(csv_path)
    return df


def load_raw_multiple_seasons(seasons: Iterable[int]) -> pd.DataFrame:
    """
    Load and concatenate multiple seasons of raw play by play data.
    """
    frames = [load_raw_season(s) for s in seasons]
    return pd.concat(frames, ignore_index=True)
