#!/usr/bin/env python3
"""Reject common accidental lab artifacts and credential material in public source."""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    'private key': re.compile(r'^-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----', re.M),
    'GitHub token': re.compile(r'\bgh[pousr]_[A-Za-z0-9]{20,}\b'),
    'AWS access key': re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    'private IPv4 address': re.compile(
        r'\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b'),
    'local project path': re.compile(r'/home/[^\s/]+/projects/'),
}


def candidates():
    result = subprocess.run(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
                            cwd=ROOT, capture_output=True, check=False)
    if result.returncode:
        return [p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts]
    return sorted({ROOT / name.decode() for name in result.stdout.split(b'\0') if name})


def main():
    errors = []
    checked = 0
    for path in candidates():
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative.startswith('tests/evidence/') and relative != 'tests/evidence/.gitkeep':
            errors.append(f'{relative}: raw assessment artifact')
        if relative.startswith(('files/evaluate-stig-', 'files/U_RHEL_')) or path.suffix in {'.ckl', '.cklb'}:
            errors.append(f'{relative}: downloaded tooling or private checklist')
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            errors.append(f'{relative}: unreviewed binary file')
            continue
        checked += 1
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                errors.append(f'{relative}: {label}')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'Public-content checks passed for {checked} files (not a comprehensive secret scanner).')


if __name__ == '__main__':
    main()
