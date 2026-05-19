# Labels

GitHub rejects issue creation when a task references a label that does not exist in the repository.

For that reason, `scripts/create_github_issues.py` ensures labels before issues are created:

1. Parse exportable markdown task files from `tasks/pending/`.
2. Collect every label referenced by those tasks.
3. Read existing labels from GitHub.
4. Create missing labels.
5. Create GitHub issues.
6. Move successful exports into `tasks/exported/`.

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

If a task uses a label that is not listed in `.github/labels.yml`, the scripts still create it automatically using a neutral default color.

## Preview labels and issues

```bash
python scripts/create_github_issues.py --dry-run
```

The dry run prints the required labels first, then the issues that would be created.

## Use a custom labels file during export

```bash
python scripts/create_github_issues.py \
  --labels-file .github/labels.yml
```

If the repository does not have a GitHub `origin` remote, pass `--repo owner/repo`.
