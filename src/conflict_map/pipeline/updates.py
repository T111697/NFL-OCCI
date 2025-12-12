"""Pipeline helpers for base builds and weekly rollups."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Sequence

import pandas as pd

from ..data.load import load_raw_multiple_seasons, load_raw_season, load_weekly_updates
from ..features.build_features import engineer_basic_features
from ..metrics.occi import compute_team_game_occi, compute_team_season_occi
from ..model.conflict_score import compute_conflict_scores


def _dedupe_conflict_frame(df_conf: pd.DataFrame) -> pd.DataFrame:
    keys = [col for col in ("game_id", "play_id") if col in df_conf.columns]
    if not keys:
        return df_conf
    return df_conf.drop_duplicates(subset=keys, keep="last")


def run_pipeline(df_raw: pd.DataFrame, output_dir: Path, metadata: dict | None = None) -> dict[str, Path]:
    """Run the full conflict pipeline on a raw frame and write CSV outputs."""

    df_feat = engineer_basic_features(df_raw)
    df_conf = compute_conflict_scores(df_feat)
    df_conf = _dedupe_conflict_frame(df_conf)

    df_game = compute_team_game_occi(df_conf)
    season_lookup = df_conf[["game_id", "season"]].drop_duplicates() if "season" in df_conf.columns else None
    df_season = compute_team_season_occi(df_game, season_lookup=season_lookup)

    output_dir.mkdir(parents=True, exist_ok=True)
    conflict_path = output_dir / "plays_with_conflict_scores.csv"
    game_path = output_dir / "team_game_occi.csv"
    season_path = output_dir / "team_season_occi.csv"

    df_conf.to_csv(conflict_path, index=False)
    df_game.to_csv(game_path, index=False)
    df_season.to_csv(season_path, index=False)

    meta = metadata or {}
    meta.update(
        {
            "seasons": sorted(df_conf["season"].dropna().unique().tolist()) if "season" in df_conf.columns else [],
            "plays": int(len(df_conf)),
            "games": int(df_game.shape[0]),
        }
    )
    (output_dir / "occi_run_metadata.json").write_text(json.dumps(meta, indent=2))

    return {"conflict": conflict_path, "game": game_path, "season": season_path}


def build_from_ranges(
    base_seasons: Iterable[int],
    latest_season: int | None,
    latest_weeks: Sequence[int] | None,
    output_dir: Path,
) -> dict[str, Path]:
    """Load historical seasons plus an in-progress season and run the pipeline."""

    frames: list[pd.DataFrame] = []
    base_seasons = list(base_seasons)
    if base_seasons:
        frames.append(load_raw_multiple_seasons(base_seasons))

    if latest_season is not None:
        if latest_weeks:
            frames.append(load_weekly_updates(latest_season, latest_weeks))
        else:
            frames.append(load_raw_season(latest_season))

    if not frames:
        raise ValueError("No seasons provided. Specify base seasons or a latest season to process.")

    df_raw = pd.concat(frames, ignore_index=True)
    metadata = {
        "base_seasons": base_seasons,
        "latest_season": latest_season,
        "latest_weeks": list(latest_weeks) if latest_weeks else [],
    }
    return run_pipeline(df_raw, output_dir=output_dir, metadata=metadata)


def append_weekly_updates(
    processed_dir: Path,
    season: int,
    weeks: Sequence[int],
    weekly_dir: Path | None = None,
) -> dict[str, Path]:
    """Append new weekly raw files to an existing processed run.

    If existing outputs are missing the conflict scores will be rebuilt from the
    provided weekly updates only. This keeps the command resilient while still
    encouraging a historical base build.
    """

    weekly_raw = load_weekly_updates(season, weeks, weekly_dir=weekly_dir)
    df_feat = engineer_basic_features(weekly_raw)
    df_updates = compute_conflict_scores(df_feat)

    conflict_path = processed_dir / "plays_with_conflict_scores.csv"
    if conflict_path.exists():
        df_base = pd.read_csv(conflict_path)
        df_conf = pd.concat([df_base, df_updates], ignore_index=True)
    else:
        df_conf = df_updates

    df_conf = _dedupe_conflict_frame(df_conf)

    df_game = compute_team_game_occi(df_conf)
    season_lookup = df_conf[["game_id", "season"]].drop_duplicates() if "season" in df_conf.columns else None
    df_season = compute_team_season_occi(df_game, season_lookup=season_lookup)

    processed_dir.mkdir(parents=True, exist_ok=True)
    df_conf.to_csv(conflict_path, index=False)
    game_path = processed_dir / "team_game_occi.csv"
    season_path = processed_dir / "team_season_occi.csv"
    df_game.to_csv(game_path, index=False)
    df_season.to_csv(season_path, index=False)

    meta_path = processed_dir / "occi_run_metadata.json"
    meta: dict = {}
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text())
        except json.JSONDecodeError:
            meta = {}

    meta.update(
        {
            "latest_weekly_update": {
                "season": season,
                "weeks": list(weeks),
            },
            "latest_season": season,
            "seasons": sorted(df_conf["season"].dropna().unique().tolist()) if "season" in df_conf.columns else [],
            "plays": int(len(df_conf)),
            "games": int(df_game.shape[0]),
        }
    )
    meta_path.write_text(json.dumps(meta, indent=2))

    return {"conflict": conflict_path, "game": game_path, "season": season_path}
