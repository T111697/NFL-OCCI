"""
Streamlit app to explore OCCI interactively.
"""
from __future__ import annotations

import pathlib
import streamlit as st
import pandas as pd

from ..viz.plots import plot_team_season_occi

DATA_DIR = pathlib.Path(__file__).resolve().parents[2] / "data" / "processed"


@st.cache_data
def load_team_season_occi() -> pd.DataFrame:
    csv_path = DATA_DIR / "team_season_occi.csv"
    if not csv_path.exists():
        st.error("team_season_occi.csv not found. Run the CLI to generate data first.")
        st.stop()
    return pd.read_csv(csv_path)


def main() -> None:
    st.title("Offensive Conflict Creation Index (OCCI) - Lite")

    df_season = load_team_season_occi()
    seasons = sorted(df_season["season"].unique())
    selected_season = st.selectbox("Season", seasons, index=len(seasons) - 1)

    st.subheader(f"Team OCCI for {selected_season}")
    plot_team_season_occi(df_season, selected_season)

    st.write("Raw data:")
    st.dataframe(df_season[df_season["season"] == selected_season])


if __name__ == "__main__":
    main()
