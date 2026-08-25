# Matt Pocock engineering pack

Канон: `https://github.com/mattpocock/skills` → `skills/engineering/`.

Не использовать плоский snapshot `merlin-agent-skills/packs/mattpocock-skills` как источник правды — он отстаёт и смешивает engineering с writing/misc.

## Install shape

```bash
VENDOR="$HERMES_HOME/vendor/mattpocock-skills"
git clone --depth 1 https://github.com/mattpocock/skills.git "$VENDOR"
# или: git -C "$VENDOR" fetch --depth 1 origin && git -C "$VENDOR" reset --hard origin/main
```

Клон **вне** `<profile>/skills/`. Потом:

`ln -sfn "$VENDOR/skills/engineering/<name>" "$HERMES_HOME/skills/mattpocock/<name>"`

Категория `mattpocock` — чтобы не смешивать с official `software-development`.

## Engineering leaf (upstream, 18)

ask-matt, code-review, codebase-design, diagnosing-bugs, domain-modeling, grill-with-docs, implement, improve-codebase-architecture, prototype, research, resolving-merge-conflicts, setup-matt-pocock-skills, tdd, to-spec, to-tickets, triage, wayfinder, wizard

Часть user-invoked (`disable-model-invocation: true`): ask-matt, to-spec, wayfinder и др. Они видны в `skills list`, модель сама их не зовёт — грузить через `skill_view`.

## Коллизии

`tdd` — если в профиле уже есть свой `tdd`, Pocock `tdd` не линковать. Переименование папки не помогает: индекс ключует по frontmatter `name:`.

## Не ставить отсюда вслепую

`skills/deprecated`, `skills/in-progress`, `skills/misc`, writing-* (beats/fragments/shape), obsidian-vault, grill-me/grilling вне engineering/. Пользователь сказал «скиллы Мэтта Покока» в инженерном контексте — это `skills/engineering/`.
