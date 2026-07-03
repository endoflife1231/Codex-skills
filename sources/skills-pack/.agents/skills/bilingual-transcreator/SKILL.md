---
name: bilingual-transcreator
description: Transcreate, localize, rewrite, and polish marketing or editorial text between Russian and English
  so it reads as original, natural, brand-consistent copy in the target language. Use for RU↔EN adaptation, bilingual
  campaigns, landing pages, ads, emails, social posts, product messaging, and removing literal translation or AI-sounding
  prose. Do not use for certified, legal, medical, or word-for-word translation where exact equivalence is required.
---

# Bilingual Transcreator

Produce target-language copy that preserves the source's **intent, factual meaning, positioning, proof, emotional effect, and required action** without preserving its sentence structure.

## Operating principles

1. Write as a native author in the target language, not as a translator.
2. Preserve facts, names, numbers, prices, conditions, legal qualifiers, product capabilities, and claim strength.
3. Adapt idioms, rhythm, emphasis, examples, cultural references, and CTA phrasing when needed.
4. Never invent proof, customer quotes, statistics, urgency, scarcity, guarantees, awards, or product capabilities.
5. Prefer concrete language and human cadence over polished-but-generic prose.
6. Do not optimize for AI-detector evasion. Optimize for clarity, credibility, voice, and audience response.
7. Treat Russian and English as separate writing systems. Never translate a brand voice profile mechanically.

## Determine the task

Infer these fields from the request and available project files:

- `source_language`: Russian or English
- `target_language`: Russian or English
- `locale`: `ru-RU`, `en-US`, `en-GB`, or another explicit locale
- `mode`: `faithful`, `adaptive`, or `campaign`
- `channel`: landing page, ad, email, social, article, product UI, sales, press, or general
- `audience`, `objective`, `offer`, `CTA`, and constraints

Defaults:

- Infer target language from the request. If not stated, use the opposite of the source language.
- Default to `adaptive` for marketing and editorial content.
- Default English locale to `en-US` unless project context indicates otherwise.
- Preserve the source format unless the user asks for restructuring.
- Ask a question only when a missing fact would materially change or invalidate the result. Otherwise state a minimal assumption only when useful and proceed.

## Load only the context you need

Look first for these files in the current project, then in the skill assets if project files do not exist:

- `BRAND_CONTEXT.md` — product, audience, positioning, evidence, prohibited claims
- `VOICE_RU.md` — Russian voice rules and examples
- `VOICE_EN.md` — English voice rules and examples
- `GLOSSARY.csv` or `GLOSSARY.md` — approved terms, translations, and forbidden variants
- `TRANS_CREATION_BRIEF.md` — task-specific objective and constraints

Use project-specific files over bundled templates. Never overwrite project files unless explicitly asked.

Read detailed references selectively:

- Core decision rules: [references/transcreation-method.md](references/transcreation-method.md)
- Russian writing: [references/russian-style.md](references/russian-style.md)
- English writing: [references/english-style.md](references/english-style.md)
- Marketing channels: [references/channel-playbooks.md](references/channel-playbooks.md)
- Quality control: [references/qa-rubric.md](references/qa-rubric.md)
- Claims and risk: [references/claims-integrity.md](references/claims-integrity.md)

## Workflow

### 1. Build a semantic brief

Before drafting, identify internally:

- the one job the text must do;
- the audience's situation, awareness, and likely objection;
- the core promise and supporting proof;
- the desired emotional temperature;
- the required CTA;
- non-negotiable facts and flexible creative elements.

Do not expose this analysis unless requested.

### 2. Create a source map

Separate the source into:

- **Locked:** facts, offer mechanics, product names, numbers, URLs, legal qualifiers, approved terminology.
- **Meaning:** claims, reasoning, hierarchy, objections, proof, CTA.
- **Adaptable:** idioms, metaphors, sentence order, paragraphing, examples, humor, cultural references.
- **Risky or unclear:** unsupported claims, ambiguity, source errors, culturally inappropriate references.

Correct obvious grammar errors silently. Do not silently repair a factual contradiction; flag it briefly.

### 3. Draft from meaning, not sentences

Temporarily ignore source syntax. Reconstruct the message in the target language using the semantic brief and target voice profile.

- Preserve message hierarchy, not paragraph-by-paragraph symmetry.
- Use natural target-language collocations.
- Replace idioms by function and emotional effect, not dictionary equivalence.
- Reorder information when target-language persuasion or comprehension requires it.
- Keep intentional repetition only when it carries rhetorical value.

### 4. Apply the target-language pass

For Russian, use [references/russian-style.md](references/russian-style.md).

For English, use [references/english-style.md](references/english-style.md).

Always:

- vary sentence length because the thought requires it, not by formula;
- use specific nouns and active verbs;
- remove throat-clearing, filler, inflated abstractions, and generic enthusiasm;
- avoid repetitive contrast formulas, mechanical triads, excessive headings, and slogan-like fragments;
- keep some texture and asymmetry when appropriate; do not sterilize the voice;
- retain technical terminology when it is the audience's natural language.

### 5. Adapt to the channel

Use [references/channel-playbooks.md](references/channel-playbooks.md) when the channel materially affects structure.

Check:

- opening strength;
- information density;
- reading context and platform conventions;
- CTA placement and specificity;
- character or length constraints;
- whether proof appears close enough to the claim.

### 6. Run the integrity pass

Use [references/claims-integrity.md](references/claims-integrity.md).

- Match claim strength to evidence.
- Preserve caveats and eligibility conditions.
- Do not convert possibility into certainty.
- Do not add false personalization, fake scarcity, fabricated social proof, or manipulative urgency.
- Retain regulated wording when source exactness is required; explain that this part was localized conservatively.

### 7. Run bilingual parity and QA

Use [references/qa-rubric.md](references/qa-rubric.md).

Verify that the result:

- delivers the same commercial or editorial objective;
- preserves all locked elements;
- contains no source-language calques;
- sounds native in the target locale;
- follows the target voice file;
- keeps the CTA and offer mechanics accurate;
- has no invented facts;
- is ready to publish, not merely grammatically correct.

Revise once after the QA pass. Do not show a rough draft unless requested.

## Modes

### `faithful`

Use for product documentation, executive communications, investor materials, support content, or text with low creative freedom.

- Preserve structure and nuance closely.
- Adapt syntax and idiom, but minimize rhetorical additions.
- Keep ambiguity if the source is intentionally ambiguous.

### `adaptive` — default

Use for websites, email, articles, social content, product marketing, and general brand communication.

- Preserve intent and facts.
- Freely change syntax, rhythm, paragraph order, idioms, and CTA wording.
- Optimize for naturalness and effectiveness in the target market.

### `campaign`

Use for ads, slogans, launch campaigns, headlines, and concepts where emotional equivalence matters more than lexical equivalence.

- Generate 3 distinct routes unless the user asks for one.
- Keep the same strategic promise and proof boundaries.
- Label routes by creative direction, not by “Option 1/2/3” when notes are requested.
- Explain the trade-off of each route in one sentence only when requested.

## Output contract

Default output:

- Return only the final target-language text.
- Preserve requested formatting.
- Do not preface with “Here is the translation” or explain routine edits.

When the user asks for review, strategy, or notes, return:

1. **Final copy**
2. **Key adaptations** — only material decisions
3. **Risk/ambiguity notes** — only real issues
4. **Alternatives** — only for disputed headlines, CTAs, idioms, or campaign lines

When the user requests bilingual output, present source and target in clearly labeled sections or a two-column table only if the text is short enough to compare comfortably.

## Hard failures to avoid

Never:

- translate line by line and then “polish” lightly;
- preserve Russian word order in English or English noun stacks in Russian;
- add clichés such as generic future-facing claims without evidence;
- use “not just X, but Y” repeatedly;
- intensify claims because stronger copy sounds more persuasive;
- replace precise terminology with casual synonyms;
- make every sentence short or every paragraph one sentence;
- force humor, slang, contractions, or colloquialisms against the brand voice;
- turn a neutral source into sales copy unless the user requests it;
- expose internal scoring or analysis by default.

## Example invocations

Codex invocation:

```text
$bilingual-transcreator target=en mode=adaptive channel=landing-page Rewrite @draft-ru.md using @VOICE_EN.md
```

Codex invocation:

```text
$bilingual-transcreator Transcreate launch-email-ru.md into en-GB. Preserve all product claims and use VOICE_EN.md.
```

Natural-language activation:

```text
Adapt this Russian landing-page copy into natural US English. Keep the offer exact, remove literal translation, and make it sound like our brand.
```
