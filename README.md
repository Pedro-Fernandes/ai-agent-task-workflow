# AI Agent Task Workflow Template

A generic GitHub template repository for running AI-assisted development through structured markdown tasks, agent instructions, and repeatable GitHub issue creation.

The goal is simple: define work in markdown, keep tasks reviewable, and let scripts convert curated task files into GitHub issues with consistent labels, milestones, and acceptance criteria.

## What this template gives you

- `AGENTS.md` with operating instructions for AI coding agents.
- `docs/` with workflow, task authoring, and repository conventions.
- `.github/ISSUE_TEMPLATE/` for manually created GitHub issues.
- `tasks/` folders for backlog, ready, and done task files.
- `scripts/create_issues.py` to create GitHub issues from markdown task files, ensuring labels exist first.
- Example tasks, default `.github/labels.yml`, and configuration to copy into your own project.

## Quick start

1. Create a new repository from this template.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Export a GitHub token with issue creation permissions:

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

4. Preview issue creation:

```bash
python scripts/create_issues.py --repo owner/repo --tasks tasks/ready --dry-run
```

5. Create the issues. The script creates any missing labels before creating issues:

```bash
python scripts/create_issues.py --repo owner/repo --tasks tasks/ready
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

## Recommended workflow

1. Capture rough ideas in `tasks/backlog/`.
2. Refine task files until they are small, testable, and agent-ready.
3. Move refined files into `tasks/ready/`.
4. Run the issue creation script.
5. Work from GitHub issues and keep task files as source-of-truth planning artifacts.

## License

MIT. Replace this license if your project requires something else.
