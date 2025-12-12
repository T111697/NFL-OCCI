"""
Helpers for drawing a football field. Placeholder for future interactive visuals.
"""
from __future__ import annotations

import matplotlib.pyplot as plt


def draw_basic_field(ax: plt.Axes | None = None) -> plt.Axes:
    """Draw a simple football field background and return the axes."""
    if ax is None:
        _, ax = plt.subplots(figsize=(12, 6))

    ax.set_xlim(0, 120)
    ax.set_ylim(0, 53.3)
    ax.axvspan(0, 10, color="#e0f7fa", alpha=0.5)
    ax.axvspan(110, 120, color="#e0f7fa", alpha=0.5)
    for yard in range(10, 111, 10):
        ax.axvline(yard, color="lightgray", linestyle="--", linewidth=0.7)
    ax.set_xlabel("Yards")
    ax.set_ylabel("Sideline to sideline")
    ax.set_title("Field Template")
    return ax
