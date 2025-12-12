"""
Definitions of the feature schema used by the conflict model.
"""
from dataclasses import dataclass
from typing import List


@dataclass
class FeatureSchema:
    """
    Simple container for feature names used by the model.
    """

    numeric_features: List[str]
    categorical_features: List[str]


DEFAULT_SCHEMA = FeatureSchema(
    numeric_features=[
        "down",
        "ydstogo",
        "yardline_100",
        "score_diff",
        "num_rb",
        "num_te",
        "num_wr",
        "target_air_yards",
    ],
    categorical_features=[
        "personnel_group",
        "pass_location_bucket",
        "target_depth_bucket",
        "situation_bucket",
        "has_motion",
        "has_play_action",
        "defensive_stress_penalty",
    ],
)
