# Bilingual Transcreator

Продуманный Agent Skill для **RU ↔ EN transcreation**: он не переводит текст построчно, а заново собирает его на целевом языке, сохраняя смысл, позиционирование, доказательства, голос бренда и действие, которое должен совершить читатель.

## Что входит

```text
bilingual-transcreator/
├── SKILL.md
├── references/
│   ├── transcreation-method.md
│   ├── russian-style.md
│   ├── english-style.md
│   ├── channel-playbooks.md
│   ├── claims-integrity.md
│   └── qa-rubric.md
├── assets/
│   ├── BRAND_CONTEXT.template.md
│   ├── VOICE_RU.template.md
│   ├── VOICE_EN.template.md
│   ├── GLOSSARY.template.csv
│   └── TRANS_CREATION_BRIEF.template.md
├── examples/
│   └── usage-and-output.md
├── evals/
│   ├── trigger-prompts.csv
│   └── quality-cases.md
└── scripts/
    ├── install.sh
    ├── install.ps1
    └── validate_brand_pack.py
```

## Использование в этом пакете

Skill уже установлен в `.agents/skills/bilingual-transcreator/`. Явный вызов:

```text
$bilingual-transcreator target=en mode=adaptive channel=landing-page @draft.md
```

Для глобальной установки вне этого пакета скопируйте папку в `~/.agents/skills/bilingual-transcreator/`.

## Рекомендуемая настройка

Скопируйте шаблоны в корень проекта и заполните их:

```bash
cp bilingual-transcreator/assets/BRAND_CONTEXT.template.md ./BRAND_CONTEXT.md
cp bilingual-transcreator/assets/VOICE_RU.template.md ./VOICE_RU.md
cp bilingual-transcreator/assets/VOICE_EN.template.md ./VOICE_EN.md
cp bilingual-transcreator/assets/GLOSSARY.template.csv ./GLOSSARY.csv
```

Минимально полезная конфигурация:

1. `BRAND_CONTEXT.md` — продукт, аудитория, позиционирование, доказательства, запрещённые обещания.
2. `VOICE_RU.md` — живые образцы и правила русского голоса.
3. `VOICE_EN.md` — отдельный английский голос, а не перевод русского профиля.
4. `GLOSSARY.csv` — утверждённые термины и запрещённые кальки.

## Режимы

- `faithful` — точная деловая адаптация с минимальной творческой свободой.
- `adaptive` — стандартный режим для сайтов, email, статей и соцсетей.
- `campaign` — несколько креативных направлений для рекламы, слоганов и запусков.

## Проверка бренд-пака

```bash
python3 bilingual-transcreator/scripts/validate_brand_pack.py .
```

Скрипт проверяет наличие и базовую заполненность файлов, но не оценивает качество самого текста.

## Дизайн skill

Основной `SKILL.md` намеренно компактный. Детальные языковые, маркетинговые и QA-правила загружаются только по необходимости. Это снижает расход контекста и упрощает развитие skill без раздувания главного файла.

## Версия

`1.0.0`
