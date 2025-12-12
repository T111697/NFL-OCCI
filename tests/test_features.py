import pandas as pd

from conflict_map.features.build_features import engineer_basic_features, select_feature_columns
from conflict_map.features.schema import DEFAULT_SCHEMA


def test_engineer_basic_features_adds_expected_columns():
    data = {
        "personnel_offense": ["1 RB, 1 TE, 3 WR", "0 RB, 2 TE, 3 WR"],
        "motion": [1, 0],
        "play_action": [0, 1],
        "air_yards": [5, 18],
        "pass_location": ["left", "middle"],
        "posteam_score": [14, 21],
        "defteam_score": [7, 10],
        "down": [1, 3],
        "ydstogo": [10, 5],
        "yardline_100": [60, 15],
        "penalty_type": ["None", "Defensive Pass Interference"],
    }
    df = pd.DataFrame(data)

    engineered = engineer_basic_features(df)

    expected_cols = {
        "num_rb",
        "num_te",
        "num_wr",
        "has_motion",
        "has_play_action",
        "target_air_yards",
        "target_depth_bucket",
        "pass_location_bucket",
        "score_diff",
        "situation_bucket",
        "defensive_stress_penalty",
        "personnel_group",
    }
    assert expected_cols.issubset(engineered.columns)

    assert engineered.loc[0, "num_rb"] == 1
    assert engineered.loc[1, "num_te"] == 2
    assert bool(engineered.loc[0, "has_motion"])
    assert bool(engineered.loc[1, "has_play_action"])
    assert bool(engineered.loc[1, "defensive_stress_penalty"])
    assert engineered.loc[1, "situation_bucket"] == "red_zone"


def test_select_feature_columns_respects_schema():
    df = pd.DataFrame(
        {
            "down": [1],
            "ydstogo": [10],
            "yardline_100": [50],
            "score_diff": [0],
            "num_rb": [1],
            "num_te": [1],
            "num_wr": [3],
            "target_air_yards": [5.0],
            "personnel_group": ["1RB_1TE_3WR"],
            "pass_location_bucket": ["left"],
            "target_depth_bucket": ["short"],
            "situation_bucket": ["normal"],
            "has_motion": [False],
            "has_play_action": [False],
            "defensive_stress_penalty": [False],
            "extra_column": [123],
        }
    )

    filtered = select_feature_columns(df, DEFAULT_SCHEMA)
    assert set(filtered.columns) == set(DEFAULT_SCHEMA.numeric_features + DEFAULT_SCHEMA.categorical_features)
