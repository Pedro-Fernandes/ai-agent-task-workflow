# AI Agent Task Workflow Template

A generic GitHub template repository for turning structured markdown task plans into GitHub issues.

## Philosophy

This repository is an AI-agent task planning and export system.

Task markdown files are planning artifacts used to:

- discuss changes with LLMs
- refine scope
- define acceptance criteria
- generate GitHub issues

After export, GitHub becomes the source of truth.

The repository intentionally does not duplicate:

- issue status
- implementation progress
- completion tracking

The repository manages one transition:

```text
Markdown task file -> GitHub issue
```

## What this template gives you

- `AGENTS.md` with operating instructions for AI coding agents.
- `docs/` with workflow, task authoring, label, and repository conventions.
- `.github/ISSUE_TEMPLATE/` for manually created GitHub issues.
- `tasks/pending/` for task files that have not been exported.
- `tasks/exported/` for task files that already created GitHub issues.
- `scripts/validate_tasks.py` to validate pending task metadata.
- `scripts/ensure_labels.py` to create missing GitHub labels before export.
- `scripts/create_github_issues.py` to create issues and move successful exports.

## Quick start

1. Create a new repository from this template.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Export a GitHub token with issue and label permissions:

```bash
export GITHUB_TOKEN="github_pat_your_token_here"
```

4. Validate pending task files:

```bash
python scripts/validate_tasks.py
```

5. Ensure labels exist:

```bash
python scripts/ensure_labels.py
```

6. Preview issue creation:

```bash
python scripts/create_github_issues.py --dry-run
```

7. Create GitHub issues:

```bash
python scripts/create_github_issues.py
```

Successful exports are updated with GitHub issue metadata and moved from `tasks/pending/` to `tasks/exported/`. Failed exports remain in `tasks/pending/`.

If the repository does not have a GitHub `origin` remote, pass `--repo owner/repo` to the label and issue scripts. The core workflow is:

```bash
python scripts/validate_tasks.py
python scripts/ensure_labels.py
python scripts/create_github_issues.py
```

## Task file format

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

## Acceptance Criteria
- [ ] Clear, testable criterion.
- [ ] Another clear, testable criterion.

## Implementation Notes
Useful constraints, links, or architectural hints.
```

## Expected Workflow

1. Human and AI discuss a feature.
2. AI generates task markdown files.
3. Tasks are placed into `tasks/pending/`.
4. Validation script runs.
5. Labels are ensured.
6. GitHub issues are created.
7. Exported tasks are moved to `tasks/exported/`.
8. All future work tracking happens in GitHub.

## Idempotency

Successful exports add these fields to task front matter before the file is moved:

```yaml
github_issue_url: "https://github.com/owner/repo/issues/123"
github_issue_number: 123
exported_at: "2026-05-19T12:00:00+00:00"
```

The export and label scripts skip task files that already contain `github_issue_url` or `github_issue_number`. This prevents accidental duplicate exports if an exported file is copied back into `tasks/pending/`.

## License

MIT. Replace this license if your project requires something else.
