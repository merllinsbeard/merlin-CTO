# Read-only isolation/deployment review probes

Use these probes for expert/persona/tenant migrations and deployment diffs. They are intentionally non-mutating; put all scratch data under `/tmp` or `TemporaryDirectory`.

## Scope and baseline

```bash
git status --short
git diff --stat
git diff --name-only
git diff --check
```

Read `AGENTS.md`, then any root context map and relevant ADRs. Keep a note of paths already dirty before the review. Review the requested diff and the full current files around each changed hunk.

## Wrapper/selector propagation

Make command-line variables are not automatically exported:

```bash
make -n index EXPERT_ID=oleg DATA_DIR=data-oleg EXPERTS_ROOT=experts
gmake -n run EXPERT_ID=oleg  # use make if gmake is unavailable
make -n docker-index EXPERT_ID=oleg DATA_DIR=data-oleg
```

Look for targets that interpolate the variables, targets that merely invoke Python/Docker, and whether a Python `load_dotenv()` fallback is defeated by an explicit Make default. Test the no-`.env`, `.env`, shell-export, and Make-command-line cases separately.

## Compose effective configuration

Never infer precedence from YAML order. Render the effective model without starting containers:

```bash
EXPERT_ID=oleg HOST_DATA_DIR=./data-oleg POSTGRES_PASSWORD=test \
  docker compose --profile tools config --format json
```

For custom database checks, also set a deliberately distinctive `DATABASE_URL` such as `postgresql://u:p@external-db:5432/oleg_db` and inspect every service's rendered `environment.DATABASE_URL`. Inspect volume sources and targets, state paths, selectors, and command arguments. Explicit `environment:` keys override values supplied by `env_file`.

## Two-namespace local-index probe

Use a temporary root containing one source packet per namespace and the same `data_dir`:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
from arslan_bot.ingestion.index import build_index
from arslan_bot.storage.db import LocalIndex

with TemporaryDirectory() as td:
    root = Path(td)
    # Create experts/a/sources and experts/b/sources with distinct marker text.
    data = root / "shared-data"
    experts = root / "experts"
    build_index(expert_id="a", data_dir=data, experts_root=experts,
                write=True, embed=False)
    before = [d.expert_id for d in LocalIndex(data).list_documents()]
    build_index(expert_id="b", data_dir=data, experts_root=experts,
                write=True, embed=False)
    after = [d.expert_id for d in LocalIndex(data).list_documents()]
    print(before, after)
```

If `after` contains only `b`, the storage is whole-file replacement and a shared default `DATA_DIR` is unsafe. Repeat with separate `data-a`/`data-b` directories to verify the documented safe path.

## SQL isolation and identity probe

When a live Postgres instance is unnecessary, inject a fake connection/cursor and record SQL plus parameters. Verify:

- empty replace deletes only the selected namespace;
- non-empty replace removes stale documents and chunks for that namespace;
- another namespace remains untouched;
- mixed document/chunk payloads are rejected;
- fresh inserts use the configured human display name, not only the technical ID;
- existing rows do not silently preserve a wrong first label unless that compatibility is intentional.

For a real DB, use a disposable database and a transaction/rollback boundary. Do not use production credentials or mutate the repository.

## Evidence standard

Each reported issue should include:

1. `path:line` in the reviewed version;
2. the exact configuration/command that triggers it;
3. observed output or state from a real probe;
4. the consequence (wrong namespace, data loss, credential exposure, broken compatibility, or only documentation drift);
5. whether it is introduced by the diff or pre-existing.

Run targeted tests with `PYTHONDONTWRITEBYTECODE=1` to avoid repository bytecode churn. Finish with `git diff --check` and `git status --short`; report any pre-existing dirty files separately.
