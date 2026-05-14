# PromptForge: Git for Your LLM Prompts

*Version control, regression tests, and diffs for production AI systems*

---

## The Problem

Every AI application has the same unspoken dread: "We changed the prompt last week and now the quality dropped. But we don't know what we changed, or why, or how to get back."

Prompts are code. They get edited, tuned, and "improved" constantly. But unlike code, they have no version history, no tests, and no diffs. You ship a `.txt` file and hope for the best.

This breaks in production. A developer updates the customer support prompt to reduce hallucinations, and three weeks later someone notices the escalation rate doubled. Nobody can trace exactly what changed because the prompt lives in Notion, or Slack, or someone's Google Doc.

**PromptForge brings engineering rigor to prompt management.**

## What It Does

PromptForge is a CLI tool that treats prompts like source code:

```bash
# Initialize a project
promptforge init my-prompts

# Add a prompt version
promptforge add --name "customer-support" --file prompts/v1.txt

# Edit and commit
promptforge edit customer-support --file prompts/v2.txt
promptforge commit -m "Add empathy, reduce hallucination risk"

# See what changed
promptforge diff customer-support v1 v2

# Run regression tests
promptforge test add --prompt customer-support \
    --input "My order is late" \
    --expected "order_id"
promptforge test run customer-support
```

Every edit is a commit. Every version is stored. You can branch, diff, cherry-pick, and merge — just like Git.

## Why Version Control for Prompts?

Because prompts have semantics, not just syntax. A single word change can alter model behavior dramatically:

```
- "You are a helpful assistant"
+ "You are a helpful assistant that cites sources"
```

This isn't a typo fix — it's a behavioral change. Without version control, you can't reason about what caused a regression.

## Architecture

```
.promptforge/
├── prompts/         # Versioned prompt files
├── branches/        # Named experiments
├── tests/           # Regression test cases
└── metrics/         # Token/latency tracking
```

Prompts are stored as plain text files with JSON metadata. No lock-in, no database.

## Use Cases

- **Production AI apps** — Track which prompt version is deployed, roll back on regression
- **Prompt libraries** — Maintain collections of reusable prompts with versioning
- **A/B testing** — Compare prompt variants systematically with metrics
- **Compliance** — Full audit trail for prompt changes in regulated industries

## Get Started

```bash
pip install promptforge
promptforge init my-project
```

Full docs at: https://github.com/AmSach/PromptForge

---

*PromptForge is MIT licensed. Contributions welcome.*
