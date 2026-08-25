#!/usr/bin/env python3
"""Materialize the public CTO skill set from a Hermes profile."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
import re

IGNORED_NAMES = (".git", "__pycache__", "*.pyc", ".DS_Store", "*.bak", "*.bak-*")
TEXT_SUFFIXES = {".md", ".py", ".sh", ".json", ".yaml", ".yml", ".toml", ".txt"}

SKILLS = [
    "blast-radius",
    "concise",
    "how",
    "ponytail",
    "principle-boundary-discipline",
    "principle-encode-lessons-in-structure",
    "principle-fix-root-causes",
    "principle-guard-the-context-window",
    "principle-laziness-protocol",
    "principle-model-the-domain",
    "principle-never-block-on-the-human",
    "principle-prove-it-works",
    "principle-separate-before-serializing-shared-state",
    "principle-sequence-verifiable-units",
    "principle-type-system-discipline",
    "tdd-bug-fix",
    "typescript-best-practices",
    "unlazy",
    "unslop",
    "wait-what-bro",
    "why",
    "writing-for-agents",
    "claude-code",
    "cli-agent-first",
    "codex",
    "computer-use",

    "hermes-agent",
    "merge-reconciler",
    "opencode",
    "oracle",
    "how-to-talk",
    "docker-management",
    "production-release-verification",

    "sdlc-review",

    "codebase-inspection",
    "github-auth",
    "github-code-review",
    "github-issue-to-pr",
    "github-issues",
    "github-pr-workflow",
    "github-repo-management",
    "remote-machine-access",
    "ask-matt",
    "code-review",
    "codebase-design",
    "diagnosing-bugs",
    "domain-modeling",
    "grill-me",
    "grill-with-docs",
    "handoff",
    "implement",
    "implement-spec",
    "improve-codebase-architecture",
    "prototype",
    "research",
    "resolving-merge-conflicts",
    "tdd",
    "to-questionnaire",
    "to-spec",
    "to-tickets",
    "triage",
    "wayfinder",
    "wizard",
    "ast-grep",
    "code-wiki",
    "concurrent-coding-agent-coordination",
    "cto-subagent-development",
    "dogfood",
    "frontend-premium-audit",
    "node-inspect-debugger",
    "plan",
    "python-debugpy",
    "requesting-code-review",
    "rest-graphql-debug",
    "simplify-code",
    "spike",
    "systematic-debugging",
    "ticket-campaign-execution",
    "product-surface-review",
    "cloudflare-temporary-deploy",
    "durable-static-site-forms",
    "har-derived-api-client",

    "page-agent",
    "claude-design",
    "design-md",
    "design-taste-frontend",
    "excalidraw",
    "popular-web-designs",
    "baoyu-infographic",
    "image",
    "image-to-code",
    "redesign-existing-projects",
    "software-architecture-visualization",
    "visualize",
    "test-driven-development",
    "subagent-driven-development",
]

RELATED_ALIASES = {
    "sketch": "prototype",
}


def discover(root: Path) -> dict[str, Path]:
    found: dict[str, Path] = {}
    candidates = list(root.glob("*/SKILL.md")) + list(root.glob("*/*/SKILL.md"))
    for skill_file in candidates:
        directory = skill_file.parent
        name = directory.name
        if name in found and found[name].resolve() != directory.resolve():
            raise RuntimeError(f"duplicate skill directory name: {name}")
        found[name] = directory
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-profile", type=Path, required=True)
    parser.add_argument("--destination", type=Path, default=Path("skills"))
    args = parser.parse_args()

    source_root = args.source_profile.expanduser().resolve() / "skills"
    destination = args.destination.resolve()
    discovered = discover(source_root)
    missing = sorted(set(SKILLS) - set(discovered))
    if missing:
        raise SystemExit(f"missing skills: {', '.join(missing)}")

    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)

    for name in SKILLS:
        source = discovered[name]
        relative_parent = source.relative_to(source_root).parent
        target = destination / relative_parent / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(
            source.resolve(),
            target,
            symlinks=False,
            ignore=shutil.ignore_patterns(*IGNORED_NAMES),
        )

    replacements = {
        "A writer named by Timofei: that writer.":
            "A writer explicitly named by the current user: that writer.",
    }
    for skill_file in destination.rglob("SKILL.md"):
        text = skill_file.read_text()
        updated = text
        for old, new in replacements.items():
            updated = updated.replace(old, new)
        if updated != text:
            skill_file.write_text(updated)

    for path in destination.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(errors="strict")
        lines = [line.rstrip() for line in text.splitlines()]
        while lines and not lines[-1]:
            lines.pop()
        normalized = "\n".join(lines) + "\n"
        if normalized != text:
            path.write_text(normalized)

    overrides = Path(__file__).resolve().parent.parent / "overrides" / "skills"
    if overrides.is_dir():
        for source in overrides.rglob("SKILL.md"):
            relative = source.relative_to(overrides)
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    available = {path.parent.name for path in destination.rglob("SKILL.md")}

    def rewrite_related(text: str) -> str:
        match = re.search(r"related_skills:\s*\[([^\]]*)\]", text)
        if not match:
            return text
        names = [item.strip().strip("'\"") for item in match.group(1).split(",") if item.strip()]
        rewritten = [RELATED_ALIASES.get(name, name) for name in names]
        replacement = "related_skills: [" + ", ".join(rewritten) + "]"
        return text[: match.start()] + replacement + text[match.end() :]

    for skill_file in destination.rglob("SKILL.md"):
        text = skill_file.read_text()
        updated = rewrite_related(text)
        if updated != text:
            skill_file.write_text(updated)

    links = [path for path in destination.rglob("*") if path.is_symlink()]
    if links:
        raise SystemExit(f"materialization left {len(links)} symlink(s)")

    missing_related = []
    for skill_file in destination.rglob("SKILL.md"):
        match = re.search(r"related_skills:\s*\[([^\]]*)\]", skill_file.read_text())
        if not match:
            continue
        names = [item.strip().strip("'\"") for item in match.group(1).split(",") if item.strip()]
        absent = [name for name in names if name not in available]
        if absent:
            missing_related.append(f"{skill_file.parent.name}: {', '.join(absent)}")
    if missing_related:
        raise SystemExit("unresolved related_skills:\n  " + "\n  ".join(missing_related))

    print(f"materialized {len(SKILLS)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
