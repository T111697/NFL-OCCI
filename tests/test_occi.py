import pandas as pd

from conflict_map.metrics.occi import compute_team_game_occi, compute_team_season_occi


def test_compute_team_game_and_season_occi():
    df_conflict = pd.DataFrame(
        {
            "game_id": [1, 1, 1, 2, 2],
            "posteam": ["A", "A", "A", "A", "B"],
            "conflict_score": [0.2, 0.4, 0.6, 0.5, 0.3],
            "season": [2023, 2023, 2023, 2023, 2023],
        }
    )

    df_game = compute_team_game_occi(df_conflict)
    assert set(df_game.columns) == {"game_id", "team", "plays", "occi_mean", "occi_std"}
    assert df_game.loc[df_game["game_id"] == 1, "plays"].iloc[0] == 3

    season_lookup = df_conflict[["game_id", "season"]].drop_duplicates()
    df_season = compute_team_season_occi(df_game, season_lookup=season_lookup)
    assert set(df_season.columns) == {"season", "team", "games", "season_occi_mean", "season_occi_std"}
    assert df_season.loc[df_season["team"] == "A", "games"].iloc[0] == 2
