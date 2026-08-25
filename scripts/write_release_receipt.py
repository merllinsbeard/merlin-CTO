#!/usr/bin/env python3
"""Write or check an immutable release receipt for this checkout."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

REQUIRED_RECEIPT_KEYS = (
    "name",
    "version",
    "git_commit",
    "git_tree",
    "skill_count",
    "file_count",
    "hermes_requires",
    "checks",
    "hashes",
)


def fail(message: str) -> None:
    raise SystemExit(f"release receipt: FAIL: {message}")


def git(root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=root, text=True).strip()
    except subprocess.CalledProcessError as exc:
        fail(f"git {' '.join(args)} failed: {exc.returncode}")
        raise


def run_check(root: Path, script: str, label: str) -> str:
    try:
        output = subprocess.check_output(
            [sys.executable, str(root / script), str(root)],
            cwd=root,
            text=True,
        ).strip()
    except subprocess.CalledProcessError as exc:
        detail = (exc.stdout or exc.stderr or "").strip() or f"exit {exc.returncode}"
        fail(f"{label}: {detail}")
        raise
    if "PASS" not in output:
        fail(f"{label} did not report PASS: {output}")
    return output


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def count_files(root: Path) -> int:
    names = git(root, "ls-files", "-z", "-c", "-o", "--exclude-standard").split("\0")
    count = sum(1 for name in names if name)
    if count == 0:
        fail("empty tree")
    return count


def build_receipt(root: Path) -> dict:
    manifest = yaml.safe_load((root / "distribution.yaml").read_text())
    skill_count = sum(1 for _ in (root / "skills").rglob("SKILL.md"))
    if skill_count == 0:
        fail("no materialized skills")
    checks = {
        "verify_distribution": run_check(root, "scripts/verify_distribution.py", "verify_distribution"),
        "verify_public_tree": run_check(root, "scripts/verify_public_tree.py", "verify_public_tree"),
    }
    return {
        "name": manifest["name"],
        "version": manifest["version"],
        "git_commit": git(root, "rev-parse", "HEAD"),
        "git_tree": git(root, "rev-parse", "HEAD^{tree}"),
        "skill_count": skill_count,
        "file_count": count_files(root),
        "hermes_requires": manifest.get("hermes_requires"),
        "issued_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checks": checks,
        "hashes": {
            "distribution.yaml": sha256_file(root / "distribution.yaml"),
            "SOUL.md": sha256_file(root / "SOUL.md"),
            "config.yaml": sha256_file(root / "config.yaml"),
        },
        "install_tracks": "default branch. Hermes profile install does not pin tags yet.",
    }


def load_receipt(path: Path) -> dict:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"receipt is not JSON: {exc}")
        raise
    if not isinstance(data, dict):
        fail("receipt must be a JSON object")
    missing = [key for key in REQUIRED_RECEIPT_KEYS if key not in data]
    if missing:
        fail(f"receipt missing keys: {', '.join(missing)}")
    return data


def check_receipt(root: Path, path: Path) -> None:
    expected = load_receipt(path)
    actual = build_receipt(root)
    compared = ("name", "version", "git_commit", "git_tree", "skill_count", "hermes_requires")
    mismatches = [
        f"{key}: receipt {expected.get(key)!r} != checkout {actual.get(key)!r}"
        for key in compared
        if expected.get(key) != actual.get(key)
    ]
    if expected.get("hashes") != actual.get("hashes"):
        mismatches.append("hashes for distribution.yaml, SOUL.md, or config.yaml differ")
    if mismatches:
        fail("; ".join(mismatches))
    print(f"release receipt: PASS ({path})")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", metavar="PATH", help="write receipt JSON to PATH")
    parser.add_argument("--check", metavar="PATH", help="compare PATH to this checkout")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.check:
        check_receipt(root, Path(args.check))
        return 0
    receipt = build_receipt(root)
    text = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.write:
        path = Path(args.write)
        path.write_text(text)
        print(f"release receipt: WROTE {path}")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
