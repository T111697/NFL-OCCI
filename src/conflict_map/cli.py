"""
Command line interface for computing OCCI from raw play by play.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .data.load import load_raw_multiple_seasons
from .features.build_features import engineer_basic_features
from .model.conflict_score import compute_conflict_scores
from .metrics.occi import compute_team_game_occi, compute_team_season_occi


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute Offensive Conflict Creation Index (OCCI)")
    parser.add_argument(
        "--seasons",
        nargs="+",
        type=int,
        required=True,
        help="Seasons to include, e.g. 2019 2020 2021",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path("data/processed"), help="Directory for output CSVs"
    )
    args = parser.parse_args()

    df_raw = load_raw_multiple_seasons(args.seasons)
    df_feat = engineer_basic_features(df_raw)
    df_conf = compute_conflict_scores(df_feat)

    df_game = compute_team_game_occi(df_conf)
    df_season = compute_team_season_occi(df_game)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    df_conf.to_csv(args.output_dir / "plays_with_conflict_scores.csv", index=False)
    df_game.to_csv(args.output_dir / "team_game_occi.csv", index=False)
    df_season.to_csv(args.output_dir / "team_season_occi.csv", index=False)


if __name__ == "__main__":
    main()
