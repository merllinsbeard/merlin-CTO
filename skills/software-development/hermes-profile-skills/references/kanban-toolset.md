# Kanban toolset without dispatcher

Скиллы `kanban-board-operations`, `kanban-sequential-campaign`, `sdlc-review` требуют `metadata.hermes.requires_toolsets: [kanban]`.

## Что включать

В `<profile>/config.yaml` top-level:

```yaml
toolsets:
  - kanban
```

`platform_toolsets.<surface>` с `kanban` недостаточно: обычная сессия часто остаётся без `kanban_*`, пока нет top-level `toolsets`.

Правка только через terminal (не `patch`/`write_file`). Бэкап `config.yaml` перед записью. Список не гнать через `hermes config set`.

Проверка: `HERMES_HOME=<profile> hermes config get toolsets` содержит `- kanban`.

Инструменты `kanban_*` в **уже открытой** сессии появятся после рестарта. Не чинить повторным attach скиллов.

## Что не включать

Не добавлять блок `kanban.dispatch_in_gateway` / `orchestrator_profile` / `default_assignee`, если профиль не должен стать автодиспетчером. Identity CTO: Automatic Kanban не его.

Скиллы борда ≠ демон оркестрации.
