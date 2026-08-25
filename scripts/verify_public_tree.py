#!/usr/bin/env python3
"""Fail closed when a public distribution contains local or private state."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

FORBIDDEN_PARTS = {
    ".env",
    "auth.json",
    "memories",
    "sessions",
    "logs",
    "home",
    "cache",
    "backups",
    "workspace",
    "node_modules",
    "__pycache__",
}
FORBIDDEN_SUFFIXES = {".db", ".db-shm", ".db-wal", ".sock", ".key", ".pem", ".pyc"}
PRIVATE_MARKERS = (
    "/home/merlin",
    "100.70.125.75",
    "oleg-ai-bot",
    "klimin-onboarding",
    "jitsi_bot",
    "land_marketing",
    "[truncated]",
)
TEXT_SUFFIXES = {
    ".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".py", ".js",
    ".ts", ".tsx", ".sh", ".bash", ".mjs", ".css", ".html",
}


def fail(message: str) -> None:
    raise SystemExit(f"public tree verification: FAIL: {message}")


def git_visible_files(root: Path) -> list[Path]:
    try:
        output = subprocess.check_output(
            ["git", "ls-files", "-z", "-c", "-o", "--exclude-standard"],
            cwd=root,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return [
            path
            for path in root.rglob("*")
            if path.is_file() and path.parts[len(root.parts) : len(root.parts) + 1] != (".git",)
        ]
    names = [name.decode() for name in output.split(b"\0") if name]
    return [root / name for name in names]


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    files = []
    for path in git_visible_files(root):
        relative = path.relative_to(root)
        if path.is_symlink():
            fail(f"symlink found: {relative}")
        if ".bak" in path.name.lower():
            fail(f"backup file found: {relative}")
        lowered_parts = {part.lower() for part in relative.parts}
        if lowered_parts & FORBIDDEN_PARTS:
            fail(f"forbidden path: {relative}")
        if not path.is_file():
            continue
        files.append(path)
        if any(path.name.lower().endswith(suffix) for suffix in FORBIDDEN_SUFFIXES):
            fail(f"forbidden file type: {relative}")
        if path.stat().st_size > 10 * 1024 * 1024:
            fail(f"file larger than 10 MiB: {relative}")
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"LICENSE", ".gitignore"}:
            if relative.parts[:1] == ("scripts",) and relative.name.startswith("verify_"):
                continue
            text = path.read_text(errors="replace").lower()
            for marker in PRIVATE_MARKERS:
                if marker.lower() in text:
                    fail(f"private marker {marker!r} in {relative}")

    if not files:
        fail("empty tree")
    print(f"public tree verification: PASS ({len(files)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
