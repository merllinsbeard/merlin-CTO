#!/usr/bin/env python3
"""Validate the repository as an installable Hermes profile distribution."""

from __future__ import annotations

import sys
from pathlib import Path
import re

import yaml

REQUIRED_OWNED = {"distribution.yaml", "SOUL.md", "config.yaml", "skills"}
PRIVATE_MARKERS = (
    "/home/merlin",
    ".openviking",
    "openviking",
    "timofei",
    "тимофей",
    "oleg-ai-bot",
    "klimin-onboarding",
    "jitsi_bot",
    "land_marketing",
)


def fail(message: str) -> None:
    raise SystemExit(f"distribution verification: FAIL: {message}")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    manifest = yaml.safe_load((root / "distribution.yaml").read_text())
    if manifest.get("name") != "merlin-cto":
        fail("manifest name must be merlin-cto")
    owned = set(manifest.get("distribution_owned") or [])
    if not REQUIRED_OWNED <= owned:
        fail(f"missing distribution-owned paths: {sorted(REQUIRED_OWNED - owned)}")

    config_text = (root / "config.yaml").read_text()
    config = yaml.safe_load(config_text)
    if config.get("memory", {}).get("provider") != "local":
        fail("default memory provider must be local")
    if config.get("terminal", {}).get("cwd") != ".":
        fail("terminal.cwd must be portable")

    skills_root = root / "skills"
    skill_files = sorted(skills_root.rglob("SKILL.md"))
    if not skill_files:
        fail("no materialized skills found")
    names = {path.parent.name for path in skill_files}
    for skill_file in skill_files:
        text = skill_file.read_text(errors="replace")
        match = re.search(r"related_skills:\s*\[([^\]]*)\]", text)
        if not match:
            continue
        related = [item.strip().strip("'\"") for item in match.group(1).split(",") if item.strip()]
        missing = [name for name in related if name not in names]
        if missing:
            fail(f"{skill_file.parent.name} related_skills missing: {', '.join(missing)}")
    links = [path for path in root.rglob("*") if path.is_symlink()]
    if links:
        fail(f"symlinks are forbidden: {links[0].relative_to(root)}")

    public_contract = "\n".join(
        (root / name).read_text(errors="replace")
        for name in ("SOUL.md", "config.yaml", "distribution.yaml")
    ).lower()
    for marker in PRIVATE_MARKERS:
        if marker.lower() in public_contract:
            fail(f"private marker in installed contract: {marker}")

    print(f"distribution verification: PASS ({len(skill_files)} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
