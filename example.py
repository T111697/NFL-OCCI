#!/usr/bin/env python3
"""
Example script demonstrating OCCI calculation and analysis
"""

from occi import OCCICalculator, load_nfl_data


def main():
    """Run OCCI analysis example."""
    
    print("=" * 70)
    print("NFL Offensive Conflict Creation Index (OCCI) - Example Analysis")
    print("=" * 70)
    print()
    
    # Load data for 2023 season
    print("Step 1: Loading NFL play-by-play data for 2023 season...")
    pbp_data = load_nfl_data(seasons=[2023])
    print(f"✓ Loaded {len(pbp_data):,} plays\n")
    
    # Initialize calculator
    print("Step 2: Initializing OCCI Calculator...")
    calculator = OCCICalculator(pbp_data)
    print("✓ Calculator initialized\n")
    
    # Calculate play-level OCCI
    print("Step 3: Calculating OCCI for each play...")
    play_occi = calculator.calculate_play_occi()
    print(f"✓ Calculated OCCI for {len(play_occi):,} plays")
    print(f"  - Average OCCI: {play_occi.mean():.2f}")
    print(f"  - Median OCCI: {play_occi.median():.2f}")
    print(f"  - Std Dev: {play_occi.std():.2f}\n")
    
    # Calculate team-level OCCI
    print("Step 4: Calculating team-level OCCI statistics...")
    team_stats = calculator.calculate_team_occi()
    print("✓ Team statistics calculated\n")
    
    # Display top 10 teams
    print("=" * 70)
    print("TOP 10 TEAMS BY AVERAGE OCCI")
    print("=" * 70)
    print(f"{'Rank':<6} {'Team':<6} {'Avg OCCI':<12} {'Plays':<8} {'Pass Rate':<12}")
    print("-" * 70)
    
    for idx, row in team_stats.head(10).iterrows():
        print(f"{idx+1:<6} {row['posteam']:<6} {row['avg_occi']:<12.2f} "
              f"{int(row['total_plays']):<8} {row['pass_rate']:<12.1f}%")
    
    print()
    
    # Display bottom 5 teams
    print("=" * 70)
    print("BOTTOM 5 TEAMS BY AVERAGE OCCI")
    print("=" * 70)
    print(f"{'Rank':<6} {'Team':<6} {'Avg OCCI':<12} {'Plays':<8} {'Pass Rate':<12}")
    print("-" * 70)
    
    total_teams = len(team_stats)
    for idx, row in team_stats.tail(5).iterrows():
        rank = total_teams - (len(team_stats) - idx - 1)
        print(f"{rank:<6} {row['posteam']:<6} {row['avg_occi']:<12.2f} "
              f"{int(row['total_plays']):<8} {row['pass_rate']:<12.1f}%")
    
    print()
    print("=" * 70)
    print("Analysis complete!")
    print()
    print("To view visualizations, run the web app:")
    print("  python webapp/app.py")
    print("Then open http://localhost:5000 in your browser")
    print("=" * 70)


if __name__ == '__main__':
    main()
