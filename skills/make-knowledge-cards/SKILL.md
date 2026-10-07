---
name: make-knowledge-cards
description: Converts a pasted article or a local Markdown/TXT file into 5-8 focused knowledge cards with title, core knowledge, explanation, and an example or self-test question. Use for making study or knowledge cards from an article or notes. Does not handle URLs, PDF, Anki export, or GUI content.
license: MIT
---

# Make Knowledge Cards

## Overview

Turn one source — an article pasted into chat, or a local `.md`/`.markdown`/`.txt` file — into a deck of **5–8 knowledge cards**. Each card captures one reusable piece of knowledge from the source and nothing else.

## Inputs

| Input | How to handle |
|---|---|
| Article text pasted in chat | Process directly |
| Local path ending in `.md`, `.markdown`, `.txt` | Read the file as UTF-8 |
| URL or web page name (`http://…`) | Do not fetch — ask the user to paste the text |
| `.pdf`, `.docx`, `.epub`, images, slides | Do not parse — ask for Markdown/TXT or pasted text |
| Anki/APKG export, or a request for a GUI app | Out of scope — say so in one sentence |

One source per deck. If several files are given, ask which one to start with.

## Workflow

### 1. Read the whole source first

Read the complete text before writing anything. Detect the source language; every label, title, and sentence in the deck uses that language.

### 2. Extract candidate knowledge points

List the points a reader must remember. A point is one of:

- a definition or concept
- a rule, principle, or procedure
- a causal mechanism or reason
- a key distinction or common confusion
- a non-obvious fact with practical value

Skip anecdotes, filler, repeated restatements, and details that merely support a larger point.

Hard rules:

- **One point per card.** Merge points that are paraphrases or sub-parts of each other.
- **Source only.** Every claim must be grounded in the source. Never add outside facts, examples, explanations, or "common knowledge" the source does not state.
- **Aim for 5–8 points.** Order by importance, or by source order when importance is tied.
- **Never pad.** If the source genuinely contains fewer than 5 distinct points, produce 3–4 cards and add the thin-source note under the deck title. With fewer than 3 real points, output those and tell the user the source is too thin. Do not split one point into two, and do not invent points to reach 5.

### 3. Draft the cards

Use the exact output format below. For each card:

- **Title** — names the single point, not a topic area. Keep under about 20 CJK characters or 12 English words.
- **Core Knowledge** — one sentence stating the atomic takeaway.
- **Explanation** — 1–3 sentences on what it means, how it works, or its scope, drawn only from the source. If the source states a rule without giving a reason, clarify its meaning or scope instead of inventing reasons, benefits, or background.
- **Example or Self-Test** — exactly one item:
  - prefer a concrete example from the source; it must not reuse the same case already cited in Core Knowledge or Explanation (instantiating an abstract placeholder with a value from the source is allowed);
  - otherwise pose one self-test question — question text only. It may pose a hypothetical scenario for the learner to apply the point, but it must not assert facts beyond the source and must not include or hint at the answer.

### 4. Validate deterministically

Write the draft deck to a temporary `.md` file and run, from the skill directory:

```
python scripts/validate_cards.py <draft.md>
```

(Use `python3` or `uv run python` depending on the environment.) Fix every reported error and re-run until it exits 0. Review each warning; a fewer-than-5 warning is acceptable only for a genuinely thin source carrying the thin-source note.

### 5. Deliver

Show the deck in chat. Write a `<name>.cards.md` file only when the user asks, by default next to the source file.

## Output format

The validator parses these exact markers:

- One level-1 heading with the deck title.
- Each card is a level-3 heading starting with its sequential number: `### 1. Title`.
- Each card contains exactly three field bullets in the fixed order below, each with a bold label.
- Nothing else inside a card — no nested bullets, no sub-headings.

Labels follow the source language:

| Language | Field 1 | Field 2 | Field 3 |
|---|---|---|---|
| 中文 | 核心知识 | 简明解释 | 示例或自测 |
| English | Core Knowledge | Explanation | Example or Self-Test |
| Other | Translate the same three labels naturally |

Template (English labels shown):

```markdown
# Knowledge Cards: <deck topic>

### 1. <Point title>
- **Core Knowledge:** <one-sentence takeaway>
- **Explanation:** <1-3 sentences, grounded in the source only>
- **Example or Self-Test:** <one source example, OR one answer-free question>

### 2. <Point title>
- **Core Knowledge:** ...
- **Explanation:** ...
- **Example or Self-Test:** ...
```

For a thin source, add this line directly under the title, in the source language:

- 中文：`> 说明：原文只包含 N 个独立知识点。`
- English：`> Note: the source covers only N distinct knowledge points.`

## Final self-check

- 5–8 cards (or 3–4 with the thin-source note); never more than 8.
- Each card teaches exactly one point, and no two cards overlap.
- No information, examples, or answers beyond what the source contains.
- Every self-test item is a question without an answer.
- Labels and language match the source.
