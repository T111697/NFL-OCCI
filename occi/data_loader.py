"""
Data loading utilities for NFL play-by-play data
"""

import nfl_data_py as nfl
import pandas as pd


def load_nfl_data(seasons, refresh=False):
    """
    Load NFL play-by-play data for specified seasons.
    
    Args:
        seasons: List of seasons (years) to load data for
        refresh: If True, download fresh data; otherwise use cached data
        
    Returns:
        DataFrame with play-by-play data
    """
    print(f"Loading NFL play-by-play data for seasons: {seasons}")
    pbp = nfl.import_pbp_data(seasons, downcast=False)
    
    # Filter to regular plays (exclude special teams, kickoffs, etc.)
    pbp = pbp[
        (pbp['play_type'].isin(['pass', 'run'])) &
        (pbp['down'].notna())
    ].copy()
    
    print(f"Loaded {len(pbp)} plays from {pbp['game_id'].nunique()} games")
    
    return pbp


def get_team_list(pbp_data):
    """
    Extract list of teams from play-by-play data.
    
    Args:
        pbp_data: DataFrame with play-by-play data
        
    Returns:
        Sorted list of unique team abbreviations
    """
    teams = pd.concat([
        pbp_data['posteam'],
        pbp_data['defteam']
    ]).dropna().unique()
    
    return sorted(teams)
