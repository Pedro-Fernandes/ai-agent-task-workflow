#!/usr/bin/env python3
"""Validate pending task markdown files without creating GitHub issues."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from create_github_issues import DEFAULT_TASKS_PATH, TaskParseError, discover_task_files, load_task


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate markdown task files.")
    parser.add_argument(
        "tasks",
        nargs="?",
        default=str(DEFAULT_TASKS_PATH),
        help="Task markdown file or directory containing .md files. Defaults to tasks/pending.",
    )
    args = parser.parse_args()

    try:
        task_files = discover_task_files(Path(args.tasks))
        for path in task_files:
            load_task(path)
            print(f"OK: {path}")
    except (OSError, TaskParseError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
