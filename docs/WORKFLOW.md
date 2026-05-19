# AI-Agent Task Export Workflow

This workflow is built around a narrow boundary: markdown task files are planning artifacts in this repository, and GitHub issues are execution artifacts in a target implementation repository.

## Lifecycle

```text
idea -> pending task -> GitHub issue in target repo -> exported task
```

After export, implementation work, status, pull requests, and completion are tracked in the target GitHub repository.

## 1. Discuss and draft

Humans and AI agents discuss the feature, bug, or maintenance need. Capture the result as a markdown task file.

The target repository can be stated at the start of the conversation or later. Before export, it must be explicit in `owner/repo` format.

## 2. Place tasks in pending

Put unexported task files in `tasks/pending/`. A pending task should include:

- Context.
- Goal.
- Scope.
- Non-goals.
- Acceptance criteria.
- Implementation notes.
- Validation plan.

## 3. Validate pending tasks

Run:

```bash
python scripts/validate_tasks.py
```

The script validates task metadata and markdown front matter without making network calls.

## 4. Create GitHub issues

Preview first:

```bash
python scripts/create_github_issues.py --repo owner/repo --dry-run
```

Then export:

```bash
python scripts/create_github_issues.py --repo owner/repo
```

The script reads `tasks/pending/`, creates one GitHub issue per exportable task in the target repository, writes the issue URL and number into task front matter, and moves successful exports into `tasks/exported/`.

The script also creates any missing labels before issue creation. GitHub rejects issue creation when a requested label does not exist, so label handling is built into export.

Failed task files remain in `tasks/pending/`.

## 5. Work in GitHub

Use GitHub issues and pull requests in the target repository for all future tracking. This repository does not track local in-progress, done, closed, or completed state.

Recommended branch naming:

```text
agent/<issue-number>-short-description
```

Each pull request should link its issue using `Closes #123` or `Fixes #123`.

## Idempotency

The export script adds `github_issue_url`, `github_issue_number`, and `exported_at` to successfully exported task files. Any task file containing `github_issue_url` or `github_issue_number` is skipped by future export runs.
