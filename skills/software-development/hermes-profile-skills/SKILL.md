---
name: hermes-profile-skills
description: Use when attaching or enabling skills on a Hermes profile.
---

# Hermes profile skills

Подключить скиллы в **изолированный** профиль Hermes: official bundle, другой профиль, сторонний pack. Не копировать канон. Не сеять весь bundled opt-in.

Перекрывается с `skill-library-management` (npx/`skills.sh` + гейт `skills.disabled` в default/Neuromancer). Этот скилл — attach в profile-local root через симлинк. Если оба видны, сначала этот для профиля, тот — для hub/npx install.

## Когда применять

- «Подключи скиллы», «поставь official/engineering/kanban/Pocock/oracle в этот профиль».
- Инвентарь: что native, что у другого профиля, что уже local.
- Канон (AGENTS, identity) ссылается на имя, которого нет в `skills_list` этого профиля.

Не применять: правка тела чужого SKILL.md; commit/push; включение Kanban dispatcher / `orchestrator_profile`; `hermes skills opt-in` «чтобы всё появилось».

## Источники (живые, не память)

1. Bundled official: `$HERMES_RELEASE/skills/{software-development,github,devops,autonomous-ai-agents}`.
2. Optional official: `$HERMES_RELEASE/optional-skills/` — те же инженерные категории + `web-development`. Не mlops, creative, finance, gaming, pentest.
3. Уже разложенный канон: `~/.hermes/skills/<cat>/<name>` — брать его, если есть `SKILL.md`.
4. Другой профиль: `~/.hermes/profiles/<name>/skills/...` — только чтение. Симлинк **в этот** профиль.
5. Matt Pocock: upstream `https://github.com/mattpocock/skills` → `skills/engineering/`. Не плоский устаревший pack в merlin-agent-skills. Состав: `references/matt-pocock-engineering.md`.

Имена official engineering: `references/official-engineering-set.md`.

Релиз на этой машине: `hermes --version` + `optional-skills` рядом с install directory. Не хардкодить tag.

## Как подключать

1. Снять `HERMES_HOME=<profile> hermes skills list --enabled-only` и дерево `<profile>/skills`. Isolated profile **не** наследует `~/.hermes/skills`.
2. Заморозить keep-set: profile-local близнецы official не затирать (`codex`, `grok`, `tdd` в CTO — свои).
3. Для каждого имени выбрать один src: shared `~/.hermes/skills` → release bundled → optional-skills → чужой профиль → vendor clone.
4. `ln -sfn <src-dir> <profile>/skills/<category>/<name>`. Категорию сохранить. Весь каталог (references/scripts), не один SKILL.md.
5. Сторонний git-pack клонировать **вне** `skills/` (`<profile>/vendor/<pack>`), затем симлинк только нужных leaf. Клон внутрь `skills/` подхватит deprecated/in-progress.
6. Коллизия имени (`tdd` Pocock vs local `tdd`) — пропустить, не переименовывать: frontmatter `name:` всё равно столкнётся в индексе.
7. Kanban-скиллы с `requires_toolsets: [kanban]` — включить toolset. Рецепт: `references/kanban-toolset.md`. Dispatcher не включать.
8. Не вызывать `hermes skills opt-in` ради дыр: посеет creative/finance и остальное.

`npx skills add` / `hermes skills install` кладёт копию и часто пишет имя в `skills.disabled`. Для канона, который уже на диске, симлинк дешевле и не триггерит disable.

## Config

- Списки в `config.yaml` (`skills.disabled`, `toolsets`) — только прямое редактирование файла через terminal. `hermes config set` на список пишет пустую строку.
- `patch` / `write_file` в `config.yaml` отказаны guard-ом.
- Перед правкой: `cp -a config.yaml config.yaml.bak-<stamp>`.
- Нет ключа `skills.disabled` = ничего не выключено. Не создавать пустой блок «на всякий».

## Проверка

- `HERMES_HOME=<profile> hermes skills list --enabled-only` — ожидаемые имена, status `enabled`, без лишних категорий.
- `skill_view(name)` по образцам из каждого источника (`hermes-agent`, `oracle`, `kanban-board-operations`, `ask-matt`) → `readiness_status: available`.
- Симлинк резолвится в выбранный канон (`readlink -f`).
- `hermes config get toolsets` содержит `kanban`, если подключали kanban-скиллы.
- Индекс **текущей** сессии может остаться старым. `skill_view` и CLI читают диск; полный автоподхват — новая сессия. Не чинить это повторным attach.

## Ловушки

- Official `codex`/`grok` поверх локальных кастомных копий.
- `repair-official --restore all` — вывалит optional целиком, включая не-инженерное.
- Писать в чужой профиль «чтобы поделиться каноном». Нужен только inbound symlink.
- Считать Neuromancer-врачей (cron/storage/bot-mode, landing Лабы) инженерной поставкой. С профиля CTO брать oracle, kanban-board, SDLC extras — не ops-флот.
- Путать `platform_toolsets.telegram: [kanban]` с рабочим toolset: без top-level `toolsets: [kanban]` сессия часто без `kanban_*`.
- Ставить Pocock `tdd` рядом с локальным `tdd`.

## Related

- `references/official-engineering-set.md` — bundled + optional, что не брать.
- `references/matt-pocock-engineering.md` — upstream engineering/, vendor, коллизии.
- `references/kanban-toolset.md` — toolset без dispatcher.
