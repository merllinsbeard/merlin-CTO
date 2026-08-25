#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROFILE="merlin-cto-smoke-$$"

cleanup() {
  hermes profile delete "$PROFILE" --yes >/dev/null 2>&1 || true
}
trap cleanup EXIT

hermes profile install "$ROOT" --name "$PROFILE" --yes
hermes profile show "$PROFILE" >/dev/null

python - "$PROFILE" <<'PY'
from pathlib import Path
import sys

import yaml
from hermes_cli.profiles import get_profile_dir

root = Path(get_profile_dir(sys.argv[1]))
assert (root / "SOUL.md").is_file()
assert (root / "config.yaml").is_file()
manifest = yaml.safe_load((root / "distribution.yaml").read_text())
assert manifest["version"] == "1.0.0"
assert manifest["name"].startswith("merlin-cto-smoke-")
assert sum(1 for _ in (root / "skills").rglob("SKILL.md")) == 90
assert not any(path.is_symlink() for path in root.rglob("*"))
for maintainer_only in ("GATES.md", "README.md", "scripts", "tools", "third_party"):
    assert not (root / maintainer_only).exists(), maintainer_only
PY

printf 'isolated install smoke: PASS (%s)\n' "$PROFILE"
