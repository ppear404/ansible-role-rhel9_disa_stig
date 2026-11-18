#!/usr/bin/env python3
"""Summarize saved Evaluate-STIG JSON or CKLB files without embedding host data."""
import argparse
import collections
import json
from pathlib import Path


def records(path):
    text = path.read_text()
    if path.suffix.lower() == '.cklb':
        checklist = json.loads(text)
        return [rule for stig in checklist['stigs'] for rule in stig['rules']]
    # Evaluate-STIG emits banner text before its console JSON array.
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != '[':
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, list) and value and all(isinstance(r, dict) and 'Status' in r for r in value):
            return value
    raise ValueError(f'No evaluator JSON records found in {path.name}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', type=Path, nargs='+')
    args = parser.parse_args()
    for path in args.files:
        counts = collections.Counter(r.get('Status', r.get('status')) for r in records(path))
        print(path.name + ': ' + ', '.join(f'{key}={value}' for key, value in sorted(counts.items())))


if __name__ == '__main__':
    main()
