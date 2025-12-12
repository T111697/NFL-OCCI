"""
Transform raw play by play into model ready features and labels for conflict scoring.
"""
from __future__ import annotations

import pandas as pd

from .schema import DEFAULT_SCHEMA, FeatureSchema


def engineer_basic_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add basic engineered columns related to offensive structure and situation.

    This function should:
    - Parse offensive personnel strings into num_rb, num_te, num_wr.
    - Create flags for pre snap motion and play action if those columns exist.
    - Bucket target depth and pass location.
    - Create a score_diff field (offense_score - defense_score).
    - Create a high leverage 'situation_bucket' (normal, 3rd_and_medium, red_zone, 2min_drill).
    - Create a 'defensive_stress_penalty' flag when the penalty type indicates DB stress.
    """
    df = df.copy()

    if "personnel_offense" in df.columns:
        parts = df["personnel_offense"].str.extract(
            r"(?P<num_rb>\d) RB, (?P<num_te>\d) TE, (?P<num_wr>\d) WR"
        )
        for col in ["num_rb", "num_te", "num_wr"]:
            df[col] = pd.to_numeric(parts[col], errors="coerce").fillna(0).astype(int)
    else:
        df["num_rb"] = 0
        df["num_te"] = 0
        df["num_wr"] = 0

    df["has_motion"] = (
        df.get("motion", pd.Series([False] * len(df))).astype(bool)
        if "motion" in df.columns
        else False
    )
    df["has_play_action"] = (
        df.get("play_action", pd.Series([False] * len(df))).astype(bool)
        if "play_action" in df.columns
        else False
    )

    if "air_yards" in df.columns:
        df["target_air_yards"] = df["air_yards"].fillna(0)
        df["target_depth_bucket"] = pd.cut(
            df["target_air_yards"],
            bins=[-20, 0, 10, 20, 80],
            labels=["behind_or_short", "short", "intermediate", "deep"],
        )
    else:
        df["target_air_yards"] = 0.0
        df["target_depth_bucket"] = "unknown"

    if "pass_location" in df.columns:
        df["pass_location_bucket"] = df["pass_location"].fillna("unknown")
    else:
        df["pass_location_bucket"] = "unknown"

    if {"posteam_score", "defteam_score"}.issubset(df.columns):
        df["score_diff"] = df["posteam_score"].fillna(0) - df["defteam_score"].fillna(0)
    else:
        df["score_diff"] = 0

    def classify_situation(row: pd.Series) -> str:
        down = row.get("down", 0)
        ydstogo = row.get("ydstogo", 0)
        yardline = row.get("yardline_100", 100)
        if yardline <= 20:
            return "red_zone"
        if down == 3 and 3 <= ydstogo <= 7:
            return "third_and_medium"
        return "normal"

    df["situation_bucket"] = df.apply(classify_situation, axis=1)

    stress_penalties = {"Defensive Pass Interference", "Illegal Contact", "Defensive Holding"}
    if "penalty_type" in df.columns:
        df["defensive_stress_penalty"] = df["penalty_type"].isin(stress_penalties)
    else:
        df["defensive_stress_penalty"] = False

    df["personnel_group"] = (
        df["num_rb"].astype(str)
        + "RB_"
        + df["num_te"].astype(str)
        + "TE_"
        + df["num_wr"].astype(str)
        + "WR"
    )

    return df


def select_feature_columns(df: pd.DataFrame, schema: FeatureSchema | None = None) -> pd.DataFrame:
    """
    Select only the columns defined in the feature schema.
    """
    if schema is None:
        schema = DEFAULT_SCHEMA

    cols = list(schema.numeric_features) + list(schema.categorical_features)
    existing_cols = [c for c in cols if c in df.columns]
    return df[existing_cols]
