---
name: humanizer
description: Edit or audit English prose to remove generic AI-writing patterns and restore a natural, specific,
  credible human voice without changing facts or inventing experience. Use for English humanization, anti-slop editing,
  and voice cleanup; not for detector evasion.
---

# Humanizer — natural English editorial pass

## Purpose

Make English text sound authored rather than statistically averaged. Preserve meaning, factual claims, uncertainty, citations, product terms, and the intended audience. This is an editorial workflow, not a promise to bypass AI detectors.

## Modes

- **Audit** — diagnose patterns and rank them by impact; do not rewrite.
- **Edit** — return one polished version plus concise change notes.
- **Voice-match** — infer a voice from user-provided samples, then edit toward that voice.
- **Deep pass** — load `references/upstream-pattern-catalog.md` and apply the full pattern catalog.

## Workflow

1. Identify purpose, audience, channel, and non-negotiable facts.
2. Read any brand voice, glossary, source copy, and examples the user supplied. Never fabricate a voice profile from nothing.
3. Mark high-impact problems first: vague abstraction, inflated significance, generic openings, repeated rhetorical templates, fake quotations, unsupported certainty, excessive headings/lists, uniform rhythm, and corporate filler.
4. Rewrite at the idea and paragraph level before polishing sentences. Prefer concrete nouns and verbs, observable details, calibrated claims, and varied sentence length.
5. Preserve useful structure. Do not make every text casual, choppy, funny, or first-person. Match the channel.
6. Run a fact-preservation pass: numbers, names, dates, conditions, legal qualifiers, links, citations, and product capabilities must remain accurate.
7. Run a voice/rhythm pass. Remove repeated sentence shapes, canned transitions, unnecessary summaries, and over-signposting.
8. Deliver the finished text. For review-only requests, do not overwrite files.

## Non-negotiable rules

- Do not add personal anecdotes, results, quotes, testimonials, urgency, guarantees, or credentials that were not in the source.
- Do not replace precise technical language with vague conversational language.
- Do not blindly remove all em dashes, headings, lists, or formal vocabulary; frequency and fit matter.
- Do not introduce grammar mistakes or random slang to simulate a human.
- Do not optimize for a detector score. Optimize for clarity, specificity, voice, and trust.
- When evidence is missing, weaken or flag the claim instead of decorating it.

## Quick pattern screen

Look for clusters rather than isolated words:

- grand claims such as “marks a pivotal moment” without evidence;
- “In today’s rapidly evolving landscape” openings;
- repetitive “not only X, but Y” or “it’s not X — it’s Y”;
- generic trios, forced symmetry, and conclusion sections that restate everything;
- abstract verbs like “leverage”, “unlock”, “redefine”, “elevate” where a concrete action exists;
- reader-address filler (“Whether you’re…”, “Let’s dive in”);
- suspiciously complete quotations or attribution without a source;
- paragraph and sentence lengths that barely vary.

For the complete catalog and examples, read `references/upstream-pattern-catalog.md`.

## Output

Unless the user requests another format, return:

1. **Revised text**
2. **Key editorial changes** — no more than 5 bullets
3. **Open factual questions** — only when unresolved claims remain
