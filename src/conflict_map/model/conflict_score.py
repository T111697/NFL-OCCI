"""
Computation of play level conflict scores.

This module exposes:
- compute_conflict_score_row: pure function from row -> float.
- compute_conflict_scores: vectorized function over a DataFrame.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def compute_conflict_score_row(row: pd.Series) -> float:
    """
    Compute a heuristic conflict score for a single play.

    The score should be in [0, 1] and combine:
    - Structural complexity (motion, play action, personnel).
    - Situation leverage (3rd down, red zone).
    - Defensive stress hints (penalties).
    - Offensive success proxy (epa or first down).

    This is a heuristic on public data, not a ground truth measurement.
    """
    score = 0.0

    if bool(row.get("has_motion", False)):
        score += 0.15
    if bool(row.get("has_play_action", False)):
        score += 0.15

    num_receivers = float(row.get("num_te", 0)) + float(row.get("num_wr", 0))
    score += min(num_receivers * 0.03, 0.18)

    situation = row.get("situation_bucket", "normal")
    if situation == "third_and_medium":
        score += 0.15
    elif situation == "red_zone":
        score += 0.10

    if bool(row.get("defensive_stress_penalty", False)):
        score += 0.2

    epa = row.get("epa", 0.0)
    if pd.notnull(epa):
        score += max(min(epa, 1.0), -0.5) * 0.25

    return float(max(0.0, min(1.0, score)))


def compute_conflict_scores(df: pd.DataFrame, score_col: str = "conflict_score") -> pd.DataFrame:
    """
    Compute conflict scores for all plays in a DataFrame.

    Adds a new column `score_col` with values in [0, 1].

    The input DataFrame must already contain engineered features.
    """
    df = df.copy()
    df[score_col] = df.apply(compute_conflict_score_row, axis=1)
    return df
