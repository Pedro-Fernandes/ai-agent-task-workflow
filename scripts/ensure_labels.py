#!/usr/bin/env python3
"""Ensure GitHub labels required by pending task files exist."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from create_github_issues import (
    DEFAULT_TASKS_PATH,
    LabelDefinition,
    RequestHTTPError,
    TaskParseError,
    ensure_labels_exist,
    infer_repo_from_git_remote,
    load_exportable_tasks,
    load_label_definitions,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ensure GitHub labels required by pending task files exist.")
    parser.add_argument(
        "--repo",
        help="GitHub repository in owner/name format. Defaults to the GitHub origin remote.",
    )
    parser.add_argument(
        "--tasks",
        default=str(DEFAULT_TASKS_PATH),
        help="Task markdown file or directory containing .md files. Defaults to tasks/pending.",
    )
    parser.add_argument(
        "--labels-file",
        default=".github/labels.yml",
        help="Optional YAML file with label colors/descriptions. Defaults to .github/labels.yml.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print required labels without creating them.")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        tasks, skipped = load_exportable_tasks(Path(args.tasks))
        label_definitions = load_label_definitions(Path(args.labels_file) if args.labels_file else None)
    except (OSError, TaskParseError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    for path in skipped:
        print(f"Skipped already exported task: {path}")

    required_labels = {label for task in tasks for label in task.labels}
    if not required_labels:
        print("No labels required by exportable pending tasks.")
        return 0

    if args.dry_run:
        for label in sorted(required_labels):
            definition = label_definitions.get(label, LabelDefinition(name=label))
            print(f"{definition.name} color={definition.color} description={definition.description!r}")
        return 0

    repo = args.repo or infer_repo_from_git_remote()
    if not repo:
        print("Error: --repo is required when a GitHub origin remote cannot be inferred.", file=sys.stderr)
        return 1

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable is required.", file=sys.stderr)
        return 1

    try:
        ensure_labels_exist(repo, token, required_labels, label_definitions)
    except RequestHTTPError as exc:
        response_text = exc.response.text if exc.response is not None else str(exc)
        print(f"Error ensuring labels: {response_text}", file=sys.stderr)
        return 1

    print("Required labels are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
