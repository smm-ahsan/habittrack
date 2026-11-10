# HabitTrack

A tiny command-line habit tracker that keeps your data in a local `habits.json` file.

## Features

- Add habits and mark them done for any date (today by default)
- Automatic streak counting with a simple rule: miss more than a day and the streak breaks
- A last-7-days view so you can see your week at a glance
- No accounts, no cloud, no dependencies - your data never leaves your folder

## Requirements

- Python 3
- Standard library only, nothing to install

## Usage

Create a habit:

```bash
python3 habittrack.py add --name "Reading"
```

Mark it done (the date is optional and defaults to today):

```bash
python3 habittrack.py done --name "Reading" --date 2026-11-10
```

See all habits with totals and current streaks:

```bash
python3 habittrack.py list
```

See one habit in detail, including the last 7 days:

```bash
python3 habittrack.py streak --name "Reading"
```

## Data

All data lives in `habits.json` in the current folder. The file is created
automatically the first time you add a habit. Move or copy that file to move
your history; delete it to start over.

## License

MIT - see [LICENSE](LICENSE).
