# Offensive Conflict Creation Index (OCCI) – Lite

OCCI-Lite is a public-data-only exploration of how NFL offenses create structural conflict for defenses. It includes a lightweight feature pipeline, heuristic conflict score, team-level aggregations, and a Streamlit explorer so you can quickly compare offenses without proprietary tracking data.

## Overview
- Engineer motion, personnel, target depth, and situation features from public play-by-play CSVs stored under `data/raw/` (e.g., `pbp_2023.csv`).
- Compute play-level conflict scores and aggregate them to team-game and team-season summaries via the CLI.
- Visualize the outputs in a wide-layout Streamlit app with league pulse, multi-season trends, and per-team game charts.
- Ship notebook-friendly CSVs so you can experiment with weighting, alternative heuristics, or outcome-based modeling.

## Quickstart
1. **Install dependencies** (Python 3.10+ recommended):
   ```bash
   pip install -e .
   ```

2. **Prepare raw data.** Place nflfastR-style play-by-play CSVs in `data/raw/` named `pbp_YYYY.csv`. The stub at `src/conflict_map/data/download.py` can be wired up to your preferred public source if you want to automate downloads.

3. **Compute conflict scores and aggregates.**
   ```bash
   # Baseline: seasons 2019–2025 plus the latest (default 2026) season
   python -m conflict_map.cli --output-dir data/processed
   ```
   Need something custom? Override the defaults:
   ```bash
   # Only historical seasons
   python -m conflict_map.cli --seasons 2020 2021 2022 --output-dir data/processed

   # Historical baseline plus specific weeks from an in-progress season
   python -m conflict_map.cli --base-start 2019 --base-end 2025 --latest-season 2026 --latest-weeks 1 2 3
   ```
   Each run writes:
   - `data/processed/plays_with_conflict_scores.csv`
   - `data/processed/team_game_occi.csv`
   - `data/processed/team_season_occi.csv`
   - `data/processed/occi_run_metadata.json` describing the coverage

4. **Explore in Streamlit.**
   ```bash
   streamlit run src/conflict_map/app/streamlit_app.py
   ```
   The app will use demo data if processed CSVs are missing, but it will prompt you to generate your own outputs via the CLI.

## Project layout
- `src/conflict_map/cli.py`: End-to-end pipeline from raw play-by-play to processed CSVs.
- `src/conflict_map/pipeline/updates.py`: Helpers for baseline builds and weekly append workflows.
- `src/conflict_map/features/`: Feature engineering helpers.
- `src/conflict_map/model/conflict_score.py`: Heuristic conflict scoring logic.
- `src/conflict_map/metrics/`: Team-game and team-season aggregations.
- `src/conflict_map/app/streamlit_app.py`: Interactive explorer consuming the processed CSVs.
- `data/raw/`: Expected location for season play-by-play CSVs.
- `data/processed/`: CLI outputs consumed by the app and notebooks.
- `tests/`: Unit tests around feature building, scoring, and metrics.

## Legacy components
Earlier iterations of this project live alongside the current pipeline for reference:
- `occi/` and `example.py` contain the original package and script built around a Flask app. They are kept for archival purposes but are not the recommended entry point.
- `webapp/` hosts the legacy Flask dashboard. New UI work should target the Streamlit app instead.

Prefer the `conflict_map` modules, CLI, and Streamlit explorer for any new development.

## Data freshness and weekly updates
- **Pull historical data (2019–2025)**: by default the CLI loads these seasons from `data/raw/pbp_YYYY.csv(.gz)`. Use `src/conflict_map/data/download.py` or your own scripts to fetch nflverse exports into that directory.
- **Attach the latest season (2026-ready)**: provide a full `pbp_2026.csv(.gz)` in `data/raw/` *or* drop weekly slices under `data/raw/weekly/pbp_2026_week_<week>.csv(.gz)`.
- **Append new weeks without recomputing**: once the baseline is built, stitch in fresh weeks via:
  ```bash
  python -m conflict_map.cli --weekly-append 2026 4,5  # weeks 4 and 5 only
  ```
  This updates the processed CSVs in place and refreshes `occi_run_metadata.json` so the Streamlit app displays the coverage window.

## Contributing
Issues and pull requests are welcome—feel free to propose improved heuristics, new visualizations, or data-loading utilities.

## License
This project is open source and available for educational and research purposes under the terms of the LICENSE file.
