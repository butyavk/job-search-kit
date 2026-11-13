---
name: company-trainer
description: Build a trainer for one coding stage at one company — interview-level tasks on the company's domain and stack with hidden questions, starters, tests and reference solutions, cards, a protocol, a plan by days, and optionally a one-page browser trainer. Use when a stage is a coding screen whose language or domain the general Live Coding Map does not cover (TypeScript, Go, an API platform, algorithms), or the candidate asks for a trainer for a company.
---

# A trainer for one company's coding stage

For SQL and Python in general, use the open Live Coding Map first (skill `live-coding`). Build a company trainer when the stage needs the company's own domain or another stack. A trainer built this way once gave «Excellent» on both live-coding tasks; another — a course of 10 lessons, 61 exercises and 13 interview tasks for a TypeScript screen.

## 1. Before building
- The stage's format from the prep (skill `interview-prep`, steps 1–2): language, platform, length, number of tasks, what the interviewer looks at.
- The domain: the company's product, its public API docs, the posting's words. The tasks are «from work» at that company, not puzzles.
- The candidate's level in the language (ask): it decides between a course with lessons and only tasks.

## 2. Layout (a folder or a repository)
```
STATE.md  DECISIONS.md
research/   format.md  company.md  sources.md
plan/       odds.md  plan.md
tasks/      <id>/README.md  ASK.md  starter.<ext>  tests.<ext>  WALKTHROUGH.md
solutions/  <id>.<ext>
cards/      drills.md  traps.md  talk.md
data/       schema and data for SQL
docs/       protocol.md  one_page.md  recipes.md  cheatsheet.md  glossary.md  think_aloud.md  my_mistakes.md
mocks/      bank.md (hidden)  log.md
scripts/    verify  check
```

## 3. A task
- `README.md` — the statement in the interview language, with details deliberately left out (as interviewers do), topic, difficulty, target time.
- `ASK.md` — the questions to ask before coding and the interviewer's answers, hidden and revealed one at a time.
- `starter`, `tests` (the example, edge cases, a wrong-but-plausible case), a reference solution, `WALKTHROUGH.md`.
- `scripts/check <id>` — what matched and the first difference «expected / got». `scripts/verify` — every reference solution green, every starter red. Run it after every change.

## 4. By type of stage
- **Algorithms:** patterns by the company's frequency (hash map, two pointers, sliding window, stack, binary search, BFS/DFS, topological sort, heap, intervals, prefix sums, DP, backtracking); per pattern a skeleton in the cheat sheet and 2–4 tasks, one «from the domain».
- **SQL:** a synthetic database of the domain, 5–8 tables, thousands of rows, **traps in the data** (test records, NULLs, duplicate events, records without a pair, the period boundary). The expected output comes from running the reference. In the browser — PGlite.
- **Python:** tasks «from work» — dictionaries, sorting by keys, money in Decimal, dates, splitting an amount, deduplication, a time window, retry, idempotency. Checked by pytest; in the browser — Pyodide.
- **TypeScript and other stacks:** the same on the stack's runtime (Node 22.18+ runs .ts; type check separately with `tsc`), plus **code-review exercises**: code with problems → find them on a timer → a debrief by severity, a verdict aloud, the interviewer's questions.

## 5. Cards, protocol, plan
- Cards: drills (3–5 minutes, one idea), traps («say what it returns, then run it»), talk (question → a 3–4-sentence answer aloud).
- `docs/protocol.md` — the 25-minute protocol from `live-coding`, adapted to the stage; the sticker: **REPEAT → ASK (batch) → COMMENTS → PLAN → CODE → CHECK vs COMMENTS**.
- `docs/my_mistakes.md` — a living list: a mistake repeated twice becomes a rule in the protocol.
- `plan/plan.md` — a plan by days up to the interview, with hours per day and checkboxes.

## 6. Optional: a one-page browser trainer
One HTML page — tasks and cards, Pyodide or PGlite, an editor, Run and Check, the plan with checkboxes, the cheat sheets, progress. Built by a script from the repository files, with expected outputs computed at build time. Publish it as an artifact where the session can; progress lives in the artifact's storage, not in the browser.

## 7. Mocks and audits
- A task from `mocks/bank.md`, not shown in advance. Claude is the interviewer: answers only what is asked, keeps time, gives no hints. At the end: «Is this what we agreed?», «How would you sanity-check it?», a question about production.
- The debrief by the protocol's steps with the time of each; look for the repeating pattern. Result into `mocks/log.md`.
- An audit every two days: format fit; errors in statements and references (rerun `verify`); over-complication and unfair time; contradicting cheat sheets; what comes up but is explained nowhere.
