# Task Authoring Guide

Good AI-agent tasks are specific, bounded, and verifiable. They are planning artifacts used to create GitHub issues, not local execution state.

## Recommended structure

```markdown
---
title: "Short imperative title"
labels: ["agent-ready"]
milestone: "MVP"
assignees: []
---

## Context
Explain why this task exists.

## Goal
Describe the desired outcome.

## Scope
Include what should be changed.

## Non-Goals
List what should not be changed.

## Acceptance Criteria
- [ ] Criterion one.
- [ ] Criterion two.

## Implementation Notes
Add constraints, examples, or relevant files.

## Validation
Explain how to verify the result.
```

## Sizing rule

A task is probably too large if it requires more than one conceptual change. Split it into smaller tasks when possible.

## Placement

Put unexported task files in `tasks/pending/`. After a successful export, the issue creation script moves them to `tasks/exported/` and adds GitHub issue metadata to the front matter.

Do not add local in-progress or done markers. Track implementation state in GitHub.

## Good acceptance criteria

Good criteria are observable:

- The export script supports `--dry-run` without creating issues.
- Invalid markdown front matter exits with a clear error message.
- The README includes a copy-paste quick start.

Weak criteria are vague:

- Make it better.
- Improve quality.
- Add some tests.
