---
title: "Add task validation script"
labels: ["script", "agent-ready", "good-first-agent-task"]
milestone: "Automation"
assignees: []
---

## Context

Task files should be validated before maintainers create GitHub issues from them.

## Goal

Provide a simple validation command that checks whether task markdown files follow the expected format.

## Scope

- Validate YAML front matter.
- Require a non-empty `title` field.
- Validate optional `labels` and `assignees` fields as lists of strings.
- Print one success line per valid file.

## Non-Goals

- Do not create GitHub issues.
- Do not modify task files automatically.

## Acceptance Criteria

- [ ] Running `python scripts/validate_tasks.py tasks/ready` validates all ready tasks.
- [ ] Invalid task files fail with a useful error message.
- [ ] The command exits with a non-zero status when validation fails.

## Implementation Notes

Reuse parsing logic from `scripts/create_issues.py` where possible.

## Validation

Run:

```bash
python scripts/validate_tasks.py tasks/ready
```
