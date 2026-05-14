#!/usr/bin/env python3
"""
PromptForge Core — Prompt versioning engine.
"""

import json
import hashlib
import os
import shutil
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any


@dataclass
class PromptVersion:
    version_id: str
    name: str
    prompt_text: str
    commit_message: str
    created_at: str
    author: str
    parent_id: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> 'PromptVersion':
        return cls(**d)


class PromptStore:
    """Stores and manages prompt versions."""

    def __init__(self, project_root: str):
        self.root = Path(project_root)
        self.prompts_dir = self.root / ".promptforge" / "prompts"
        self.prompts_dir.mkdir(parents=True, exist_ok=True)
        self.meta_dir = self.root / ".promptforge" / "meta"
        self.meta_dir.mkdir(parents=True, exist_ok=True)

    def _hash_content(self, content: str) -> str:
        return hashlib.sha256(content.encode()).hexdigest()[:8]

    def add(self, name: str, prompt_text: str, message: str = "Initial commit", author: str = "user") -> PromptVersion:
        """Add a new prompt or new version of existing prompt."""
        existing = self._list_versions(name)
        version_num = len(existing) + 1
        parent_id = existing[-1].version_id if existing else None
        
        version_id = f"v{version_num}_{self._hash_content(prompt_text)}"
        
        # Save prompt file
        version_dir = self.prompts_dir / name / version_id
        version_dir.mkdir(parents=True, exist_ok=True)
        (version_dir / "prompt.txt").write_text(prompt_text)
        
        # Save metadata
        pv = PromptVersion(
            version_id=version_id,
            name=name,
            prompt_text=prompt_text,
            commit_message=message,
            created_at=datetime.utcnow().isoformat(),
            author=author,
            parent_id=parent_id
        )
        (version_dir / "meta.json").write_text(json.dumps(pv.to_dict(), indent=2))
        
        # Update index
        self._update_index(name, pv)
        
        return pv

    def _list_versions(self, name: str) -> List[PromptVersion]:
        """List all versions of a prompt."""
        index_path = self.meta_dir / f"{name}.json"
        if not index_path.exists():
            return []
        data = json.loads(index_path.read_text())
        return [PromptVersion.from_dict(v) for v in data]

    def _update_index(self, name: str, version: PromptVersion):
        """Update the index for a prompt."""
        versions = self._list_versions(name)
        versions.append(version)
        index_path = self.meta_dir / f"{name}.json"
        index_path.write_text(json.dumps([v.to_dict() for v in versions], indent=2))

    def get(self, name: str, version_id: str) -> Optional[PromptVersion]:
        """Get a specific version of a prompt."""
        version_dir = self.prompts_dir / name / version_id
        meta_path = version_dir / "meta.json"
        if not meta_path.exists():
            return None
        return PromptVersion.from_dict(json.loads(meta_path.read_text()))

    def diff(self, name: str, v1_id: str, v2_id: str) -> str:
        """Show diff between two versions."""
        v1 = self.get(name, v1_id)
        v2 = self.get(name, v2_id)
        if not v1 or not v2:
            return f"Version not found"
        
        path1 = self.prompts_dir / name / v1_id / "prompt.txt"
        path2 = self.prompts_dir / name / v2_id / "prompt.txt"
        
        try:
            result = subprocess.run(
                ["diff", "-u", str(path1), str(path2)],
                capture_output=True, text=True
            )
            return result.stdout or result.stderr
        except FileNotFoundError:
            # diff not available, fallback to line-by-line
            lines1 = path1.read_text().splitlines()
            lines2 = path2.read_text().splitlines()
            output = []
            for i, (a, b) in enumerate(zip(lines1, lines2)):
                if a != b:
                    output.append(f"- {a}")
                    output.append(f"+ {b}")
            if len(lines1) != len(lines2):
                output.append(f"--- {len(lines1)} lines vs {len(lines2)} lines")
            return "\n".join(output) if output else "No differences"

    def log(self, name: str) -> List[PromptVersion]:
        return self._list_versions(name)


class ForgeConfig:
    """Project configuration."""

    def __init__(self, project_root: str):
        self.root = Path(project_root)
        self.config_file = self.root / ".promptforge" / "forge.yml"
        self.config: Dict[str, Any] = {}
        if self.config_file.exists():
            self.config = json.loads(self.config_file.read_text())

    def set(self, key: str, value: Any):
        self.config[key] = value
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.config_file.write_text(json.dumps(self.config, indent=2))

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)
