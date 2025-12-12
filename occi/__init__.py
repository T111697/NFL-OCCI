"""
NFL Offensive Conflict Creation Index (OCCI) Package

This package computes and visualizes the OCCI metric for NFL offenses,
estimating how often and intensely an offense forces a defense into
structurally difficult situations.
"""

__version__ = "0.1.0"

from .calculator import OCCICalculator
from .data_loader import load_nfl_data

__all__ = ["OCCICalculator", "load_nfl_data"]
