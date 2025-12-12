"""
Basic plotting utilities for OCCI results.
"""
from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt


def plot_team_season_occi(
    df_season: pd.DataFrame,
    season: int,
    highlight_teams: list[str] | None = None,
) -> plt.Figure:
    """
    Horizontal bar chart of season OCCI for a single year.

    Returns a matplotlib Figure for embedding in notebooks or Streamlit.
    """
    subset = df_season[df_season["season"] == season].sort_values("season_occi_mean", ascending=True)
    highlight_set = set(highlight_teams or [])

    colors = ["#1f77b4" if team not in highlight_set else "#ff7f0e" for team in subset["team"]]

    fig, ax = plt.subplots(figsize=(9, 10))
    bars = ax.barh(subset["team"], subset["season_occi_mean"], color=colors, alpha=0.9)
    ax.set_xlabel("Season OCCI mean")
    ax.set_ylabel("Team")
    ax.set_title(f"Offensive Conflict Creation Index - {season}")

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.005, bar.get_y() + bar.get_height() / 2, f"{width:.3f}", va="center")

    ax.grid(axis="x", linestyle="--", alpha=0.4)
    fig.tight_layout()
    return fig


def plot_team_season_trend(df_season: pd.DataFrame, teams: list[str]) -> plt.Figure:
    """
    Line chart of OCCI by season for selected teams.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    for team in teams:
        team_df = df_season[df_season["team"] == team].sort_values("season")
        ax.plot(team_df["season"], team_df["season_occi_mean"], marker="o", label=team)

    ax.set_xlabel("Season")
    ax.set_ylabel("Season OCCI mean")
    ax.set_title("Seasonal OCCI trend")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()
    return fig
