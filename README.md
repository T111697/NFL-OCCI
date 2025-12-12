# Offensive Conflict Creation Index (OCCI) - Lite

OCCI-Lite is a public-data-only exploration of how NFL offenses create structural conflict for defenses. It packages a lightweight feature pipeline, a heuristic conflict score, team-level metrics, and a Streamlit UI for quick exploration.

## What OCCI is and is not

**What it is**
- A heuristic, play-level proxy for how much an offense stresses defensive structure.
- Built entirely on open play-by-play data (no tracking or proprietary sources).
- Designed for experimentation: tweak the heuristics, swap in better data, or fit a model using outcomes as weak labels.

**What it is not**
- A definitive measure of "scheme quality" or coaching skill.
- A replacement for film study or granular route/coverage data.
- A proprietary or paid-data product.

## Data sources and limitations

The project expects public play-by-play CSVs (e.g., nflfastR exports) stored under `data/raw/` as `pbp_YYYY.csv`. There is no download automation by default—`download.py` includes a clear TODO to wire in a suitable source. Without tracking data, conflict is inferred from personnel, motion, play action, target depth/location, situation, and defensive penalties that signal stress.

## Installation and setup

1. Create and activate a Python 3.10+ environment.
2. Install dependencies:

```bash
pip install -e .
```

3. Ensure raw play-by-play files exist in `data/raw/` (or implement the downloader).

## Usage

### Download data

Implement `src/conflict_map/data/download.py:download_season` with a public CSV source, then run it (or place CSVs manually) so files like `data/raw/pbp_2023.csv` are present.

### Run the CLI

```bash
python -m conflict_map.cli --seasons 2022 2023 --output-dir data/processed
```

This loads raw data, engineers features, computes play-level conflict scores, and writes:
- `data/processed/plays_with_conflict_scores.csv`
- `data/processed/team_game_occi.csv`
- `data/processed/team_season_occi.csv`

### Launch the Streamlit app

```bash
streamlit run src/conflict_map/app/streamlit_app.py
```

Select a season to view team-level OCCI and browse the underlying table. Ensure processed CSVs exist first.

## Roadmap and future ideas

- Per-route concept tagging and conflict typology.
- Opponent-specific matchup trees and defensive adjustment tracking.
- Interactive field visualizations showing attack locations and motion patterns.
- Model-based weighting of features using outcomes as weak labels.
