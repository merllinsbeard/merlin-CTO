# Skill map

Every merlin-cto skill except this router. Open a row only when the request matches its signal. Do not load the whole file into the answer. Name one skill, or one short sequence.

SOUL wording is copied as-is where the skill sits on the SOUL lists.

## Speech

- `how-to-talk`. Перед каждым ответом человеку, до профильного навыка задачи. Задаёт подачу, не предметное решение.
- `unslop`. Cut AI tells from any writing. Финальный проход человеческому тексту.
- `concise`. Человек просит короче: «короче», «кратко», «без воды».
- `wait-what-bro`. Прошлая подача не села. Перескажи то же проще, без нового исследования.

## Who writes

- `cli-agent-first`. Выбрать прямое исполнение, сабагента или coding CLI. Сначала этот навык, если выбор «я или writer».
- `cto-subagent-development`. Native `delegate_task` для независимого исследования или изолированных правок. Родитель держит решения и приёмку.
- `ticket-campaign-execution`. Закрыть уже опубликованный граф тикетов. Один writer на тикет.
- `subagent-driven-development`. План через сабагентов с двухступенчатым ревью. Бери, только если этот цикл уже принят в репо.
- `concurrent-coding-agent-coordination`. Несколько coding-агентов уже пересеклись на одном репо. Назначь одного владельца записи.
- `principle-never-block-on-the-human`. Обратимую работу делай сам и покажи результат. Спрашивай только на необратимом.

## Writers

Load only after `cli-agent-first` named this sibling. Check the binary and login first.

- `codex`. OpenAI Codex CLI. Security, money, irreversible, costly failure.
- `claude-code`. Claude Code CLI. Features, PRs, autonomous repo work.
- `opencode`. OpenCode CLI. Provider-agnostic writer or PR review.
- `computer-use`. Desktop in the background, without stealing the user's focus.

## Work management

- `unlazy`. Довести большую автономную задачу до проверяемого результата. Убивает отчёт на 80 процентах.
- `ponytail`. Выбрать самое простое решение, которое действительно работает.
- `principle-laziness-protocol`. Минимальный diff, закрывающий корень задачи.
- `principle-sequence-verifiable-units`. Выполнять большую работу проверяемыми частями.
- `principle-prove-it-works`. Доказать результат запуском, тестом или живой проверкой.
- `principle-guard-the-context-window`. Выносить большие независимые ветки из главного контекста.
- `how`. Обьяснить как, включая инфоргафики через каноничные скиллы. Как устроено и где живёт. Не вместе с `why` на один вопрос.
- `why`. Обьяснить почему так сделали, по коммитам, тикетам и докам, включая инфоргафики через каноничные скиллы. Не вместе с `how` на один вопрос.

## Specs and tickets

- `grill-me`. Relentless interview, no working directory.
- `grill-with-docs`. То же в репо: пишет ADR и glossary по ходу. Человек набирает `/grill-with-docs`.
- `to-spec`. Оформить и опубликовать согласованную спеку с проверяемыми условиями готовности.
- `to-tickets`. Разбить спеку на автономные вертикальные тикеты с необходимыми `blocked_by`.
- `plan`. Markdown-план в `.hermes/plans/`. Без исполнения.
- `implement`. Собрать работу по спеке или тикетам.
- `implement-spec`. Собрать уже данную спецификацию.
- `triage`. Сырые issues и внешние PR. Не триажь тикеты, которые уже написал `to-tickets`.
- `wayfinder`. Когда объём не помещается в одну сессию и решений ещё нет. Человек набирает `/wayfinder`.
- `to-questionnaire`. Недостающие факты живут в чужой голове. Человек набирает `/to-questionnaire`.
- `ask-matt`. Только семейство Matt Pocock. Человек набирает `/ask-matt`.

Сначала согласованная спека, потом тикеты. Реализацию внутри шага спеки не пиши.

## Architecture

- `improve-codebase-architecture`. Парный к уже стоящему codebase-design: тот проектирует глубокий модуль, этот сканирует живой код на мелкие модули и предлагает, что углубить. Человек набирает `/improve-codebase-architecture`.
- `principle-model-the-domain` и `domain-modeling`. Сначала моделировать stateful-логику и ветвящиеся правила.
- `principle-type-system-discipline`. Делать неверные состояния трудно выразимыми.
- `principle-boundary-discipline`. Держать валидацию и ошибки на правильных границах.
- `principle-separate-before-serializing-shared-state`. Разделять владельцев состояния до добавления блокировок.
- `codebase-design`. Проектировать глубокие модули и ясное владение ответственностью.
- `code-wiki`. Собирать вики по репо: обзор, архитектура, модули, Mermaid. Что и как устроено, не зачем так решили.
- `research`. Первоисточники и цитируемый файл. Потом этот файл в `/grill-with-docs`.
- `prototype`. Одноразовая программа, которая отвечает на вопрос дизайна.
- `spike`. Одноразовый технический эксперимент до сборки. В продукт не мержи.
- `codebase-inspection`. LOC, языки, соотношения. Инвентарь, не вики.
- `codebase-capability-map`. Карта возможностей платформы из исходников и доков: что система умеет на самом деле.
- `software-architecture-visualization`. Картинка архитектуры только из фактов репо.
- `setup-ts-deep-modules`. TypeScript-пакеты как глубокие модули через dependency-cruiser.

## Correctness

- `blast-radius`. Найти затрагиваемые контракты, данные, вызовы и соседние пути.
- `principle-fix-root-causes`. Исправлять причину, а не симптом.
- `tdd`. Использовать по явному запросу или когда красный тест лучше всего фиксирует границу дефекта.
- `tdd-bug-fix`. Человек явно просит TDD на баге. Набирает `/tdd-bug-fix`.
- `test-driven-development`. Официальный bundled TDD. Рядом с `tdd` не грузи. Предпочитай `tdd`.
- `diagnosing-bugs`. Жёсткий баг или регрессия, цикла ещё нет.
- `systematic-debugging`. Четыре фазы, цикл уже красный.
- `rest-graphql-debug`. Живой REST или GraphQL: статус, auth, схема, воспроизведение.
- `node-inspect-debugger`. Node `--inspect` и CDP, когда `console.log` мало.
- `python-debugpy`. pdb или remote DAP для Python.
- `ast-grep`. Поиск и перепись по форме AST, не по тексту.
- `typescript-best-practices`. TypeScript-синтаксис поверх `principle-type-system-discipline`.
- `simplify-code`. Четыре параллельных ревьюера недавнего diff.

## Review and release

- `code-review`. Две оси: стандарты репо и спека, от `HEAD` до зафиксированной точки.
- `requesting-code-review`. Локальный проход до коммита: сканы, гейты, автофикс.
- `github-code-review`. PR на GitHub, inline через `gh` или REST.
- `sdlc-review`. Ревью handoff в полосе Kanban. Не подменяет исполнителя.
- `kanban-board-operations`. Почистить или сверить переполненную Kanban-доску. Это состояние доски, не код-ревью.
- `oracle`. Второй модели дай бандл промпта и файлов. Совет, не факт.
- `production-release-verification`. merged, released, deployed, live-accepted держи раздельно. Health-check не закрывает пользовательский сценарий.

## GitHub and git

- `github-auth`. HTTPS-токен, SSH, `gh login`.
- `github-issues`. Создать, разметить, назначить issue.
- `github-issue-to-pr`. Issue до проверенного PR с честным CI.
- `github-pr-workflow`. Ветка, коммит, open, CI, merge.
- `github-repo-management`. Clone, fork, remotes, releases.
- `resolving-merge-conflicts`. Уже идёт merge или rebase. Никогда не делает `--abort`.
- `merge-reconciler`. Нейтральная третья сторона, когда конфликтуют две агентские ветки.
- `handoff`. Портативный файл в другую сессию, директорию или harness. Человек набирает `/handoff`.

## Frontend and product

- `design-taste-frontend`. Новый лендинг или портфолио, не шаблон.
- `redesign-existing-projects`. Поднять существующий сайт или приложение.
- `frontend-premium-audit`. Дыры премиального качества, file:line, без правок в этом шаге.
- `dogfood`. Живой исследовательский QA. Дефекты пиши, потом возвращайся в поток сборки.
- `product-surface-review`. Обещание продукта против живого текста и побочных эффектов.
- `image-to-code`. Сначала картинка дизайна, потом вёрстка по ней.
- `popular-web-designs`. 54 живых дизайн-системы как HTML/CSS.
- `claude-design`. Разовый HTML: лендинг, колода, прототип.
- `design-md`. Файл токенов DESIGN.md.
- `page-agent`. Встроенный в страницу GUI-копилот.

## Pictures

- `visualize`. Чарт, карта, симулятор, мокап в чат.
- `baoyu-infographic`. Инфографика, сетка раскладок и стилей.
- `excalidraw`. JSON-схема, которую можно открыть на excalidraw.com.
- `image`. Сгенерировать или править картинку.
- `software-architecture-visualization`. См. Architecture. Только из фактов.

## Infra and Hermes

- `docker-management`. Контейнеры, образы, тома, Compose.
- `remote-machine-access`. Нативная работа с Mac и удалёнными хостами.
- `hermes-agent`. Настройка и диагностика Hermes. Официальная документация остаётся главным источником.
- `hermes-desktop-debugging`. Desktop ведёт UI-действие не туда. Трассируй как переход состояния, не как один обработчик кнопки.
- `inspecting-hermes-desktop-dom`. Прочитать живой DOM/CSS Desktop через CDP.
- `hermes-profile-skills`. Подключить навыки в изолированный профиль.
- `hermes-profile-governance`. Аудит и сопровождение поведения профиля целиком.
- `public-hermes-profile-distribution`. Опубликовать переносимый профиль с доказательствами.
- `hermes-agent-skill-authoring`. Писать in-repo SKILL.md: frontmatter и структура.
- `oauth-login-debug`. Живой провал OAuth/OIDC. Сначала пробы против сайта, не догадки по докам.
- `wizard`. Шаги, которые может кликнуть только человек.
- `cloudflare-temporary-deploy`. Временный живой Worker без аккаунта.
- `durable-static-site-forms`. Статический сайт должен реально сохранить заявку.
- `har-derived-api-client`. Записать XHR в HAR и вывести HTTP-клиент.
- `computer-use`. См. Writers.

## Knowledge

- `writing-for-agents`. Любой текст, который исполняет агент: AGENTS, CLAUDE, skill, prompt, spec, ticket, Kanban card или delegate-task.
- `principle-encode-lessons-in-structure`. Закреплять повторяющиеся уроки в коде, типах, тестах или skills, а не в напоминаниях.
- `codebase-inspection`. См. Architecture.
