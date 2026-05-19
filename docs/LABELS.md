# Labels

GitHub rejects issue creation when a task references a label that does not exist in the repository.

For that reason, `scripts/create_issues.py` always runs this sequence:

1. Parse all selected markdown task files.
2. Collect every label referenced by those tasks.
3. Read existing labels from GitHub.
4. Create missing labels.
5. Only then create the GitHub issues.

## Label definitions

Default label metadata lives in:

```text
.github/labels.yml
```

Each label can define a name, color, and description:

```yaml
labels:
  - name: agent-ready
    color: 0e8a16
    description: Refined task ready for an AI coding agent.
```

If a task uses a label that is not listed in `.github/labels.yml`, the script still creates it automatically using a neutral default color.

## Preview labels before creating issues

```bash
python scripts/create_issues.py --repo owner/repo --tasks tasks/ready --dry-run
```

The dry run prints the required labels first, then the issues that would be created.

## Use a custom labels file

```bash
python scripts/create_issues.py \
  --repo owner/repo \
  --tasks tasks/ready \
  --labels-file .github/labels.yml
```
