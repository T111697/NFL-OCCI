"""
Flask web application for visualizing OCCI metrics
"""

from flask import Flask, render_template, jsonify, request
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
import sys
import os

# Add parent directory to path to import occi package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from occi import OCCICalculator, load_nfl_data

app = Flask(__name__)

# Global variables to cache data
pbp_data = None
calculator = None
team_stats = None


def initialize_data(seasons=[2023]):
    """Initialize NFL data and OCCI calculator."""
    global pbp_data, calculator, team_stats
    
    print("Initializing data...")
    pbp_data = load_nfl_data(seasons)
    calculator = OCCICalculator(pbp_data)
    calculator.calculate_play_occi()
    team_stats = calculator.calculate_team_occi()
    print("Data initialized successfully!")


@app.route('/')
def index():
    """Main page with OCCI visualizations."""
    return render_template('index.html')


@app.route('/api/team-rankings')
def team_rankings():
    """API endpoint to get team OCCI rankings."""
    if team_stats is None:
        return jsonify({"error": "Data not loaded"}), 500
    
    return jsonify(team_stats.to_dict(orient='records'))


@app.route('/api/team-chart')
def team_chart():
    """Generate team OCCI comparison chart."""
    if team_stats is None:
        return jsonify({"error": "Data not loaded"}), 500
    
    # Create bar chart of team OCCI scores
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=team_stats['posteam'],
        y=team_stats['avg_occi'],
        marker_color='rgb(55, 83, 109)',
        text=team_stats['avg_occi'].round(1),
        textposition='auto',
    ))
    
    fig.update_layout(
        title='NFL Teams by Average OCCI Score',
        xaxis_title='Team',
        yaxis_title='Average OCCI',
        height=500,
        template='plotly_white',
        showlegend=False,
    )
    
    return json.dumps(fig, cls=PlotlyJSONEncoder)


@app.route('/api/occi-distribution')
def occi_distribution():
    """Generate OCCI distribution chart."""
    if calculator is None:
        return jsonify({"error": "Data not loaded"}), 500
    
    play_data = calculator.get_play_data_with_occi()
    
    # Create histogram of OCCI scores
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=play_data['occi'],
        nbinsx=50,
        marker_color='rgb(55, 83, 109)',
    ))
    
    fig.update_layout(
        title='Distribution of OCCI Scores Across All Plays',
        xaxis_title='OCCI Score',
        yaxis_title='Number of Plays',
        height=400,
        template='plotly_white',
        showlegend=False,
    )
    
    return json.dumps(fig, cls=PlotlyJSONEncoder)


@app.route('/api/team-detail/<team>')
def team_detail(team):
    """Get detailed OCCI breakdown for a specific team."""
    if calculator is None:
        return jsonify({"error": "Data not loaded"}), 500
    
    play_data = calculator.get_play_data_with_occi()
    team_plays = play_data[play_data['posteam'] == team]
    
    if len(team_plays) == 0:
        return jsonify({"error": f"No data found for team {team}"}), 404
    
    # Calculate component averages
    components = {
        'Motion': team_plays['motion_score'].mean() * 100,
        'Formation': team_plays['formation_score'].mean() * 100,
        'Target Depth': team_plays['target_depth_score'].mean() * 100,
        'Play Action': team_plays['play_action_score'].mean() * 100,
        'Personnel': team_plays['personnel_score'].mean() * 100,
        'Situational': team_plays['situational_score'].mean() * 100,
    }
    
    # Create radar chart
    categories = list(components.keys())
    values = list(components.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=team
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        title=f'OCCI Component Breakdown - {team}',
        height=500,
    )
    
    return json.dumps(fig, cls=PlotlyJSONEncoder)


@app.route('/api/pass-vs-run')
def pass_vs_run():
    """Compare OCCI for pass vs run plays."""
    if calculator is None:
        return jsonify({"error": "Data not loaded"}), 500
    
    play_data = calculator.get_play_data_with_occi()
    
    pass_plays = play_data[play_data['pass_attempt'] == 1]['occi']
    run_plays = play_data[play_data['rush_attempt'] == 1]['occi']
    
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=pass_plays,
        name='Pass Plays',
        marker_color='rgb(55, 83, 109)'
    ))
    
    fig.add_trace(go.Box(
        y=run_plays,
        name='Run Plays',
        marker_color='rgb(26, 118, 255)'
    ))
    
    fig.update_layout(
        title='OCCI Distribution: Pass vs Run Plays',
        yaxis_title='OCCI Score',
        height=400,
        template='plotly_white',
    )
    
    return json.dumps(fig, cls=PlotlyJSONEncoder)


if __name__ == '__main__':
    # Initialize with 2023 season data
    initialize_data(seasons=[2023])
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
