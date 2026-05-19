# AI-Agent Task Workflow

This workflow is built around a simple idea: humans and AI agents collaborate better when work is written as small, explicit, reviewable tasks.

## Lifecycle

```text
idea -> backlog task -> refined task -> ready task -> GitHub issue -> branch -> PR -> done
```

## 1. Capture ideas

Put rough ideas in `tasks/backlog/`. These can be incomplete, but they should describe the problem or opportunity.

## 2. Refine into agent-ready tasks

Before a task is moved to `tasks/ready/`, make sure it includes:

- Context.
- Goal.
- Scope.
- Non-goals.
- Acceptance criteria.
- Implementation notes.
- Validation plan.

## 3. Create GitHub issues

Run:

```bash
python scripts/create_issues.py --repo owner/repo --tasks tasks/ready --dry-run
python scripts/create_issues.py --repo owner/repo --tasks tasks/ready
```

The script reads markdown task files and creates one issue per task.

## 4. Execute through branches and PRs

Recommended branch naming:

```text
agent/<issue-number>-short-description
```

Each pull request should link its issue using `Closes #123` or `Fixes #123`.

## 5. Keep the workflow clean

After an issue is created, either:

- move the task file to `tasks/done/`, or
- keep it in `tasks/ready/` and add an `issue_url` field to the front matter.

This template does not force one approach. Choose the convention that fits your team.


## Label ordering guarantee

The issue creation script intentionally performs label creation before issue creation. This prevents GitHub API failures caused by task files referencing labels that are not yet present in the repository.

Recommended command:

```bash
python scripts/create_issues.py --repo owner/repo --tasks tasks/ready
```

Use `--dry-run` first to see both the required labels and the issues that would be created.
