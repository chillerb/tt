#!/usr/bin/env python

import argparse
import datetime as dt
import csv

from pathlib import Path

APP_NAME = "tt"
CONFIG_PATH = Path(f"~/.config/{APP_NAME}/")
DATA_PATH = Path(f"~/.local/share/{APP_NAME}/")
FILE_NAME = "time.csv"

HEADER = ["date", "time", "hours", "project", "message"]


def track(record):
    file_path = DATA_PATH / FILE_NAME
    write_header = not file_path.exists()
    with open(file_path, "a") as time_file:
        writer = csv.DictWriter(time_file, fieldnames=HEADER)
        if write_header:
            writer.writeheader()
        writer.writerow(record)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="tt", description="A simple time tracking tool.", add_help=False)

    parser.add_argument("-h", "--hours", type=float, help="hours")
    parser.add_argument("-p", "--project", type=str, help="project")
    parser.add_argument("-m", "--message", type=str, help="descriptive message")
    parser.add_argument("-d", "--date", default="today", type=str, help="date")
    parser.add_argument("-t", "--time", default="now", type=str, help="hours spend")

    args = parser.parse_args()

    record = {
        "date": args.date,
        "time": args.time,
        "hours": args.hours,
        "project": args.project,
        "message": args.message
    }

    track(record)
