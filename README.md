# PromptForge — Version Control for LLM Prompts

**PromptForge** is a CLI toolkit that brings Git-like version control to LLM prompts. Fork prompt versions, diff them, run regression tests, and cherry-pick the best versions — all from the command line.

## Features

- **Prompt versioning** — Every edit is a commit with a diff
- **Semantic diffs** — See exactly what changed between prompt versions (instruction drift, context shifts)
- **Regression testing** — Define test cases (input → expected output patterns) and catch regressions before deployment
- **Cherry-pick** — Copy the best parts of different prompt versions
- **Branch and merge** — Experiment with variations without losing the original
- **Metrics** — Track token usage, latency, and cost per prompt version
- **Local storage** — No external dependency, prompts stored as plain files

## Installation

```bash
pip install promptforge
# or
pip install -e .
```

## Quick Start

```bash
# Initialize a prompt project
promptforge init my-prompts

# Add your first prompt
promptforge add --name "customer-support" --file prompts/v1.txt

# Edit and commit changes
promptforge edit customer-support --file prompts/v2.txt
promptforge commit -m "Add empathy tone, reduce hallucination risk"

# View diff
promptforge diff customer-support v1 v2

# Add test cases
promptforge test add --prompt customer-support --input "My order is late" --expected "order_id"

# Run regression tests
promptforge test run customer-support

# Branch and experiment
promptforge branch customer-support --name "with-citations"
promptforge checkout with-citations
# ... make changes ...
promptforge merge with-citations

# View history
promptforge log customer-support
```

## Architecture

```
.promptforge/
├── prompts/          # Versioned prompt files
│   ├── v1/          # Each version is a directory
│   │   ├── meta.json
│   │   └── prompt.txt
│   └── v2/
├── branches/        # Named branches
├── tests/           # Regression test cases
│   └── customer-support/
│       ├── test_001.json
│       └── test_002.json
├── metrics/         # Per-version usage stats
└── forge.yml        # Project config
```

## Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize a promptforge project |
| `add` | Add a new prompt |
| `edit` | Update a prompt (creates new version) |
| `commit` | Save changes with a message |
| `diff` | Show differences between versions |
| `log` | Show version history |
| `branch` | Create a new branch |
| `checkout` | Switch branches |
| `merge` | Merge branches |
| `test add` | Add a test case |
| `test run` | Run regression tests |
| `metrics` | Show token/latency stats |

## Why PromptForge?

Prompts are code. They deserve the same rigor:
- **Version control** for collaboration and rollback
- **Tests** to catch regressions when you "improve" a prompt
- **Diffing** to understand exactly what changed

Most teams manage prompts in Notion, Google Docs, or Slack threads. PromptForge brings engineering discipline to prompt management.

## Use Cases

- **Production AI apps** — Track which prompt version is deployed
- **Prompt libraries** — Maintain collections of reusable prompts
- **A/B testing** — Compare prompt variants systematically
- **Compliance** — Audit trail for prompt changes

## License

MIT
