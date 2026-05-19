#!/usr/bin/env python3
"""Create GitHub issues from markdown task files.

Each markdown task file must contain YAML front matter with at least:

---
title: "Issue title"
labels: ["agent-ready"]
---

The remaining markdown body becomes the GitHub issue body.

Important: this script creates any missing labels before creating issues.
GitHub rejects issue creation when a requested label does not exist.
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests
import yaml


DEFAULT_LABEL_COLOR = "ededed"
DEFAULT_LABEL_DESCRIPTION = "Created automatically by the AI agent task workflow."


@dataclass(frozen=True)
class TaskIssue:
    source_file: Path
    title: str
    body: str
    labels: list[str]
    assignees: list[str]
    milestone: str | None


@dataclass(frozen=True)
class LabelDefinition:
    name: str
    color: str = DEFAULT_LABEL_COLOR
    description: str = DEFAULT_LABEL_DESCRIPTION


class TaskParseError(ValueError):
    pass


def github_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def parse_front_matter(content: str, path: Path) -> tuple[dict[str, Any], str]:
    if not content.startswith("---\n"):
        raise TaskParseError(f"{path}: missing YAML front matter starting with ---")

    try:
        _, raw_front_matter, body = content.split("---", 2)
    except ValueError as exc:
        raise TaskParseError(f"{path}: invalid YAML front matter block") from exc

    metadata = yaml.safe_load(raw_front_matter) or {}
    if not isinstance(metadata, dict):
        raise TaskParseError(f"{path}: front matter must be a YAML mapping")

    return metadata, body.strip()


def normalize_string_list(value: Any, field_name: str, path: Path) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise TaskParseError(f"{path}: '{field_name}' must be a list of strings")
    return [item.strip() for item in value if item.strip()]


def load_task(path: Path) -> TaskIssue:
    metadata, body = parse_front_matter(path.read_text(encoding="utf-8"), path)

    title = metadata.get("title")
    if not isinstance(title, str) or not title.strip():
        raise TaskParseError(f"{path}: 'title' is required and must be a string")

    labels = normalize_string_list(metadata.get("labels"), "labels", path)
    assignees = normalize_string_list(metadata.get("assignees"), "assignees", path)

    milestone = metadata.get("milestone")
    if milestone is not None and not isinstance(milestone, str):
        raise TaskParseError(f"{path}: 'milestone' must be a string when provided")

    issue_body = f"{body}\n\n---\nCreated from `{path.as_posix()}`."

    return TaskIssue(
        source_file=path,
        title=title.strip(),
        body=issue_body,
        labels=labels,
        assignees=assignees,
        milestone=milestone,
    )


def discover_task_files(tasks_path: Path) -> list[Path]:
    if tasks_path.is_file():
        return [tasks_path]
    if not tasks_path.exists():
        raise FileNotFoundError(f"Task path does not exist: {tasks_path}")
    return sorted(tasks_path.glob("*.md"))


def load_label_definitions(path: Path | None) -> dict[str, LabelDefinition]:
    """Load optional label metadata from YAML.

    Supported formats:

    labels:
      - name: agent-ready
        color: 0e8a16
        description: Ready for an AI agent

    Or:

    agent-ready:
      color: 0e8a16
      description: Ready for an AI agent
    """
    if path is None or not path.exists():
        return {}

    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise TaskParseError(f"{path}: label definition file must be a YAML mapping")

    items = raw.get("labels", raw)
    definitions: dict[str, LabelDefinition] = {}

    if isinstance(items, list):
        iterable = items
    elif isinstance(items, dict):
        iterable = [{"name": name, **(value or {})} for name, value in items.items()]
    else:
        raise TaskParseError(f"{path}: labels must be a list or mapping")

    for item in iterable:
        if not isinstance(item, dict):
            raise TaskParseError(f"{path}: each label definition must be a mapping")
        name = item.get("name")
        if not isinstance(name, str) or not name.strip():
            raise TaskParseError(f"{path}: each label definition requires a name")
        color = str(item.get("color", DEFAULT_LABEL_COLOR)).lstrip("#")
        description = str(item.get("description", DEFAULT_LABEL_DESCRIPTION))
        definitions[name.strip()] = LabelDefinition(name=name.strip(), color=color, description=description)

    return definitions


def list_existing_labels(repo: str, token: str) -> set[str]:
    labels: set[str] = set()
    page = 1
    while True:
        response = requests.get(
            f"https://api.github.com/repos/{repo}/labels",
            headers=github_headers(token),
            params={"per_page": 100, "page": page},
            timeout=30,
        )
        response.raise_for_status()
        batch = response.json()
        if not batch:
            break
        labels.update(label["name"] for label in batch)
        page += 1
    return labels


def create_label(repo: str, token: str, definition: LabelDefinition) -> None:
    response = requests.post(
        f"https://api.github.com/repos/{repo}/labels",
        headers=github_headers(token),
        json={
            "name": definition.name,
            "color": definition.color,
            "description": definition.description,
        },
        timeout=30,
    )
    response.raise_for_status()


def ensure_labels_exist(
    repo: str,
    token: str,
    required_labels: set[str],
    label_definitions: dict[str, LabelDefinition],
) -> None:
    """Create missing labels before any issue is created."""
    if not required_labels:
        return

    existing_labels = list_existing_labels(repo, token)
    missing_labels = sorted(required_labels - existing_labels)

    for label_name in missing_labels:
        definition = label_definitions.get(
            label_name,
            LabelDefinition(name=label_name),
        )
        create_label(repo, token, definition)
        print(f"Created missing label: {label_name}")


def get_milestone_number(repo: str, token: str, milestone_title: str) -> int | None:
    url = f"https://api.github.com/repos/{repo}/milestones"
    response = requests.get(url, headers=github_headers(token), params={"state": "all"}, timeout=30)
    response.raise_for_status()
    for milestone in response.json():
        if milestone.get("title") == milestone_title:
            return milestone.get("number")
    return None


def create_issue(repo: str, token: str, task: TaskIssue) -> str:
    payload: dict[str, Any] = {
        "title": task.title,
        "body": task.body,
        "labels": task.labels,
        "assignees": task.assignees,
    }

    if task.milestone:
        milestone_number = get_milestone_number(repo, token, task.milestone)
        if milestone_number is None:
            raise RuntimeError(
                f"Milestone '{task.milestone}' was not found in {repo}. "
                "Create it first or remove it from the task file."
            )
        payload["milestone"] = milestone_number

    response = requests.post(
        f"https://api.github.com/repos/{repo}/issues",
        headers=github_headers(token),
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["html_url"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create GitHub issues from markdown task files.")
    parser.add_argument("--repo", required=True, help="GitHub repository in owner/name format.")
    parser.add_argument("--tasks", required=True, help="Task markdown file or directory containing .md files.")
    parser.add_argument("--dry-run", action="store_true", help="Print issues and required labels without creating them.")
    parser.add_argument(
        "--labels-file",
        default=".github/labels.yml",
        help="Optional YAML file with label colors/descriptions. Defaults to .github/labels.yml.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    tasks_path = Path(args.tasks)

    try:
        task_files = discover_task_files(tasks_path)
        tasks = [load_task(path) for path in task_files]
        label_definitions = load_label_definitions(Path(args.labels_file) if args.labels_file else None)
    except (OSError, TaskParseError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not tasks:
        print(f"No markdown task files found in {tasks_path}")
        return 0

    required_labels = {label for task in tasks for label in task.labels}

    if args.dry_run:
        print("[dry-run] Required labels will be ensured before issues are created:")
        for label in sorted(required_labels):
            definition = label_definitions.get(label, LabelDefinition(name=label))
            print(f"          {definition.name} color={definition.color} description={definition.description!r}")
        print()
        for task in tasks:
            print(f"[dry-run] {task.source_file}: {task.title}")
            print(f"          labels={task.labels} assignees={task.assignees} milestone={task.milestone}")
        return 0

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable is required.", file=sys.stderr)
        return 1

    try:
        ensure_labels_exist(args.repo, token, required_labels, label_definitions)
    except requests.HTTPError as exc:
        response_text = exc.response.text if exc.response is not None else str(exc)
        print(f"Error ensuring labels before issue creation: {response_text}", file=sys.stderr)
        return 1

    for task in tasks:
        try:
            issue_url = create_issue(args.repo, token, task)
            print(f"Created: {issue_url}")
        except requests.HTTPError as exc:
            response_text = exc.response.text if exc.response is not None else str(exc)
            print(f"Error creating issue for {task.source_file}: {response_text}", file=sys.stderr)
            return 1
        except RuntimeError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
