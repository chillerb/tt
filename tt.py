#!/usr/bin/env python

import argparse
import datetime as dt
import csv

from pathlib import Path

APP_NAME = "tt"
CONFIG_PATH = Path(f"~/.config/{APP_NAME}/").expanduser()
DATA_PATH = Path(f"~/.local/share/{APP_NAME}/").expanduser()

FILE_NAME = "time.csv"
HEADER = ["datetime", "hours", "project", "message"]


def track(record, delimiter=","):
    DATA_PATH.mkdir(exist_ok=True)
    file_path = DATA_PATH / FILE_NAME
    write_header = not file_path.exists()
    with open(file_path, "a") as time_file:
        writer = csv.DictWriter(time_file, fieldnames=HEADER, delimiter=delimiter)
        if write_header:
            writer.writeheader()
        writer.writerow(record)


def vali_date(date_str, timespec="minutes"):
    if date_str == "now":
        date_time = dt.datetime.now()
    else:
        date_time = dt.datetime.fromisoformat(date_str)
    return date_time.isoformat(timespec=timespec)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="tt", description="A simple time tracking tool.")

    parser.add_argument("hours", type=float, default=1, help="hours")
    parser.add_argument("-p", "--project", type=str, help="project")
    parser.add_argument("-m", "--message", type=str, help="descriptive message")
    parser.add_argument("-t", "--time", default="now", type=str, help="datetime in isoformat")
    parser.add_argument("--delimiter", default=",", type=str, help="csv delimiter")

    args = parser.parse_args()

    record = {
        "datetime": vali_date(args.time),
        "hours": args.hours,
        "project": args.project,
        "message": args.message
    }

    track(record, delimiter=args.delimiter)
