---
title: "Add GitHub Actions validation for task files"
labels: ["automation", "needs-refinement"]
milestone: "Hardening"
assignees: []
---

## Context

Task files can drift from the expected format. A CI check would catch invalid task files before they are merged.

## Goal

Run task validation automatically on pull requests.

## Scope

- Add a GitHub Actions workflow.
- Install Python dependencies.
- Run `scripts/validate_tasks.py` against task folders.

## Non-Goals

- Do not create issues from CI.
- Do not require a GitHub token.

## Acceptance Criteria

- [ ] Pull requests run task validation.
- [ ] Invalid task markdown fails the workflow.
- [ ] The workflow is documented in the README.

## Implementation Notes

This needs refinement before implementation because the team should decide which folders are validated.

## Validation

Open a pull request with a valid and invalid task file to confirm behavior.
