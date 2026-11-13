---
name: live-coding
description: Train and run live-coding rounds in SQL and Python — the 25-minute protocol, requirements as comments, think-aloud phrases, timed mocks with Claude as a silent interviewer, debriefs; tasks and in-browser checking through the Live Coding Map site. Use when a stage includes live coding, a SQL or Python screen, or a pair-programming round, for /prep and /mock live-coding.
---

# Live coding — SQL and Python

Tasks and checking live on the open site **Live Coding Map**: SQL and Python exercises, traps, 32 interview-level tasks with in-browser checking (PostgreSQL and Python in WebAssembly) and hidden edge-case data, a timed mock, plans for 1, 2–3 and 4–6 weeks, cards and Anki decks; in English and Russian, no sign-up: https://butyavk.github.io/live-coding/ (source: https://github.com/butyavk/live-coding). The candidate solves there; Claude runs the round and the debrief.

## The protocol — one task, about 25 minutes
The main idea: **requirements are kept in comments, not in the head, and checked against the code before «done».**

| Minutes | What I do | Sign that it is going well |
| --- | --- | --- |
| 0–2 | Repeat the task in one sentence and say what one row of the result is | «So for each developer I return one row: …» |
| 2–5 | Schema: ask about the tables, `SELECT * … LIMIT 5`, columns → questions | questions written per column |
| 5–8 | Questions **in one batch**, each with my assumption | answers written as a comment |
| 8–10 | Plan aloud: 2–4 steps | CTEs or functions named |
| 10–18 | Code, run after each step | **writing code by minute 10** |
| 18–22 | Check against the comments, then test | every comment line found in the code |
| 22–25 | Index / complexity / production | one or two sentences |

No code by minute 10 — stop asking: «Let me start with these assumptions and adjust later.»

### Questions come from two places
- **Without the schema, right after repeating:** domain questions — test purchases, trials, refunds, which stores, «Anything I should know about data quality — duplicates, test data, missing values?»
- **From the columns:** «Could you walk me through the tables and how they connect?», then `SELECT * FROM <main table> LIMIT 5`. A flag `is_…` → include or exclude? A category → `GROUP BY` it → which values count? A time that can be NULL → what does NULL mean? Two similar amounts → which one? Several dates → which one puts a row into the period? An event or payment ID → can the same one arrive twice?
- Always settle: what «today» is (a fixed date or `now()`); every limiting word in the task (enrolled, paid, active, last 30 days) → which column; filters; what one result row is and whether zeros and empty groups are included; ties and order; edge cases (negative, zero, empty, too many); who the result is for («Is this for finance or a product dashboard? It decides refunds and rounding.»).

### Answers go straight into a comment
```sql
-- RESULT: one row per enrolled developer: developer_id, headroom_usd
-- today = 2026-09-30; last 30 days = [today - 30 days, today)
-- filters: no sandbox; app_store + play_store; no refunds
-- one row per enrolled developer; zero if nothing; negative allowed
-- PLAN: 1) proceeds per developer  2) debt per developer  3) developers LEFT JOIN both
```
In Python the same as a docstring or comments at the top. Edge cases («no data → 0») go into the comment in the first minutes and are searched for in the output before «done».

## Thinking aloud — the phrases
- Repeat: «Let me repeat the task in my own words.» «So the result has one row per …, with columns …»
- Ask: «A few questions, with what I would assume.»
- Plan: «I will do it in three steps: first …, then …, and at the end …»
- Code: say what and why, not every keystroke: «I filter sandbox here, as we agreed.»
- Test: «Let me check the edge case with no purchases.»
- Discuss: «For production I would add an index on (developer_id, created_at).» «This is O(n log n) because of the sort.»
- Stuck: «I am stuck on the join. Let me write the simple version first.» «Can I ask for a small hint?» — asking is better than silence.
- Time: «I have about five minutes; I will finish the main case and mention the rest.»

## Setup
- Open the company's coding platform (CoderPad, HackerRank, a shared editor) and its sandbox on the first day of prep.
- Train in interview conditions: no AI hints in the editor — `vscode-no-ai-settings.json` in this folder turns them off in VS Code.

## Mock (for /mock live-coding)
- The candidate picks or Claude assigns a task on Live Coding Map (by the stage's language and domain), and starts the site's timer.
- Claude is a silent interviewer: answers only the questions asked, with plausible answers for the task; gives a hint only when asked; says the time at minutes 10, 18 and 22.
- At the end the candidate pastes the code and the site's check result.
- The debrief by the protocol, with timing: when coding started, which question was missing, which comment line is not in the code, which edge case failed, what was said about production. Repeating errors go to the prep document's «My errors»: as it was → as it should be → the English phrase.
