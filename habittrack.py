#!/usr/bin/env python3
"""HabitTrack - a tiny habit tracker that stores data in habits.json.

Usage:
    python3 habittrack.py add --name "Reading"
    python3 habittrack.py done --name "Reading" --date 2026-11-10
    python3 habittrack.py list
    python3 habittrack.py streak --name "Reading"

Standard library only.
"""

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

DATA_FILE = Path("habits.json")


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(2)


def load_data():
    if not DATA_FILE.exists():
        return {}
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        fail(f"{DATA_FILE} is corrupted and could not be read as JSON.")
    if not isinstance(data, dict):
        fail(f"{DATA_FILE} has an unexpected format and could not be read.")
    return data


def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def parse_date(text):
    try:
        return date.fromisoformat(text)
    except ValueError:
        fail(f"invalid date '{text}' (expected YYYY-MM-DD).")


def habit_dates(data, name):
    if name not in data:
        fail(f"unknown habit '{name}'. Add it first with: add --name \"{name}\"")
    return {date.fromisoformat(d) for d in data[name]}


def current_streak(done_dates):
    """Length of the consecutive-day run ending at the latest done date.

    The streak is broken (0) when the latest done date is older than
    yesterday.
    """
    if not done_dates:
        return 0
    latest = max(done_dates)
    if latest < date.today() - timedelta(days=1):
        return 0
    streak = 0
    day = latest
    while day in done_dates:
        streak += 1
        day -= timedelta(days=1)
    return streak


def cmd_add(args):
    data = load_data()
    if args.name in data:
        fail(f"habit '{args.name}' already exists.")
    data[args.name] = []
    save_data(data)
    print(f"Habit added: {args.name}")


def cmd_done(args):
    data = load_data()
    done = habit_dates(data, args.name)
    day = parse_date(args.date) if args.date else date.today()
    done.add(day)
    data[args.name] = sorted(d.isoformat() for d in done)
    save_data(data)
    print(f"Marked {args.name} done on {day.isoformat()}")


def cmd_list(args):
    data = load_data()
    if not data:
        print("No habits yet. Add one with: add --name \"Reading\"")
        return
    for name in sorted(data):
        done = {date.fromisoformat(d) for d in data[name]}
        last = max(done).isoformat() if done else "never"
        print(
            f"{name}: {len(done)} days, current streak "
            f"{current_streak(done)}, last done {last}"
        )


def cmd_streak(args):
    data = load_data()
    done = habit_dates(data, args.name)
    last = max(done).isoformat() if done else "never"
    print(f"{args.name}: {len(done)} days total")
    print(f"Current streak: {current_streak(done)}")
    print(f"Last done: {last}")
    print("Last 7 days:")
    today = date.today()
    for offset in range(6, -1, -1):
        day = today - timedelta(days=offset)
        mark = "x" if day in done else " "
        print(f"{day.isoformat()} [{mark}]")


def main():
    parser = argparse.ArgumentParser(
        prog="habittrack",
        description="Track daily habits in a local habits.json file.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="create a new habit")
    p_add.add_argument("--name", required=True, help="habit name")
    p_add.set_defaults(func=cmd_add)

    p_done = sub.add_parser("done", help="mark a habit done for a date")
    p_done.add_argument("--name", required=True, help="habit name")
    p_done.add_argument(
        "--date", default=None, help="YYYY-MM-DD (default: today)"
    )
    p_done.set_defaults(func=cmd_done)

    p_list = sub.add_parser("list", help="list all habits and streaks")
    p_list.set_defaults(func=cmd_list)

    p_streak = sub.add_parser("streak", help="show streak detail for a habit")
    p_streak.add_argument("--name", required=True, help="habit name")
    p_streak.set_defaults(func=cmd_streak)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
