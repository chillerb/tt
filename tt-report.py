#!/usr/bin/env python

import argparse
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from pathlib import Path

APP_NAME = "tt"
CONFIG_PATH = Path(f"~/.config/{APP_NAME}/").expanduser()
DATA_PATH = Path(f"~/.local/share/{APP_NAME}/").expanduser()

FILE_NAME = "time.csv"


def plot_daily(time_df):
    bottom = 0
    for project, project_df in time_df.groupby("project"):
        hours_per_day = project_df.groupby("date")["hours"].sum()
        plt.bar(hours_per_day.index, hours_per_day, bottom=bottom, label=project)
        bottom += hours_per_day
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.axhline(8, ls="--")
    plt.ylabel("hours")
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()


def report(from_date, to_date, output: Path, delimiter=","):
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
    plt.figure()
    plot_daily(time_df)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output / "daily.png")


def vali_date(date_str, timespec="minutes"):
    if date_str == "now":
        date_time = dt.datetime.now()
    else:
        date_time = dt.datetime.fromisoformat(date_str)
    return date_time.isoformat(timespec=timespec)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="tt-report", description="Visualize tracked time.")

    parser.add_argument("--from-date", default="now", type=str, help="from datetime")
    parser.add_argument("--to-date", default="now", type=str, help="to datetime")
    parser.add_argument("-o", "--output", default="report", type=Path, help="output directory")
    parser.add_argument("--delimiter", default=",", type=str, help="csv delimiter")

    args = parser.parse_args()

    from_date = dt.datetime.fromisoformat(vali_date(args.from_date))
    to_date = dt.datetime.fromisoformat(vali_date(args.to_date))

    report(from_date, to_date, args.output)
