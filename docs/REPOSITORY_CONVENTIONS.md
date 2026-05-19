# Repository Conventions

## Labels

Suggested labels:

- `agent-ready`: task has enough detail for an AI agent.
- `needs-refinement`: task needs more context before implementation.
- `docs`: documentation changes.
- `script`: automation or tooling changes.
- `bug`: defect or regression.
- `enhancement`: new or improved behavior.
- `good-first-agent-task`: small, isolated task suitable for testing the workflow.

## Task folders

Use only these task lifecycle folders:

- `tasks/pending/`: markdown tasks that have not been exported to GitHub issues.
- `tasks/exported/`: markdown tasks that were successfully exported to GitHub issues.

Do not add local workflow folders for in-progress or done work. GitHub issues and pull requests track execution state after export.

## Milestones

Suggested milestones:

- `MVP`
- `Automation`
- `Documentation`
- `Hardening`

## Commit style

Use concise, descriptive commit messages:

```text
Add dry-run mode to issue creation script
Document agent-ready task format
Fix markdown front matter validation
```

## PR checklist

- [ ] The change is scoped to the issue.
- [ ] Acceptance criteria are satisfied.
- [ ] Relevant tests or manual validation were run.
- [ ] Documentation was updated if behavior changed.
