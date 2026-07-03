# Codex Skills Pack — обновлённая локальная версия для IDE

Готовый репозиторный набор версии **2026-07-03.1** из **252 skills** для Codex CLI, IDE extension и Codex app. В этой версии исходный инженерный пак дополнен полноценными SEO, marketing, content-studio, RU/EN transcreation и editorial workflows; Claude-ориентированные части перенесены в нативные Codex skills, vendor helpers и project custom agents.

## Быстрый старт

1. Распакуйте содержимое архива **в корень Git-репозитория**. Рядом с кодом должны появиться `.agents/`, `.codex/` и `AGENTS.md`.
2. Если в проекте уже есть `AGENTS.md`, не заменяйте его: добавьте содержимое `.agents/AGENTS.fragment.md` в существующий файл.
3. Если в проекте уже есть `.codex/`, аккуратно объедините каталоги; custom agents лежат только в `.codex/agents/`.
4. Перезапустите Codex, если список skills не обновился автоматически.
5. В CLI/IDE используйте `$skill-name`, например `$debugging-and-error-recovery`, `$test-driven-development`, `$api-and-interface-design` или `$engineering-delivery-lifecycle`.

Codex сканирует `.agents/skills` от текущей директории до корня репозитория и загружает полный `SKILL.md` только после выбора skill. При большом наборе часть описаний может не попасть в первоначальный список, поэтому пакет содержит полный индекс и локальный маршрутизатор:

```bash
python3 .agents/tools/find_skill.py "исправить нестабильный тест и доказать причину" --top 8
```


## Как Codex должен читать пакет

- Сначала применяются правила из корневого `AGENTS.md` и более узких instruction-файлов в целевой части репозитория.
- Для явного workflow используйте `$skill-name`; без явного имени Codex выбирает skill по `description`.
- Полный skill загружается только после выбора; ссылки внутри `SKILL.md` открываются по мере необходимости.
- Project custom agents из `.codex/agents/` запускаются только явно и возвращают отчёт родительской сессии.
- Интеграционные skills не означают, что CLI, MCP, браузер, credentials или сеть уже настроены: Codex обязан проверить предпосылки.

Skills написаны преимущественно на английском, а управляющие README/AGENTS — на русском и английском. Это сделано намеренно: технические термины и upstream-инструкции сохраняются без потери смысла, а установка и маршрутизация остаются понятными русскоязычному пользователю.

## Что добавлено из agent-skills

### Определение и планирование

- `$interview-me` — выявить реальную цель и ограничения у недоопределённого запроса.
- `$idea-refine` — расширить варианты, проверить предположения и выбрать направление.
- `$spec-driven-development` — оформить спецификацию и acceptance criteria.
- `$planning-and-task-breakdown` — разложить работу на зависимые проверяемые задачи.
- `$context-engineering` — подготовить сфокусированный контекст для Codex.
- `$source-driven-development` — опираться на актуальные официальные первоисточники.

### Реализация и проверка

- `$incremental-implementation`, `$test-driven-development`, `$debugging-and-error-recovery`.
- `$frontend-ui-engineering`, `$api-and-interface-design`, `$browser-testing-with-devtools`.
- `$doubt-driven-development` — явная дорогая проверка рискованных решений свежим контекстом.

### Review и delivery

- `$code-review-and-quality`, `$code-simplification`, `$security-and-hardening`, `$performance-optimization`.
- `$git-workflow-and-versioning`, `$ci-cd-and-automation`, `$deprecation-and-migration`.
- `$documentation-and-adrs`, `$observability-and-instrumentation`, `$shipping-and-launch`.
- `$engineering-delivery-lifecycle` — явный end-to-end orchestrator для крупной фичи, миграции или релиза.

Исходный `using-agent-skills` не установлен отдельным meta-skill: он конфликтовал бы с уже существующим `$skill-router` и навязывал бы процесс даже для мелких правок. Его полезная lifecycle-карта объединена с `$skill-router` и новым `$engineering-delivery-lifecycle`.

## Custom agents Codex

В `.codex/agents/` находятся:

- `code_reviewer` — пятиосевой review;
- `security_auditor` — security-аудит и trust boundaries;
- `test_engineer` — test strategy и coverage gaps;
- `web_performance_auditor` — web performance audit без выдумывания метрик.
- `cavecrew_investigator` — компактный read-only поиск по коду.
- `cavecrew_builder` — ограниченные правки в одном-двух файлах.
- `cavecrew_reviewer` — компактное findings-only ревью.
- `impeccable_asset_producer` — готовит raster-ассеты из утверждённого Impeccable mock без смены арт-дирекшена;
- `impeccable_manual_edit_applier` — точечно переносит подтверждённые live-copy edits в исходники.

Агенты Impeccable, как и остальные project agents, запускаются только после явного разрешения пользователя. При отказе соответствующая работа остаётся в родительской сессии.

## Расширенные design-workflow

Три новых skill разделены по типу результата, чтобы не конкурировать за один запрос:

- `$impeccable` — существующий production product UI: dashboards, tools, forms, settings, accessibility, UX copy, audit/polish/hardening и live browser iteration;
- `$design-taste-frontend` — brand-led production frontend: landing pages, portfolios, campaigns, editorial sites и image-first marketing builds;
- `$huashu-design` — HTML-визуальные артефакты: hi-fi prototypes, interactive demos, decks, motion, MP4/GIF и narrated explainers.

Taste upstream содержал 13 skills. В пак зарегистрирован один `$design-taste-frontend`; полезные режимы brand-kit, image-to-code, web/mobile image direction, minimalist, brutalist, high-end, GSAP и Stitch перенесены в его `references/` и загружаются только по задаче. Legacy v1 и конфликтный `full-output-enforcement` исключены.

Huashu runtime разделён по возможностям: обычные HTML/CSS/JS-артефакты не требуют установки; PPTX/PDF/image/video/narration helpers проверяют зависимости перед запуском. Нелицензированные bundled BGM/SFX не включены. Impeccable hook не включается автоматически и требует явной команды плюс review/trust через `/hooks`.

Codex создаёт subagents только по явному запросу. Пример:

> Spawn `code_reviewer`, `security_auditor` and `test_engineer` in parallel, wait for all reports, then merge them into a GO/NO-GO ship decision.

## Caveman / Cavecrew

Из `caveman-main.zip` добавлены восемь Codex skills:

- `$caveman` — явный режим сверхкратких, но технически точных ответов;
- `$caveman-commit` и `$caveman-review` — компактные commit/review форматы;
- `$caveman-compress` — безопасное сжатие Markdown/text через candidate → validation → atomic apply;
- `$caveman-stats` — честное сравнение bytes/chars/words и грубая оценка токенов;
- `$caveman-help` — справка по набору;
- `$caveman-setup` — опциональная установка нативных Codex hooks;
- `$cavecrew` — маршрутизация трёх компактных custom agents.

Критичные миграции:

- вызовы Anthropic API и `claude --print` удалены; сжатие выполняет текущая сессия Codex локально над candidate-файлом;
- Claude session-log статистика заменена на детерминированное сравнение файлов, потому что формат Codex transcript не является стабильным интерфейсом;
- Claude/Gemini/OpenCode slash-команды и tool manifests заменены на `$skill-name`, `.agents/skills/` и `.codex/agents/*.toml`;
- постоянные hooks не включаются автоматически: `$caveman-setup` сначала показывает diff/preview и требует подтверждения, после чего пользователь отдельно доверяет hook через `/hooks`;
- слишком широкие auto-trigger правила сужены, чтобы Caveman не перехватывал обычные commit/review задачи.

Большинство skills не требует npm-пакетов или внешних API. Для базовых helper-скриптов нужен Python 3. Расширенные Huashu export/media helpers и Impeccable live tooling сначала проверяют свои явно документированные Node/browser/FFmpeg-зависимости и не устанавливают их автоматически.

## Chrome DevTools MCP

Skill `$browser-testing-with-devtools` требует отдельного MCP-сервера. Пакет **не устанавливает и не запускает внешние зависимости автоматически**. Пример безопасной изолированной настройки:

```bash
codex mcp add chrome_devtools -- npx -y chrome-devtools-mcp@latest --isolated
```

Перед использованием Codex должен проверить наличие Node/npm, Chrome и активного MCP. Если зависимости нет, следует использовать `$playwright`/`$playwright-interactive` либо честно сообщить, что live-browser verification не выполнялась.

## Структура

- `.agents/skills/` — 252 Codex skills.
- `.agents/SKILLS_INDEX.md` и `.json` — полный каталог и происхождение.
- `.agents/tools/find_skill.py` — локальный поиск по задаче.
- `.agents/tools/validate_pack.py` — структурная проверка пакета.
- `.agents/tools/validate_integration.py` — глубокая проверка импортов, ссылок, skill-ссылок и Codex-переноса.
- `.agents/INTEGRATION_ANALYSIS.md` — полный анализ входных архивов, коллизий и решений переноса.
- `.agents/CODEX_INTEGRATIONS.md` — Codex-native MCP и credentials setup.
- `.agents/MIGRATION_REPORT.md` — что перенесено, изменено и исключено.
- `.agents/THIRD_PARTY_NOTICES.md` и `.agents/licenses/` — лицензии и происхождение.
- `.codex/agents/` — 33 проектных custom agents.
- `AGENTS.md` — правила выбора, безопасности и сочетания skills.

## Проверка после установки

```bash
python3 .agents/tools/validate_pack.py
python3 .agents/tools/validate_integration.py
python3 .agents/tools/find_skill.py "ваша задача" --top 8
```

Ожидаемый результат: `OK: 252 skills and 33 custom agents validated`.

## Правила использования

- Используйте узкий domain skill вместо широкого, когда он точнее соответствует задаче.
- Сочетайте skills последовательно, если они дополняют друг друга; не запускайте несколько почти одинаковых review-skills без причины.
- Проверяйте CLI, credentials, сеть и MCP до интеграционных действий. Нельзя изображать успешный вызов отсутствующего инструмента.
- Перед deploy, publish, push, merge, destructive migration и изменением внешних систем требуется явное подтверждение.
- Не выводите и не коммитьте secrets.

## Происхождение обновления

Workflow-skills и первые custom agents адаптированы из `agent-skills-main.zip` (MIT, Copyright © 2025 Addy Osmani). Caveman/Cavecrew добавлены из `caveman-main.zip` (MIT, Copyright © 2026 Julius Brussee). Claude/Gemini/OpenCode wrappers не копировались напрямую: полезная логика перенесена в Codex skills, project custom agents и опциональные нативные hooks.

# Обновление 2026-07-03.1: marketing, SEO и живой RU/EN-текст

## Что интегрировано

- **46 marketing skills**: product marketing, research, copywriting/editing, CRO, paid media, lifecycle, launch, pricing, retention, social, analytics, RevOps и другие.
- **31 SEO skills**: глубокий audit, technical/content/schema/hreflang/local/GEO/SXO, Google APIs, drift, backlinks, programmatic SEO и явные optional extensions.
- **15 content-studio skills**: brand setup, blog, social platforms, strategy, repurposing, calendar, presentation, infographic, image and video workflows.
- **8 language/editorial skills**: bilingual transcreation, English and Russian humanization, ru-text, professional EN→RU translation, Russian editing, Textovod integration and ASCII diagram editing.
- **24 additional custom agents**: 18 SEO specialists and 6 content specialists. Together with the existing 9 agents, the pack now contains **33**.

## Коллизии и дедупликация

- `$seo-audit` is the deep specialist suite; the marketing pack audit is preserved as `$marketing-seo-audit`.
- `$content-strategy` is the broad marketing strategy; the content-studio variant is `$content-editorial-strategy`.
- Three byte-identical copies (`ru-text`, `seo-dataforseo`, `seo-image-gen`) are registered once; all unique supporting files are retained.

## Optional live integrations

Use `.agents/CODEX_INTEGRATIONS.md` for Codex-native MCP and credential setup. Source Claude installers are intentionally not executed or required.

## Shared state and runtime paths

```text
.agents/product-marketing.md          # positioning and customer context for marketing skills
.agents/brand/                         # BRAND.md, VOICE.md, VISUAL.md for content skills
.agents/vendor/claude-seo/             # shared SEO Python helpers and data
.agents/vendor/marketingskills/tools/  # implementation/tool registry
.agents/vendor/content-skills/         # content utilities, styles and assets
.codex/agents/seo_*.toml               # optional SEO specialists
.codex/agents/content_*.toml           # optional content specialists
```

The pack does not install Python/Node packages, configure MCP servers, create credentials, call paid APIs, publish content, submit URLs, buy ads, or mutate external systems automatically. Every integration skill must preflight capabilities and request approval where side effects or spend are possible.

## Recommended text pipeline

```text
$product-marketing / $content-strategy
→ $copywriting or a narrow $content-* skill
→ $bilingual-transcreator when adapting RU↔EN
→ $humanizer or $humanizer-ru
→ $copy-editing and/or $ru-text
→ factual and claims check
```

## Recommended SEO routing

- Quick strategic/manual review: `$marketing-seo-audit`.
- Deep audit with bundled helpers: `$seo-audit`.
- One page: `$seo-page`.
- Technical, schema, hreflang, local, GEO or other specialist task: use the matching `$seo-*` skill.
- Live integrations such as Ahrefs, DataForSEO, Firecrawl, SE Ranking, Profound and Unlighthouse are explicit/optional and require their own setup.

