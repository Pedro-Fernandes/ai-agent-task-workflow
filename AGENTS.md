# AGENTS.md

This repository is designed to be used by human maintainers and AI coding agents.

## Mission

Help teams convert product ideas into small, reviewable, implementation-ready tasks, then execute those tasks safely through GitHub issues and pull requests.

## Operating principles

1. Prefer small changes over large rewrites.
2. Treat markdown task files as planning artifacts, not as a substitute for code review.
3. Do not implement unclear tasks. First refine the task with context, scope, and acceptance criteria.
4. Keep generated code simple, testable, and consistent with the repository conventions.
5. Never invent hidden requirements. State assumptions explicitly in the PR description.
6. When modifying scripts, include dry-run behavior and helpful error messages.
7. Avoid destructive operations unless the task explicitly asks for them.

## Agent workflow

When assigned a GitHub issue or markdown task:

1. Read the full issue body and all linked task files.
2. Identify the smallest valuable change that satisfies the acceptance criteria.
3. Inspect the repository structure before editing.
4. Plan the change and ask for plan approval
5. Make the change.
6. Add or update tests when practical.
7. Run relevant checks locally.
8. Summarize the change, assumptions, and verification steps in the PR.

## Definition of agent-ready

A task is agent-ready when it has:

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
