"""
OCCI Calculator - Core computation logic for Offensive Conflict Creation Index

The OCCI metric estimates how often and intensely an offense forces a defense
into structurally difficult situations using various play-by-play proxies.
"""

import pandas as pd
import numpy as np


class OCCICalculator:
    """
    Calculator for Offensive Conflict Creation Index (OCCI).
    
    OCCI uses multiple factors from play-by-play data to estimate
    how much conflict an offense creates for the defense:
    - Motion usage
    - Formation tightness (personnel groupings)
    - Target depth (for passing plays)
    - Play action and RPO usage
    - Route variety and complexity
    """
    
    # Weights for different OCCI components
    WEIGHTS = {
        'motion': 0.15,
        'formation': 0.20,
        'target_depth': 0.20,
        'play_action': 0.15,
        'personnel': 0.15,
        'situational': 0.15,
    }
    
    # Maximum meaningful passing depth in yards for normalization
    MAX_TARGET_DEPTH = 50.0
    
    def __init__(self, pbp_data):
        """
        Initialize calculator with play-by-play data.
        
        Args:
            pbp_data: DataFrame with NFL play-by-play data
        """
        self.pbp_data = pbp_data.copy()
        self._prepare_features()
    
    def _prepare_features(self):
        """Extract and prepare features for OCCI calculation."""
        
        # Motion score - use shift in formation or no_huddle as proxy
        self.pbp_data['motion_score'] = np.where(
            self.pbp_data['no_huddle'] == 1, 1.0,
            np.where(self.pbp_data['shotgun'] == 1, 0.6, 0.3)
        )
        
        # Formation score - based on personnel and shotgun usage
        # More spread formations create more conflict
        self.pbp_data['formation_score'] = self._calculate_formation_score()
        
        # Target depth score - deeper targets create more conflict
        self.pbp_data['target_depth_score'] = self._calculate_target_depth_score()
        
        # Play action score
        self.pbp_data['play_action_score'] = np.where(
            self.pbp_data['pass_attempt'] == 1,
            np.where(self.pbp_data['qb_dropback'] == 1, 0.7, 0.3),
            0.5  # Run plays have moderate score
        )
        
        # Personnel score - variety in personnel creates conflict
        self.pbp_data['personnel_score'] = self._calculate_personnel_score()
        
        # Situational score - down and distance variety
        self.pbp_data['situational_score'] = self._calculate_situational_score()
    
    def _calculate_formation_score(self):
        """
        Calculate formation complexity score.
        
        Returns normalized score based on formation type.
        """
        # Use shotgun and available receiver information as proxy
        scores = np.zeros(len(self.pbp_data))
        
        # Shotgun formations generally more complex
        shotgun_mask = self.pbp_data['shotgun'] == 1
        scores[shotgun_mask] = 0.7
        
        # Under center
        scores[~shotgun_mask] = 0.4
        
        # No huddle adds complexity
        no_huddle_mask = self.pbp_data['no_huddle'] == 1
        scores[no_huddle_mask] += 0.3
        
        return np.clip(scores, 0, 1)
    
    def _calculate_target_depth_score(self):
        """
        Calculate target depth score for passing plays.
        
        Deeper targets create more conflict for defense.
        """
        scores = np.zeros(len(self.pbp_data))
        
        # For pass plays, use air_yards as proxy
        pass_mask = self.pbp_data['pass_attempt'] == 1
        air_yards = self.pbp_data['air_yards'].fillna(0)
        
        # Normalize air yards to 0-1 scale
        normalized_depth = np.clip(air_yards / self.MAX_TARGET_DEPTH, 0, 1)
        scores[pass_mask] = normalized_depth[pass_mask]
        
        # For run plays, use moderate fixed score
        scores[~pass_mask] = 0.4
        
        return scores
    
    def _calculate_personnel_score(self):
        """
        Calculate personnel variety score.
        
        More diverse personnel creates more conflict.
        """
        # Use number of pass attempts vs runs as proxy for variety
        scores = np.where(
            self.pbp_data['pass_attempt'] == 1,
            0.6,  # Pass plays
            0.4   # Run plays
        )
        
        # Adjust for down - unexpected playcalls create more conflict
        # E.g., passing on early downs, running on 3rd and long
        down = self.pbp_data['down'].fillna(1)
        ydstogo = self.pbp_data['ydstogo'].fillna(10)
        
        # Pass on 1st/2nd down or run on 3rd+ and long
        unexpected_mask = (
            ((down <= 2) & (self.pbp_data['pass_attempt'] == 1)) |
            ((down >= 3) & (ydstogo >= 7) & (self.pbp_data['rush_attempt'] == 1))
        )
        scores[unexpected_mask] += 0.2
        
        return np.clip(scores, 0, 1)
    
    def _calculate_situational_score(self):
        """
        Calculate situational complexity score.
        
        More challenging situations create more conflict.
        """
        scores = np.ones(len(self.pbp_data)) * 0.5  # Base score
        
        # Scoring position increases complexity
        yardline = self.pbp_data['yardline_100'].fillna(50)
        scores += np.where(yardline <= 20, 0.2, 0)
        
        # Third/fourth down increases complexity
        down = self.pbp_data['down'].fillna(1)
        scores += np.where(down >= 3, 0.2, 0)
        
        # Close games increase complexity
        score_diff = self.pbp_data['score_differential'].fillna(0).abs()
        scores += np.where(score_diff <= 7, 0.1, 0)
        
        return np.clip(scores, 0, 1)
    
    def calculate_play_occi(self):
        """
        Calculate OCCI for each play.
        
        Returns:
            Series with OCCI score for each play
        """
        occi = (
            self.pbp_data['motion_score'] * self.WEIGHTS['motion'] +
            self.pbp_data['formation_score'] * self.WEIGHTS['formation'] +
            self.pbp_data['target_depth_score'] * self.WEIGHTS['target_depth'] +
            self.pbp_data['play_action_score'] * self.WEIGHTS['play_action'] +
            self.pbp_data['personnel_score'] * self.WEIGHTS['personnel'] +
            self.pbp_data['situational_score'] * self.WEIGHTS['situational']
        )
        
        # Normalize to 0-100 scale
        self.pbp_data['occi'] = occi * 100
        
        return self.pbp_data['occi']
    
    def calculate_team_occi(self):
        """
        Calculate aggregate OCCI metrics by team.
        
        Returns:
            DataFrame with team-level OCCI statistics
        """
        # Ensure play OCCI is calculated
        if 'occi' not in self.pbp_data.columns:
            self.calculate_play_occi()
        
        # Group by offensive team
        team_stats = self.pbp_data.groupby('posteam').agg({
            'occi': ['mean', 'std', 'median', 'count'],
            'pass_attempt': 'sum',
            'rush_attempt': 'sum',
        }).round(2)
        
        # Flatten column names
        team_stats.columns = ['_'.join(col).strip() for col in team_stats.columns.values]
        team_stats = team_stats.rename(columns={
            'occi_mean': 'avg_occi',
            'occi_std': 'occi_std',
            'occi_median': 'median_occi',
            'occi_count': 'total_plays',
            'pass_attempt_sum': 'pass_plays',
            'rush_attempt_sum': 'rush_plays',
        })
        
        # Calculate pass rate
        team_stats['pass_rate'] = (
            team_stats['pass_plays'] / team_stats['total_plays'] * 100
        ).round(1)
        
        # Sort by average OCCI
        team_stats = team_stats.sort_values('avg_occi', ascending=False)
        
        return team_stats.reset_index()
    
    def get_play_data_with_occi(self):
        """
        Get full play-by-play data with OCCI scores.
        
        Returns:
            DataFrame with plays and OCCI scores
        """
        if 'occi' not in self.pbp_data.columns:
            self.calculate_play_occi()
        
        return self.pbp_data
