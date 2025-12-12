"""
Offensive Conflict Creation Index (OCCI) computation.

This module aggregates play level conflict scores into:
- team season level OCCI
- team game level OCCI
- optionally, split by situation or opponent.
"""
from __future__ import annotations

import pandas as pd


def compute_team_game_occi(
    df_conflict: pd.DataFrame,
    team_col: str = "posteam",
    game_id_col: str = "game_id",
    score_col: str = "conflict_score",
) -> pd.DataFrame:
    """
    Compute OCCI per team per game.

    Returns a DataFrame with columns:
    - game_id
    - team
    - plays
    - occi_mean
    - occi_std
    """
    grouped = df_conflict.groupby([game_id_col, team_col])

    result = grouped[score_col].agg(
        plays="count",
        occi_mean="mean",
        occi_std="std",
    ).reset_index().rename(columns={team_col: "team"})
    return result


def compute_team_season_occi(
    df_game_occi: pd.DataFrame,
    season_lookup: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """
    Aggregate game level OCCI into season level OCCI per team.

    If season_lookup is provided, it should map game_id -> season.
    Otherwise, assume the input already has a 'season' column.
    """
    df = df_game_occi.copy()
    if season_lookup is not None:
        df = df.merge(season_lookup, on="game_id", how="left")

    if "season" not in df.columns:
        raise ValueError(
            "season column not found - provide a season_lookup or include season in df_game_occi"
        )

    grouped = df.groupby(["season", "team"])
    result = grouped["occi_mean"].agg(
        games="count",
        season_occi_mean="mean",
        season_occi_std="std",
    ).reset_index()
    return result
