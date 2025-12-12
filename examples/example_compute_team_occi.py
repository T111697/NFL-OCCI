"""Example script to compute team-level OCCI from existing play-level CSVs."""
from __future__ import annotations

import pandas as pd

from conflict_map.features.build_features import engineer_basic_features
from conflict_map.model.conflict_score import compute_conflict_scores
from conflict_map.metrics.occi import compute_team_game_occi, compute_team_season_occi


if __name__ == "__main__":
    raw_path = "data/raw/pbp_2023.csv"
    df_raw = pd.read_csv(raw_path)
    df_feat = engineer_basic_features(df_raw)
    df_conf = compute_conflict_scores(df_feat)

    df_game = compute_team_game_occi(df_conf)
    df_season = compute_team_season_occi(df_game)

    print(df_game.head())
    print(df_season.head())
