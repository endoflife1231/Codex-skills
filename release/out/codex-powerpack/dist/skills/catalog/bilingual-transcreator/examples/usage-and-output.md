# Usage and Output Examples

These examples demonstrate behavior, not fixed brand voice.

## 1. Adaptive RU → EN landing page

### Request

```text
Use $bilingual-transcreator. Adapt this into en-US for a B2B landing page:
«Сервис помогает командам быстрее согласовывать договоры и не терять правки в бесконечных цепочках писем. Подключение занимает один день.»
```

### Strong output

```text
Get contracts approved without chasing changes across endless email threads.

The platform keeps comments, revisions, and approvals in one place, so your team can move from draft to signature faster. Setup takes one day.
```

Why it works:

- The first sentence carries the customer tension rather than the Russian syntax.
- “Setup takes one day” preserves the claim exactly.
- It does not invent percentages or customer proof.

## 2. Adaptive EN → RU email

### Source

```text
You don't need another dashboard. You need to know which accounts are about to churn—and what to do next.
```

### Strong output

```text
Ещё один дашборд проблему не решит. Важно вовремя увидеть клиентов, которые могут уйти, и понять, что делать дальше.
```

A weaker literal version would preserve the English contrast formula and overuse «вам нужно».

## 3. Campaign mode

### Request

```text
$bilingual-transcreator target=ru mode=campaign channel=paid-ad
Source: “Close the books without the month-end scramble.”
Context: accounting automation; do not claim full automation.
```

### Possible routes

```text
Закрывайте месяц без аврала в последние дни.
```

```text
Меньше ручной сверки. Спокойнее закрытие месяца.
```

```text
Все данные к закрытию месяца — без гонки по таблицам.
```

The routes preserve the tension but avoid promising that the product closes the books autonomously.

## 4. Risk note

### Source

```text
Our platform guarantees a 40% reduction in operating costs.
```

When no evidence is supplied, do not soften or strengthen silently. Return a conservative provisional version and a brief risk note when notes were requested:

```text
Наша платформа помогает сокращать операционные расходы.
```

Risk: the source contains a guaranteed quantified claim. Restore “40%” only with approved evidence and required qualification.

## 5. When not to transcreate

For a contract clause, certified document, medication instruction, or mandatory legal disclosure, use precise translation and professional review. The skill should say that creative adaptation is inappropriate for that portion.
