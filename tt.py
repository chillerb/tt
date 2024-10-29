#!/usr/bin/env python

import argparse
import csv
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import subprocess

from pathlib import Path

APP_NAME = "tt"
CONFIG_PATH = Path(f"~/.config/{APP_NAME}/").expanduser()
DATA_PATH = Path(f"~/.local/share/{APP_NAME}/").expanduser()

FILE_NAME = "time.csv"
HEADER = ["datetime", "hours", "project", "message"]


def track(record, delimiter=","):
    """Write record to time.csv file."""
    DATA_PATH.mkdir(exist_ok=True)
    file_path = DATA_PATH / FILE_NAME
    write_header = not file_path.exists()
    with open(file_path, "a") as time_file:
        writer = csv.DictWriter(time_file, fieldnames=HEADER, delimiter=delimiter)
        if write_header:
            writer.writeheader()
        writer.writerow(record)


def report(from_date, to_date, output: Path, delimiter=","):
    """Process time records in [from_date,to_date] range and generate plots."""
    output.mkdir(exist_ok=True)
    file_path = DATA_PATH / FILE_NAME
    time_df = pd.read_csv(file_path, delimiter=delimiter)

    # parse datetimes and select from-to range
    time_df["datetime"] = pd.to_datetime(time_df["datetime"])
    time_df["date"] = time_df["datetime"].dt.date
    select_from = from_date <= time_df["datetime"]
    select_to = time_df["datetime"] <= to_date
    time_df = time_df.loc[select_from & select_to]

    # plot total
    title = f"{from_date} to {to_date}"
    time_df.groupby("project")["hours"].sum().plot.pie(title=title, legend=True, autopct="%d %%")
    plt.savefig(output / "total.png")

    # plot hours per day
    df = time_df.groupby(["date", "project"])["hours"].sum().unstack(fill_value=0)
    df.plot(kind="bar", stacked=True, title=title, ylabel="hours")
    plt.axhline(8, ls="--")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(output / "daily.png")


def open_time_vault():
    """Opens time.csv file."""
    subprocess.run(["open", DATA_PATH / FILE_NAME])


def vali_date(date_str, timespec="minutes"):
    """Checks if date_str is given in isoformat."""
    if date_str == "now":
        date_time = dt.datetime.now()
    else:
        date_time = dt.datetime.fromisoformat(date_str)
    return date_time.isoformat(timespec=timespec)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="tt", description="A simple time tracking tool.")

    parser.add_argument("--delimiter", default=",", type=str, help="csv delimiter")

    subparsers = parser.add_subparsers(dest="command")

    parser_track = subparsers.add_parser("track", aliases=["t"], help="Track spend hours.")

    parser_track.add_argument("hours", type=float, default=1, help="hours")
    parser_track.add_argument("-p", "--project", type=str, help="project")
    parser_track.add_argument("-m", "--message", type=str, help="descriptive message")
    parser_track.add_argument("-t", "--time", default="now", type=str, help="datetime in isoformat")

    parser_report = subparsers.add_parser("report", help="Visualize spend hours.")

    parser_report.add_argument("--from-date", default="now", type=str, help="from datetime")
    parser_report.add_argument("--to-date", default="now", type=str, help="to datetime")
    parser_report.add_argument("-o", "--output", default="report", type=Path, help="output directory")

    parser_open = subparsers.add_parser("open", help="Open the time.csv file for manual editing.")

    args = parser.parse_args()

    if args.command == "track" or args.command == "t":
        record = {
            "datetime": vali_date(args.time),
            "hours": args.hours,
            "project": args.project,
            "message": args.message
        }

        track(record, delimiter=args.delimiter)
    elif args.command == "report":
        from_date = dt.datetime.fromisoformat(vali_date(args.from_date))
        to_date = dt.datetime.fromisoformat(vali_date(args.to_date))

        report(from_date, to_date, args.output, args.delimiter)
    elif args.command == "open":
        open_time_vault()
