# Surface probes

Читай этот файл, когда уже есть inventory и нужно, куда смотреть. Пути — типичные для expert-bot / Next chat+studio; в другом репо ищи те же роли, не эти имена.

## Identity

| Слой | Где смотреть | Вопрос |
|---|---|---|
| Канон | `CONTEXT.md`, спека продукта, шапка chat/login | Кем назван собеседник? |
| Runtime | `experts/<id>/runtime.json`, `prompts/system.md`, `prompts/style.md`, `prompts/answer.md` | Запрещает ли style то, что канон обещает? |
| Команды | router `/start` `/about` `/help` `/contact`; склейка disclosure | Пустой handle? Вечный «я не он»? Архив на каждом старте? |
| UI | login card, chat header subtitle, BotFather strings | Тот же термин, что в CONTEXT? |

Расхождение канона и style — дефект продукта, не «осторожный промпт».

## Access

| Проба | Зачем |
|---|---|
| `requireStudioAccess` vs `requireChatAccess` | Один и тот же гейт = ученик видит пульт |
| Ссылка Studio в шапке чата | Навигация шире роли |
| Deny-текст Telegram vs login copy | Одинаковый реестр или два входа |
| Capability на мутациях API | Видимость ≠ право писать; оба назови |

## Side effects

| Проба | Дефект, если |
|---|---|
| Кнопка «Поделиться» / share | `publish()` в markup ответа, а не в handler нажатия |
| Voice / Vision | Acceptance требует, флаги `false`, копирайт честно «только текст» — согласовано с конфигом, расходится со спекой запуска |
| Снимок | Модель read-only/TTL может быть верной при неверном моменте создания |

## Корпус (четыре счётчика)

1. Каталог: `content_state`, access_kind, число уроков.
2. Файлы: `experts/<id>/sources/**` минус `.gitkeep`.
3. Jobs: ready / failed / running; причина failed одной строкой.
4. Индекс и skill cards: `data-*/processed`, `experts/<id>/skills/` без `_README`.

Не складывай в фразу «материалы уже есть».

## Хаб и git

Хаб и OV entity — evidence прошлой сверки. Live: ветка канона, `origin/main`, worktree ingest, `.env` keys без значений. Checkout на уже влитой feature-ветке при отставшем локальном `main` — хвост live git, не «мы на актуальном main».
