---
name: answer-blocks
description: Build interview answers from the candidate's answer blocks (Lego-style pieces — whole story, first line, context, action, result, lesson) and keep the block library consistent and fact-checked. Use when answering or rehearsing any interview question, writing or editing a block or recipe, adding a fact, or checking the pack.
---

# Answers from blocks

The pack keeps answers not as texts but as **blocks**: small checked sentences from which any answer to any question for any company is built. A block is one thought, in English and in the candidate's native language; an answer is a chain of blocks.

Two integrity rules:
1. **Every block reads without its neighbours.** It names the project or company («At Shoply, …», «Our checkout service …»); it does not open with «Then», «So», «That», «It», «Also» or a pronoun with nothing to point to. The check catches such openings.
2. **Every story has a whole-story block `S`** (20–40 seconds): situation, own action, result and, if there is one, the lesson — in 3–5 sentences. It answers the question on its own; details (`C`, `A`, `R`, `D`, `L`) are added on follow-ups. A topic with an `R` block, or with both `O` and `L`, counts as a story.

## Where things are
- `me/blocks/*.md` — blocks, by topic.
- `me/recipes.md` — bank question → first line and chains (short and long), and the story set.
- `me/facts.md` — facts with definition, source and confirmation date; a block claims nothing that is not there.
- `me/never-say.md` — bans and filler words.
- `bank/questions.md` in the kit — the universal question bank with IDs; `me/questions-extra.md` — the candidate's own extra questions (`Q01`…).

## Block format
```
#### CHK-A1 · Short title
`A` · tags, comma separated · ~8 s
- EN: One to three sentences, ready to say, in the candidate's register.
- XX: The same in the native language, same meaning (XX = its two-letter code: RU, ES, DE…; none for a native English speaker).
- ⚠ What not to say next to it, if anything.
```
ID = topic + type + number: `CHK-A1`. Exception: one-line templates for logistics and questions to the interviewer — `LOG-1`, `ASK-1`, no type letter. The second line uses the two-letter code of the native language from `me/profile.yaml` → `languages.native` (`RU:`, `DE:`, `ES:` …); a native English speaker has only `EN:`. The English register follows `languages.english` (skill `english-register`). Examples below come from the made-up story in `examples/example-story.md` (Shoply). Types:

| Type | What it is | Example |
| --- | --- | --- |
| `S` | the whole story in 20–40 s, answers the question on its own | «At Shoply, our checkout went down almost every week … the outages stopped.» |
| `O` | the first line — the answer straight away | «At Shoply, our checkout went down almost every week.» |
| `C` | context: where, who, scale | «I was the engineering manager of the payments team, six engineers.» |
| `A` | what I did — an I-sentence | «I went through the logs and traces myself…» |
| `R` | result with a number | «The outages stopped, and sales-day conversion grew by 4%.» |
| `D` | how the number was measured | «Our analysts compared the sale with the previous one.» |
| `L` | lesson, the rule since | «Today I would add an alert on the queue from day one.» |
| `P` | position, belief | «I believe in small teams that own their product.» |
| `G` | an honest gap in one sentence | «I have not run a team of more than ten engineers yet.» |
| `Q` | answer to a frequent follow-up | «Yes, the alert came a month later, and it was my call.» |

A block may have two types (`R` · `D`) when the result comes with its definition.

## Building an answer
1. Find the question in the bank (ID) or the nearest one. Take the recipe from `me/recipes.md`.
2. Choose the length: a recruiter and little time — short (for a story, its `S` block, 25–35 s); a hiring manager, a panel, a CTO — long (45–90 s): `S`, then details on follow-ups.
3. The first line is the `O` block, word for word. An `A` or `R` block (an I-sentence) within the first two sentences.
4. The other blocks in order; when speaking, own words are fine as long as the meaning is the block's.
5. For a company — one bridge sentence at the end (their problem ↔ my block). Bridges live in the company's prep document, not in the pack.
6. Check: nothing from `never-say.md`; one story is not told twice in one process (`templates/story-split.md`); English through `english-register`.
7. Show the answer as: the first line, the anchor of block IDs (`CHK-O1 → CHK-A1 → CHK-R1`), the full text.

No recipe — build one from existing blocks by tags, show it, and after the candidate's «yes» add the row to `me/recipes.md`.

Recipe columns: «First line» — the ID of an `O` (or `S`) block; «Short» and «Long» — chains of IDs in backticks. «Notes» is free text: the nearest story, ideas for later and ID hints go there; IDs in notes do not count as coverage. A recipe that uses a draft block counts as a draft.

## Adding or changing a block
- A new fact from the candidate: first a row in `me/facts.md` (source «said on <date>», the confirmation date), then the block.
- A new story: the `S` block first, then details. A new block takes the next free number in its topic. IDs never change: recipes and prep documents point to them.
- An outdated or wrong block — do not delete it: fix the text and add `⚠ corrected <date>: was …`. If the meaning changed completely — a new block, and mark the old one `⚠ outdated since <date>, use <ID>`.
- A fact the candidate has not confirmed — the block keeps `· draft` in its type line; drafts never go into answers.
- A confirmed wording with slots that `/prep` fills per company or vacancy (`<one concrete thing in this role>`) is marked `· template` in its type line; its slots are not unfinished text.
- After editing: `python3 <kit>/scripts/check_pack.py` (it finds the pack itself: `--me`, `$JOB_SEARCH_ME`, `../me` next to the kit, `./me`) — links, duplicate IDs, register, bans, drafts, coverage. No shell (claude.ai) — the checklist below.

## Checklist without the script
The same list as `check_pack.py`, by eye, over the changed files:
1. Every block has `#### ID · title`, a type line in backticks, `- EN:` and the native-language line (none for a native English speaker). No ID repeats.
2. Every ID in `recipes.md` chains and in block text exists.
3. No block opens with a link word (Then, So, That, It, Also …); the project or company is named.
4. English: no contractions (I'm, don't), every sentence under 30 words, 12–15 words on average, under 13% of words with 8+ letters (targets per level in `english-register`). A native English speaker: only the sentence length and the AI-word and never-say rules apply; contractions are fine.
5. No filler from `never-say.md` and no claim from its «Never claim» table, except in the blocks that row names.
6. Confirmed blocks have no `<…>` placeholders longer than one word; one-word slots like `<company>` are fine.
7. Every story (an `R`, or `O` and `L`) has an `S` block.
8. Core ★ and the ◆ of the candidate's track (`target.track`): each has a recipe without drafts, or «—» and a note on when to come back.

## Fact check
The format check does not prove the facts. Once a month (`/review`) and after big edits:
1. Put every source on disk: the files listed in `fact_sources` of `me/profile.yaml` — story bank, prep documents, interview debriefs, notes, CV (the CV ranks lowest). A check against the CV alone does not count.
2. Freeze the pack (a copy with the date).
3. A **separate agent**, which did not write the blocks, checks every block against every source and gives a verdict per block: `OK`, `CONFLICT` (a source says otherwise — quote both), `OVERCLAIM` (the block says more than the source), `NOT FOUND` (no source), `EN≠XX` (the two language lines differ in meaning). Without an agent, do it in a fresh session with only the files.
4. Claude shows the candidate only what is not `OK`, one question per item, and fixes blocks and facts after their answer.
5. The verdicts go to `me/fact-check-<date>.md`, so the next check starts from them.

Notes from 1:1s and feedback about other people are sources for the candidate's own facts only: they are never quoted, paraphrased or named in anything an employer reads.

## From an interview into blocks
After `/debrief`: each new phrasing that worked → a block or a block edit (during an open process only with a note: `templates/debrief.md`); each speech error → a line in `me/voice.md` or `me/never-say.md`; each new question → a row in `me/questions-extra.md` (next `Q` ID; the kit's bank is not edited from a pack) and a recipe.

## A cheat sheet
On request: for the questions of a stage, a table «question → first line → anchor of IDs → one or two numbers». First lines word for word; everything else as anchors.

## Do not
- Do not write a long «perfect answer» around the blocks: it drifts from the facts at the next edit.
- Do not invent numbers, roles or authorship to fill a gap in a chain. A gap is a question for the candidate.
- Do not mix blocks of two stories (a number from one with a client from another).
