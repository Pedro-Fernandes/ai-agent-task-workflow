# AGENTS.md

This repository is designed to be used by human maintainers and AI coding agents.

## Mission

Help teams convert product ideas into small, reviewable markdown task plans, then export those plans into GitHub issues in the target implementation repository.

## Source of truth

This repository tracks planning and export state only:

- `tasks/pending/` contains markdown tasks that are candidates for GitHub issue export.
- `tasks/exported/` contains markdown tasks that already have GitHub issues.
- The target GitHub repository is the source of truth after export.

Agents must not invent local completion state. Do not create local folders, labels, metadata, or conventions for implementation progress, in-progress work, done work, PR state, or issue closure. Track that work in GitHub.

At the start of a planning conversation, ask what project is being discussed and what GitHub repository should receive exported issues. It is acceptable to draft and refine tasks before that is known, but never export tasks without an explicit target repository from the user.

## Operating principles

1. Prefer small changes over large rewrites.
2. Treat markdown task files as planning artifacts, not as implementation state.
3. Do not implement unclear tasks. First refine the task with context, scope, and acceptance criteria.
4. Keep generated code simple, testable, and consistent with the repository conventions.
5. Never invent hidden requirements. State assumptions explicitly in the PR description.
6. When modifying scripts, include dry-run behavior and helpful error messages.
7. Avoid destructive operations unless the task explicitly asks for them.

## Export workflow

When preparing markdown tasks for GitHub:

1. Put unexported task files in `tasks/pending/`.
2. Confirm the target repository in `owner/repo` format.
3. Run `python scripts/validate_tasks.py`.
4. Run `python scripts/create_github_issues.py --repo owner/repo`.
5. Leave exported files in `tasks/exported/`.
6. Track implementation, PRs, and completion in the target GitHub repository.

## Agent workflow

When assigned a GitHub issue or markdown task:

1. Read the full issue body and any linked task file.
2. Identify the smallest valuable change that satisfies the acceptance criteria.
3. Inspect the repository structure before editing.
4. Plan the change and ask for plan approval when the surrounding workflow requires it.
5. Make the change.
6. Add or update tests when practical.
7. Run relevant checks locally.
8. Summarize the change, assumptions, and verification steps in the PR.

## Definition of export-ready

A task is export-ready when it has:

- A clear goal.
- Enough context to avoid guessing.
- Explicit non-goals or out-of-scope items.
- Testable acceptance criteria.
- Known constraints, dependencies, or affected files.
- A preferred validation method.

## Pull request expectations

Every PR should include:

- What changed.
- Why it changed.
- How it was tested.
- Any assumptions or follow-up tasks.

## Safety rails

Agents should not:

- Change public APIs without explicit acceptance criteria.
- Add new dependencies without justification.
- Remove tests to make a build pass.
- Store secrets, tokens, or credentials in the repository.
- Modify generated lock files without understanding the dependency change.
