"""
Basic plotting utilities for OCCI results.
"""
from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt


def plot_team_season_occi(df_season: pd.DataFrame, season: int) -> None:
    """
    Horizontal bar chart of season OCCI for a single year.
    """
    subset = df_season[df_season["season"] == season].sort_values("season_occi_mean", ascending=True)

    plt.figure(figsize=(8, 10))
    plt.barh(subset["team"], subset["season_occi_mean"])
    plt.xlabel("Season OCCI mean")
    plt.ylabel("Team")
    plt.title(f"Offensive Conflict Creation Index - {season}")
    plt.tight_layout()
    plt.show()
