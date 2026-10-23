#!/usr/bin/env python3
"""Check a flashcard file before the user imports it.

Usage:
    python3 check_cards.py <deck-file> --format anki|quizlet|cloze

Errors (the import fails or produces broken cards):
  - a line has the wrong number of fields
  - a card has an empty side
  - two cards have the same front (ignoring case and spaces)
  - a cloze line has no {{c1::...}} marker

Warnings (the card works but is probably too big to study):
  - a front is longer than 200 characters

Exit code: 0 if there are no errors, 1 otherwise. Standard library only.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

MAX_FRONT = 200
CLOZE_MARKER = re.compile(r"\{\{c\d+::.+?\}\}")


def read_cards(path, deck_format):
    """Yield (line_number, fields) for every card line, skipping # headers and blank lines."""
    lines = path.read_text(encoding="utf-8").splitlines()
    for number, line in enumerate(lines, start=1):
        if not line.strip() or line.startswith("#"):
            continue
        if deck_format == "anki":
            yield number, next(csv.reader([line]))
        else:
            yield number, line.split("\t")


def check(path, deck_format):
    """Return (errors, warnings, card_count)."""
    errors, warnings = [], []
    expected_fields = 1 if deck_format == "cloze" else 2
    seen_fronts = {}
    count = 0

    for number, fields in read_cards(path, deck_format):
        count += 1
        if len(fields) != expected_fields:
            errors.append(f"line {number}: has {len(fields)} fields, expected {expected_fields}")
            continue
        if any(not field.strip() for field in fields):
            errors.append(f"line {number}: a side is empty")
            continue

        front = fields[0]
        if deck_format == "cloze" and not CLOZE_MARKER.search(front):
            errors.append(f"line {number}: no {{{{c1::...}}}} marker")
        key = " ".join(front.lower().split())
        if key in seen_fronts:
            errors.append(f"line {number}: same front as line {seen_fronts[key]}")
        else:
            seen_fronts[key] = number
        if len(front) > MAX_FRONT:
            warnings.append(f"line {number}: front is {len(front)} characters (aim for under {MAX_FRONT})")

    if count == 0:
        errors.append("no cards found")
    return errors, warnings, count


def main():
    parser = argparse.ArgumentParser(description="Check a flashcard file before importing it.")
    parser.add_argument("deck", type=Path, help="the .csv or .txt deck file")
    parser.add_argument("--format", choices=["anki", "quizlet", "cloze"], required=True)
    args = parser.parse_args()

    if not args.deck.is_file():
        print(f"ERROR: {args.deck} not found")
        return 1

    errors, warnings, count = check(args.deck, args.format)
    for error in errors:
        print(f"error:   {error}")
    for warning in warnings:
        print(f"warning: {warning}")
    print(f"{count} card(s), {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
