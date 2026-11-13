---
name: system-design
description: Train and run system-design interview rounds — the 6-step frame, questions before drawing, assumptions aloud, a design card per likely task with variants, mocks as the interviewer, an honest debrief; theory through the System Design Map site. Use when a stage includes system design or architecture, for /prep and /mock system-design.
---

# System design

Theory and practice live on the open site **System Design Map** — a reworked and updated edition of The System Design Primer, in English and Russian: https://butyavk.github.io/system-design/ (source: https://github.com/butyavk/system-design). Send the candidate there for any topic they need to learn; this skill is about the round itself.

## The frame — 6 steps, the same everywhere (one-page sheet, design card, mocks); minutes for a 60-minute round
1. **Scope — questions and assumptions** (0–5): 4–5 START questions (`questions.md`), the obvious said as an assumption, a one-sentence summary of what was heard.
2. **Contract — API and data** (5–12): the API or inputs, 2–3 main entities with keys (PK, UNIQUE, FK).
3. **Simple — a working skeleton** (12–25): it works at low load.
4. **Scale — numbers** (25–40): count the heaviest part first; what is added and on which signal.
5. **Failures** (40–50): what breaks, what we see, what we do.
6. **Wrap-up — the summary in a minute** (50–60): in English, with trade-offs; the rest is the interviewer's questions.

The candidate leads the first 15–20 minutes.

## Rules that paid off
- **Ask only what changes the design.** 4–5 questions at the start (START), the rest when you reach that part (LATER). The obvious is not asked but said as an assumption. Answers go on the board as text at once.
- **Count the heaviest part first**, then draw the scale.
- **Variants with an assumption removed.** For every likely task, 2–3 variants: «what if there are no notifications / no queue / no SDK / data arrives once a day». In a real round the task given was exactly the variant without the assumption. Train «how do we notice a change»: keep the previous state and compare.
- **If the company's stack is known** (Kafka in the posting) — use it and say why; do not ask «may I use Kafka».
- **Arrows:** calls and service flow solid, table reads and writes dashed; a frame around what is written in one transaction.
- Typical blocks and seven common designs: `patterns.md`.
- Diagrams, frames and the printed sheet come from one data source; otherwise every edit drifts across three files.

## Preparing for a company
1. Likely tasks from the company's product, reviews of their rounds and the interviewers' public work; each with a likelihood and its source.
2. A design card per likely task (`templates/sd-task-card.md`): START / assumptions / LATER; three frames (skeleton → scale → failures); tables with keys; failures and defences; the summary in a minute in English (`english-register`); bridges to the candidate's experience only from blocks, with IDs.
3. The one-page sheet: the frame, START questions, assumptions, the blocks list — rewritten by hand the day before.

## Mock (for /mock system-design)
- Claude is the interviewer: gives the task in one sentence, answers only what is asked (answers from the card's «expected answer», or a plausible one marked as an assumption), keeps time per step, gives no hints.
- At three checkpoints (after the questions, after the skeleton, at the end) the candidate pastes a screenshot of the drawing (Excalidraw or paper).
- At the end Claude asks one variant with an assumption removed.
- The debrief by the six steps, with timing: which questions changed nothing, which assumption was missing, where the scale was drawn before counting, what the summary lacked. Repeating errors go to the prep document's «My errors».
- At least 2–3 full mocks with a real person who picks the task.
