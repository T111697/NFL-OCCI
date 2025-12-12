"""
Command line interface for computing OCCI from raw play by play.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from .data.load import load_raw_multiple_seasons
from .pipeline.updates import append_weekly_updates, build_from_ranges, run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute Offensive Conflict Creation Index (OCCI)")
    parser.add_argument(
        "--seasons",
        nargs="+",
        type=int,
        help="Explicit seasons to include, e.g. 2019 2020 2021. Overrides --base-start/--base-end.",
    )
    parser.add_argument(
        "--base-start",
        type=int,
        default=2019,
        help="First season to include in the historical baseline (default: 2019).",
    )
    parser.add_argument(
        "--base-end",
        type=int,
        default=2025,
        help="Last fully completed season to include in the historical baseline (default: 2025).",
    )
    parser.add_argument(
        "--latest-season",
        type=int,
        default=2026,
        help="In-progress or future season to tack on top of the baseline (default: 2026).",
    )
    parser.add_argument(
        "--latest-weeks",
        nargs="+",
        type=int,
        help="Optional list of week numbers for the latest season when only weekly exports are available.",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path("data/processed"), help="Directory for output CSVs"
    )
    parser.add_argument(
        "--weekly-append",
        nargs=2,
        metavar=("SEASON", "WEEKS"),
        help=(
            "Append weekly files for a season to existing processed outputs without recomputing the baseline. "
            "WEEKS should be a comma-separated list, e.g. 2026 1,2,3"
        ),
    )
    args = parser.parse_args()
    if args.weekly_append:
        season = int(args.weekly_append[0])
        weeks = [int(w.strip()) for w in args.weekly_append[1].split(",") if w.strip()]
        append_weekly_updates(args.output_dir, season=season, weeks=weeks)
        return

    if args.seasons:
        df_raw = load_raw_multiple_seasons(args.seasons)
        run_pipeline(df_raw, output_dir=args.output_dir, metadata={"explicit_seasons": args.seasons})
        return

    base_seasons = range(args.base_start, args.base_end + 1)
    latest_season = args.latest_season
    latest_weeks = args.latest_weeks

    build_from_ranges(base_seasons, latest_season=latest_season, latest_weeks=latest_weeks, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
