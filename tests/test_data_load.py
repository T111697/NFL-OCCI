import pandas as pd

from conflict_map.data.load import load_raw_season, load_weekly_updates


def test_load_raw_season_supports_gzip(tmp_path):
    df = pd.DataFrame({"season": [2026], "game_id": [1], "play_id": [10]})
    gz_path = tmp_path / "pbp_2026.csv.gz"
    df.to_csv(gz_path, index=False)

    loaded = load_raw_season(2026, data_dir=tmp_path)
    pd.testing.assert_frame_equal(loaded, df)


def test_load_weekly_updates(tmp_path):
    weekly_dir = tmp_path / "weekly"
    weekly_dir.mkdir()
    df_w1 = pd.DataFrame({"season": [2026], "week": [1], "game_id": ["g1"], "play_id": [1]})
    df_w2 = pd.DataFrame({"season": [2026], "week": [2], "game_id": ["g2"], "play_id": [2]})
    df_w1.to_csv(weekly_dir / "pbp_2026_week_1.csv", index=False)
    df_w2.to_csv(weekly_dir / "pbp_2026_week_2.csv", index=False)

    loaded = load_weekly_updates(2026, weeks=[1, 2], weekly_dir=weekly_dir)
    assert set(loaded["week"]) == {1, 2}
    assert len(loaded) == 2
