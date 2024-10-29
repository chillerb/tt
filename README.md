# tt

> A simple time tracking tool.

`tt` provides a CLI to write hours into a CSV file at `~/.local/share/tt/time.csv`.
Implemented in Python 3.12

## Installation

```sh
# install python requirements
pip install -r requirements.txt

# copies tt.py to ~/.local/bin/tt
bash install.sh
```

## Usage

```sh
# track 2 hours for project website
tt track 2 --project website -m "update images"

# create visual reports
tt report --from-date 2024-10-24 --to-date 2024-10-31
```
