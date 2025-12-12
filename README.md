# NFL Offensive Conflict Creation Index (OCCI)

A Python package and web application for computing and visualizing the Offensive Conflict Creation Index (OCCI) for NFL teams. OCCI measures how effectively offenses create structural challenges and difficult decision-making situations for opposing defenses.

## 🏈 What is OCCI?

The Offensive Conflict Creation Index estimates how often and how intensely an offense forces a defense into structurally difficult situations. It analyzes multiple play-by-play factors including:

- **Motion & Tempo**: Pre-snap movement, shifts, and no-huddle usage
- **Formation Complexity**: Personnel groupings, shotgun vs under center, spread formations
- **Target Depth**: Vertical passing threats and field stretching
- **Play Action & Deception**: Play-action passes and RPO (Run-Pass Option) usage
- **Personnel Variety**: Diverse personnel packages and unexpected play calling
- **Situational Complexity**: Down-and-distance variety and game situation awareness

Higher OCCI scores indicate offenses that consistently force defenses to make difficult adjustments and decisions.

## 📊 Features

- **Play-by-Play OCCI Calculation**: Compute OCCI scores for every offensive play
- **Team-Level Aggregation**: Generate team statistics and rankings
- **Interactive Web Dashboard**: Visualize OCCI metrics with interactive charts
- **Component Analysis**: Break down OCCI into individual contributing factors
- **Comparative Analysis**: Compare teams and analyze pass vs run tendencies

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Install from source

```bash
# Clone the repository
git clone https://github.com/T111697/NFL-OCCI.git
cd NFL-OCCI

# Install dependencies
pip install -r requirements.txt

# Optional: Install as a package
pip install -e .
```

## 💻 Usage

### Command-Line Example

Run the example script to see OCCI calculations for the 2023 NFL season:

```bash
python example.py
```

This will:
1. Load play-by-play data from the 2023 NFL season
2. Calculate OCCI for each play
3. Generate team-level statistics
4. Display top and bottom teams by OCCI

### Python API

```python
from occi import OCCICalculator, load_nfl_data

# Load NFL play-by-play data
pbp_data = load_nfl_data(seasons=[2023])

# Initialize calculator
calculator = OCCICalculator(pbp_data)

# Calculate play-level OCCI
play_occi = calculator.calculate_play_occi()

# Calculate team-level statistics
team_stats = calculator.calculate_team_occi()

# Get full data with OCCI scores
play_data = calculator.get_play_data_with_occi()
```

### Web Application

Launch the interactive web dashboard:

```bash
python webapp/app.py
```

Then open your browser to `http://localhost:5000`

The web app provides:
- **Team Rankings**: Bar chart showing all teams ranked by average OCCI
- **Distribution Analysis**: Histogram of OCCI scores across all plays
- **Pass vs Run Comparison**: Box plots comparing OCCI for pass and run plays
- **Team Detail View**: Radar chart showing component breakdown for individual teams
- **Statistics Table**: Complete team statistics with rankings

## 📈 OCCI Methodology

OCCI is calculated as a weighted combination of six components:

| Component | Weight | Description |
|-----------|--------|-------------|
| Motion | 15% | Pre-snap movement and tempo (no-huddle, shifts) |
| Formation | 20% | Formation complexity (shotgun, personnel) |
| Target Depth | 20% | Passing depth and vertical threat |
| Play Action | 15% | Deceptive elements (play action, RPO) |
| Personnel | 15% | Personnel variety and unexpected play calls |
| Situational | 15% | Situational complexity (down, distance, field position) |

Each component is scored 0-1, then combined and normalized to a 0-100 scale.

### Component Details

**Motion Score**: Based on no-huddle usage and shotgun formations as proxies for pre-snap motion and tempo.

**Formation Score**: Evaluates formation complexity using shotgun vs under center, no-huddle, and formation variety.

**Target Depth Score**: For passing plays, uses air yards to measure vertical threat. Normalized to 0-1 scale with 50 yards as maximum.

**Play Action Score**: Estimates deceptive play calling using QB dropback patterns and play type.

**Personnel Score**: Measures play-calling variety and unpredictability based on down/distance expectations.

**Situational Score**: Accounts for game context including field position, down, score differential, and pressure situations.

## 📁 Project Structure

```
NFL-OCCI/
├── occi/                      # Main package
│   ├── __init__.py           # Package initialization
│   ├── calculator.py         # OCCI calculation logic
│   └── data_loader.py        # NFL data loading utilities
├── webapp/                    # Web application
│   ├── app.py                # Flask application
│   ├── templates/            # HTML templates
│   │   └── index.html        # Main dashboard page
│   └── static/               # Static assets (CSS, JS)
├── example.py                # Example usage script
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
└── README.md                 # This file
```

## 🔧 Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **nfl_data_py**: Access to NFL play-by-play data
- **flask**: Web application framework
- **plotly**: Interactive visualizations

## 📝 Data Source

This project uses open play-by-play data provided by [nfl_data_py](https://github.com/nfl-data-py/nfl_data_py), which aggregates data from various sources including NFL's Game Statistics and Information System (GSIS).

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest new features or components
- Improve documentation
- Submit pull requests

## 📄 License

This project is open source and available for educational and research purposes.

## 🙏 Acknowledgments

- NFL play-by-play data provided by nfl_data_py
- Inspired by advanced football analytics and defensive complexity research
- Built for football analytics enthusiasts and researchers

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Note**: OCCI is an experimental metric designed to capture offensive complexity. It should be used alongside other metrics for comprehensive team evaluation.