"""
Streamlit app to explore OCCI interactively.
"""
from __future__ import annotations

import pathlib
from typing import List

import pandas as pd
import streamlit as st

from ..viz.plots import plot_team_season_occi, plot_team_season_trend

DATA_DIR = pathlib.Path(__file__).resolve().parents[2] / "data" / "processed"

st.set_page_config(
    page_title="OCCI Lite Explorer",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def build_demo_season_data() -> pd.DataFrame:
    demo = [
        {"season": 2022, "team": "BUF", "season_occi_mean": 0.584, "season_occi_std": 0.06, "games": 17},
        {"season": 2022, "team": "PHI", "season_occi_mean": 0.565, "season_occi_std": 0.05, "games": 17},
        {"season": 2022, "team": "KC", "season_occi_mean": 0.602, "season_occi_std": 0.07, "games": 17},
        {"season": 2022, "team": "SF", "season_occi_mean": 0.553, "season_occi_std": 0.06, "games": 17},
        {"season": 2023, "team": "BUF", "season_occi_mean": 0.611, "season_occi_std": 0.05, "games": 17},
        {"season": 2023, "team": "PHI", "season_occi_mean": 0.575, "season_occi_std": 0.05, "games": 17},
        {"season": 2023, "team": "KC", "season_occi_mean": 0.593, "season_occi_std": 0.05, "games": 17},
        {"season": 2023, "team": "SF", "season_occi_mean": 0.578, "season_occi_std": 0.04, "games": 17},
        {"season": 2023, "team": "MIA", "season_occi_mean": 0.623, "season_occi_std": 0.06, "games": 17},
    ]
    return pd.DataFrame(demo)


@st.cache_data
def build_demo_game_data() -> pd.DataFrame:
    demo = [
        {"season": 2023, "week": 1, "game_id": "2023BUF1", "team": "BUF", "opponent": "NYJ", "plays": 64, "occi_mean": 0.64, "occi_std": 0.08},
        {"season": 2023, "week": 2, "game_id": "2023BUF2", "team": "BUF", "opponent": "LVR", "plays": 62, "occi_mean": 0.60, "occi_std": 0.05},
        {"season": 2023, "week": 3, "game_id": "2023BUF3", "team": "BUF", "opponent": "MIA", "plays": 65, "occi_mean": 0.63, "occi_std": 0.06},
        {"season": 2023, "week": 1, "game_id": "2023MIA1", "team": "MIA", "opponent": "LAC", "plays": 68, "occi_mean": 0.66, "occi_std": 0.07},
        {"season": 2023, "week": 2, "game_id": "2023MIA2", "team": "MIA", "opponent": "NE", "plays": 60, "occi_mean": 0.62, "occi_std": 0.06},
        {"season": 2023, "week": 3, "game_id": "2023MIA3", "team": "MIA", "opponent": "BUF", "plays": 59, "occi_mean": 0.64, "occi_std": 0.05},
    ]
    return pd.DataFrame(demo)

import streamlit as st
import pandas as pd

from ..viz.plots import plot_team_season_occi

DATA_DIR = pathlib.Path(__file__).resolve().parents[2] / "data" / "processed"


@st.cache_data
def load_team_season_occi() -> pd.DataFrame:
    csv_path = DATA_DIR / "team_season_occi.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path)
    st.info("Processed `team_season_occi.csv` not found. Using a short demo dataset so the UI remains explorable.")
    return build_demo_season_data()


@st.cache_data
def load_team_game_occi() -> pd.DataFrame | None:
    csv_path = DATA_DIR / "team_game_occi.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return build_demo_game_data()


def style_app_shell() -> None:
    st.markdown(
        """
        <style>
            .block-container { padding-top: 2rem; }
            .occi-metric { background: linear-gradient(135deg, #0f172a, #1e293b); color: #f8fafc; padding: 1rem; border-radius: 0.75rem; }
            .occi-card { border: 1px solid #e2e8f0; padding: 1rem; border-radius: 0.75rem; background: #ffffff; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_season_section(df_season: pd.DataFrame) -> List[str]:
    seasons = sorted(df_season["season"].unique())
    teams = sorted(df_season["team"].unique())

    st.header("League pulse")
    selected_season = st.selectbox("Season", seasons, index=len(seasons) - 1, key="season_select")
    highlight_teams = st.multiselect(
        "Highlight teams",
        options=teams,
        default=teams[:3] if teams else [],
        help="Highlighted teams pop in the visual and drive downstream comparisons.",
    )

    season_df = df_season[df_season["season"] == selected_season]
    if season_df.empty:
        st.warning("No rows for the selected season.")
        return highlight_teams

    col1, col2, col3 = st.columns(3)
    league_mean = season_df["season_occi_mean"].mean()
    top_row = season_df.sort_values("season_occi_mean", ascending=False).iloc[0]
    spread = season_df["season_occi_mean"].max() - season_df["season_occi_mean"].min()

    col1.metric("League average OCCI", f"{league_mean:.3f}")
    col2.metric("Top offense", f"{top_row['team']} — {top_row['season_occi_mean']:.3f}")
    col3.metric("Top-to-bottom spread", f"{spread:.3f}")

    fig = plot_team_season_occi(df_season, selected_season, highlight_teams=highlight_teams)
    st.pyplot(fig, clear_figure=True)

    st.caption("Values are heuristic conflict scores aggregated per team-season. Higher implies more consistent structural stress on defenses.")
    st.dataframe(
        season_df.sort_values("season_occi_mean", ascending=False).style.format({"season_occi_mean": "{:.3f}", "season_occi_std": "{:.3f}"}),
        use_container_width=True,
    )
    st.download_button(
        "Download season slice as CSV",
        data=season_df.to_csv(index=False).encode("utf-8"),
        file_name=f"team_season_occi_{selected_season}.csv",
        mime="text/csv",
    )
    return highlight_teams


def render_trend_section(df_season: pd.DataFrame, default_teams: List[str]) -> None:
    st.header("Tempo over time")
    teams = sorted(df_season["team"].unique())
    trend_teams = st.multiselect(
        "Pick teams to compare over seasons",
        options=teams,
        default=default_teams[:3] if default_teams else teams[:3],
    )
    if not trend_teams:
        st.info("Select one or more teams to draw a season-by-season curve.")
        return

    fig = plot_team_season_trend(df_season, trend_teams)
    st.pyplot(fig, clear_figure=True)

    st.dataframe(
        df_season[df_season["team"].isin(trend_teams)].sort_values(["team", "season"]).style.format(
            {"season_occi_mean": "{:.3f}", "season_occi_std": "{:.3f}"}
        ),
        use_container_width=True,
    )


def render_game_section(df_game: pd.DataFrame | None, default_team: str | None) -> None:
    st.header("Game-level texture")
    if df_game is None or df_game.empty:
        st.info("Add `data/processed/team_game_occi.csv` to unlock game-level views.")
        return

    teams = sorted(df_game["team"].unique())
    focus_team = st.selectbox("Focus team", options=teams, index=teams.index(default_team) if default_team in teams else 0)
    team_games = df_game[df_game["team"] == focus_team].copy()
    if team_games.empty:
        st.warning("No games for this team in the loaded data.")
        return

    team_games = team_games.sort_values(["season", "week"] if "week" in team_games.columns else ["game_id"])
    chart_data = team_games[["week", "occi_mean"]] if "week" in team_games.columns else team_games[["game_id", "occi_mean"]]
    chart_data = chart_data.set_index(chart_data.columns[0])

    st.subheader(f"{focus_team} game-to-game OCCI")
    st.line_chart(chart_data, height=280)

    st.dataframe(
        team_games.style.format({"occi_mean": "{:.3f}", "occi_std": "{:.3f}"}),
        use_container_width=True,
    )
    st.download_button(
        f"Download {focus_team} games as CSV",
        data=team_games.to_csv(index=False).encode("utf-8"),
        file_name=f"{focus_team}_game_occi.csv",
        mime="text/csv",
    )


def render_methodology() -> None:
    with st.expander("What am I looking at?", expanded=False):
        st.markdown(
            """
            **OCCI** is a public-data-only heuristic for how much an offense stresses defensive structure.
            Scores reflect motion, play action, personnel spread, leverage situations, and stress penalties.
            Use this view to spot trend shifts, compare peer offenses, and decide where deeper film work is warranted.
            """
        )



def main() -> None:
    style_app_shell()
    st.title("Offensive Conflict Creation Index (OCCI) — Lite")
    st.write("Explore league-wide stress creation using only public play-by-play signals.")

    df_season = load_team_season_occi()
    df_game = load_team_game_occi()

    highlight_teams = render_season_section(df_season)
    render_trend_section(df_season, highlight_teams)
    render_game_section(df_game, highlight_teams[0] if highlight_teams else None)
    render_methodology()
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
