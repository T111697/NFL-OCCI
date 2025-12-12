import pandas as pd

from conflict_map.model.conflict_score import compute_conflict_score_row, compute_conflict_scores


def test_compute_conflict_score_row_handles_flags():
    row = pd.Series(
        {
            "has_motion": True,
            "has_play_action": True,
            "num_te": 1,
            "num_wr": 3,
            "situation_bucket": "third_and_medium",
            "defensive_stress_penalty": True,
            "epa": 0.5,
        }
    )
    score = compute_conflict_score_row(row)
    assert 0 <= score <= 1
    assert score > 0.6


def test_compute_conflict_scores_vectorizes():
    df = pd.DataFrame(
        [
            {"has_motion": False, "has_play_action": False, "num_te": 0, "num_wr": 2},
            {"has_motion": True, "has_play_action": True, "num_te": 2, "num_wr": 3},
        ]
    )
    result = compute_conflict_scores(df)
    assert "conflict_score" in result.columns
    assert len(result["conflict_score"]) == 2
    assert result["conflict_score"].iloc[1] > result["conflict_score"].iloc[0]
