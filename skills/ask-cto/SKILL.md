---
name: ask-cto
description: Explain which SOUL mode and skills fit this request.
disable-model-invocation: true
version: 1.2.0
author: Merlin, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [routing, cto]
    related_skills: [how-to-talk, writing-for-agents, cli-agent-first]
---

# Ask CTO

Раскрывает `SOUL.md`. Своего процесса не добавляет.

## Когда применять

- Человек написал `/ask-cto`.
- Спросил, какой режим или какие навыки взять.

Если человек уже назвал навык, загрузи его. Не перемаршрутизируй.

`ask-matt` закрывает только семейство Matt Pocock.

## Как отвечать

1. Прочитай живой проект, инструкции репозитория, `git status` и владение. Прямой источник сильнее памяти.
2. Выбери один пункт из раздела «Рабочие режимы» в `SOUL.md`.
3. Возьми навыки только из списков `SOUL.md`. Пиши frontmatter-имя (`to-spec`), не путь папки.
4. Текст другому агенту пиши через `writing-for-agents`. Ответ человеку — через `how-to-talk`.
5. Работа закончена только когда есть проверенный артефакт: тесты, живой вывод, diff, файл, URL или состояние сервиса.

Не выдумывай пятый режим. Не проси человека заполнять контракт из полей. Назови режим, назови навыки, сделай работу или скажи, какого навыка нет в профиле.
