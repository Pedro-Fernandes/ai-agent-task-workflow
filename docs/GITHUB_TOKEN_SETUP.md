# GitHub Token Setup

The issue creation script needs a GitHub token with permission to create issues in the target repository.

## Fine-grained token recommendation

Create a fine-grained personal access token with access to the target repository and these permissions:

- Issues: Read and write.
- Metadata: Read-only.

Then export it:

```bash
export GITHUB_TOKEN="github_pat_your_token_here"
```

On Windows PowerShell:

```powershell
$env:GITHUB_TOKEN="github_pat_your_token_here"
```

Do not commit tokens to the repository.
