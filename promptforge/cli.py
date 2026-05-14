#!/usr/bin/env python3
"""
PromptForge CLI — Git-like interface for LLM prompt management.
"""

import argparse
import os
import sys
from pathlib import Path
from promptforge.core import PromptStore, ForgeConfig


def find_project_root() -> Path:
    cwd = Path.cwd()
    for d in [cwd, *cwd.parents]:
        if (d / ".promptforge").exists():
            return d
    return cwd


def cmd_init(args):
    root = Path.cwd()
    forge_dir = root / ".promptforge"
    if forge_dir.exists():
        print(f"Already initialized: {forge_dir}")
        return
    forge_dir.mkdir(parents=True, exist_ok=True)
    (forge_dir / "prompts").mkdir()
    (forge_dir / "meta").mkdir()
    (forge_dir / "tests").mkdir()
    (forge_dir / "metrics").mkdir()
    print(f"Initialized PromptForge at {root}")


def cmd_add(args):
    root = find_project_root()
    store = PromptStore(str(root))
    
    prompt_text = ""
    if args.file:
        prompt_text = Path(args.file).read_text()
    elif args.text:
        prompt_text = args.text
    else:
        print("Error: --file or --text required")
        return
    
    pv = store.add(args.name, prompt_text, args.message or "Initial commit", args.author or os.getenv("USER", "user"))
    print(f"Added '{args.name}' as {pv.version_id}")


def cmd_log(args):
    root = find_project_root()
    store = PromptStore(str(root))
    versions = store.log(args.name)
    
    for v in versions:
        print(f"\n{'-'*50}")
        print(f"  {v.version_id} | {v.created_at[:10]} | {v.author}")
        print(f"  Message: {v.commit_message}")
        print(f"  Preview: {v.prompt_text[:100]}...")


def cmd_diff(args):
    root = find_project_root()
    store = PromptStore(str(root))
    result = store.diff(args.name, args.v1, args.v2)
    print(result)


def cmd_edit(args):
    root = find_project_root()
    store = PromptStore(str(root))
    
    prompt_text = ""
    if args.file:
        prompt_text = Path(args.file).read_text()
    elif args.text:
        prompt_text = args.text
    else:
        print("Error: --file or --text required")
        return
    
    pv = store.add(args.name, prompt_text, args.message or "Updated prompt", args.author or os.getenv("USER", "user"))
    print(f"Updated '{args.name}' to {pv.version_id}")


def cmd_get(args):
    root = find_project_root()
    store = PromptStore(str(root))
    pv = store.get(args.name, args.version)
    if pv:
        print(pv.prompt_text)
    else:
        print(f"Version {args.version} not found for '{args.name}'")


def main():
    parser = argparse.ArgumentParser(prog="promptforge", description="Version control for LLM prompts")
    sub = parser.add_subparsers()

    p_init = sub.add_parser("init", help="Initialize a promptforge project")
    p_init.set_defaults(fn=cmd_init)

    p_add = sub.add_parser("add", help="Add a new prompt")
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--file", help="File containing prompt text")
    p_add.add_argument("--text", help="Prompt text directly")
    p_add.add_argument("--message", help="Commit message")
    p_add.add_argument("--author", help="Author name")
    p_add.set_defaults(fn=cmd_add)

    p_log = sub.add_parser("log", help="Show prompt version history")
    p_log.add_argument("name", help="Prompt name")
    p_log.set_defaults(fn=cmd_log)

    p_diff = sub.add_parser("diff", help="Show diff between versions")
    p_diff.add_argument("name", help="Prompt name")
    p_diff.add_argument("v1", help="First version ID")
    p_diff.add_argument("v2", help="Second version ID")
    p_diff.set_defaults(fn=cmd_diff)

    p_edit = sub.add_parser("edit", help="Update a prompt (creates new version)")
    p_edit.add_argument("--name", required=True)
    p_edit.add_argument("--file", help="File containing prompt text")
    p_edit.add_argument("--text", help="Prompt text directly")
    p_edit.add_argument("--message", help="Commit message")
    p_edit.add_argument("--author", help="Author name")
    p_edit.set_defaults(fn=cmd_edit)

    p_get = sub.add_parser("get", help="Get a specific version of a prompt")
    p_get.add_argument("--name", required=True)
    p_get.add_argument("--version", required=True)
    p_get.set_defaults(fn=cmd_get)

    args = parser.parse_args()
    if hasattr(args, "fn"):
        args.fn(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
