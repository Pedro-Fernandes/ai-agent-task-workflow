# Conversation-to-Issue Workflow for AI Agents

A lightweight workflow for turning human and LLM conversations into clear markdown tasks, then exporting those tasks into GitHub issues that drive coding work.

This repository exists for the messy middle between "we talked about a change" and "an agent can implement this safely." It gives humans and LLMs a shared place to shape ideas into concrete work: context, scope, non-goals, acceptance criteria, and validation notes. Once a task is ready, the repository exports it to GitHub, where implementation tracking belongs.

## Philosophy

Good AI-assisted development starts before code. Humans and LLMs need room to discuss intent, tradeoffs, constraints, and acceptance criteria before asking a coding agent to modify a repository.

This template treats markdown task files as planning artifacts. They are useful because they are easy to read, easy to revise during conversation, and structured enough to become GitHub issues.

The lifecycle is intentionally narrow:

```text
conversation -> refined markdown task -> GitHub issue
```

After export, GitHub becomes the source of truth for execution. This repository does not duplicate:

- issue status
- implementation progress
- pull request state
- completion tracking

## What This Template Gives You

- `tasks/pending/` for task files still being prepared for export.
- `tasks/exported/` for task files that already produced GitHub issues.
- `tasks/TASK_TEMPLATE.md` for consistent task structure.
- `AGENTS.md` with instructions for AI coding agents.
- `docs/` with workflow, task authoring, label, and repository conventions.
- `.github/ISSUE_TEMPLATE/` for manually created GitHub issues.
- `scripts/validate_tasks.py` to validate task metadata before export.
- `scripts/create_github_issues.py` to create missing labels, create issues, add export metadata, and move successful exports.

## Expected Workflow

1. A human and an LLM discuss a feature, bug, cleanup, or product idea.
2. The LLM drafts one or more markdown task files.
3. The human and LLM refine those tasks until the scope is clear.
4. Refined tasks are placed in `tasks/pending/`.
5. The tasks are validated.
6. The export script creates any missing GitHub labels.
7. The export script creates GitHub issues.
8. Successfully exported task files are moved to `tasks/exported/`.
9. All future work tracking happens in GitHub issues and pull requests.

## Quick Start

1. Create a new repository from this template.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Export a GitHub token with issue and label permissions:

```bash
export GITHUB_TOKEN="github_pat_your_token_here"
```

4. Add or refine task files in `tasks/pending/`.
5. Validate pending tasks:

```bash
python scripts/validate_tasks.py
```

6. Preview the export:

```bash
python scripts/create_github_issues.py --dry-run
```

7. Create GitHub issues:

```bash
python scripts/create_github_issues.py
```

If the repository does not have a GitHub `origin` remote, pass `--repo owner/repo` to the export script.

## Task File Format

Each task is a markdown file with YAML front matter:

```markdown
---
title: "Add repository health check endpoint"
labels: ["backend", "agent-ready"]
milestone: "MVP"
assignees: []
---

## Context
Why this task exists.

## Goal
What needs to be achieved.

## Scope
- What should change.

## Non-Goals
- What should not change.

## Acceptance Criteria
- [ ] Clear, testable criterion.
- [ ] Another clear, testable criterion.

## Implementation Notes
Useful constraints, links, or architectural hints.

## Validation
How to verify the result.
```

## Export Behavior

`scripts/create_github_issues.py` reads exportable tasks from `tasks/pending/`. Before creating issues, it collects every label referenced by those tasks and creates any missing labels in GitHub.

For each successful export, the script adds GitHub metadata to the task front matter:

```yaml
github_issue_url: "https://github.com/owner/repo/issues/123"
github_issue_number: 123
exported_at: "2026-05-19T12:00:00+00:00"
```

Then it moves the task file to `tasks/exported/`.

Failed exports stay in `tasks/pending/` so they can be fixed and retried.

## Idempotency

The export script skips task files that already contain `github_issue_url` or `github_issue_number`. This prevents accidental duplicate exports if an exported task is copied back into `tasks/pending/`.

There is no hidden state. The filesystem and task front matter explain what has happened.

## License

MIT. Replace this license if your project requires something else.
