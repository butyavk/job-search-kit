---
name: interview-prep
description: Prepare a candidate for an interview process at one company — format and people, topic weights, a day-by-day plan, answers from the pack, learning them, trainers, mocks, take-home tasks, the final round, references, the same-day debrief and the offer. Use for /prep, /mock and /debrief, when a company invites the candidate to any stage, sends a take-home or makes an offer.
---

# Interview preparation

The skill builds the whole preparation for one company: the role and the people, answers, system design, live coding, mocks, debriefs, the final round and references. It was tested on full processes up to the final round for manager roles.

Two inputs:
1. **The candidate's pack** — facts, blocks and recipes, bans, voice, past debriefs. Claude adds nothing beyond it.
2. **The vacancy and the company** — the posting, recruiter emails, the interview guide, public material about the company and the interviewers.

Templates are in `templates/`.

## Rules — always
- **The project is the shared memory.** The company's context file (`templates/context-file.md`) is read first in every session; a decision or result goes into the project in the same turn.
- **Facts only from the pack or the candidate's words.** No invented or rounded-up numbers, dates or authorship. No fitting story — «I do not have an exact example», never a made-up one.
- **Content decisions are the candidate's.** Claude proposes and asks; it fixes only obvious errors itself.
- **Status from mail and calendar.** Project documents always lag behind the mail.
- **Emails, bookings and applications are sent by the candidate** (router skill, «Autonomy»). Claude drafts.
- **A CV once sent does not change.** An inaccuracy in it goes into the rules, and in the interview the candidate says how it really was.
- **Recording calls and AI notes only if the company allows it.** Otherwise notes right after the call.
- **English in the register the candidate holds when speaking** (skill `english-register`, checked by the script, not by eye).
- **Contradictions in the pack are the candidate's to resolve.** Write both versions and ask; do not use the fact until they answer.
- **Chances only on request**, marked «my estimate from the transcript, not a forecast of the company's decision».
- **Be brief.** What does not change a decision is not written.

## One stage, one cycle
```
format and people → topic weights and plan → material and trainer → learn it → mocks and audits → interview → debrief the same day → next stage
```

### Step 0. Project and context file
- One project per company, or one folder: `companies/<company>/` next to `me/` (never inside the kit) with `context.md`, the prep document, `learning-sheet.md`, debriefs. The first document is the context file: role, money and terms from the posting, stages with dates, people, where things are, working rules.
- Read the pack first: `me/never-say.md`, then `me/facts.md` (open questions), then `me/recipes.md` and the blocks.
- No pack yet — `/start`. Stories in another form — cut them into blocks (`answer-blocks`). Remove bridges to a previous company from ready answers («At <old company> I would…»).
- CV: the version sent for this vacancy, saved and unchanged.
- Choose and warn references at the start, not at the end (`templates/references.md`).

### Step 1. Format and people
- Sources: the company's interview guide, recruiter emails, Glassdoor-type reviews, the values page, the engineering blog, vacancies of neighbouring teams.
- For each interviewer: role, team, what they do in public (posts, talks, public code). This gives likely topics and 1–2 questions for them at the end. Never mention their personal profiles aloud: it sounds like studying the person rather than the company.
- **The recruiter call** comes first almost everywhere: money and format, contract and country, timing and stages, rules on recording and AI, who the interviewers are. Recording or an AI notetaker on the candidate's side only where the company allows and the candidate agrees (`forms.recording_consent`); a notetaker that joins calls by itself is turned off for interviews unless both agree. Prep: `templates/recruiter-call.md`.
- **Unknown company or little public data** (anonymous posting, agency): work from the posting, mark every estimate «from the posting», turn cells without a source into questions for the recruiter. Do not invent the company.

### Step 2. Weights and plan
- Topics by likelihood (high / medium / low), each with the source of the estimate.
- A day-by-day plan with hours per day; unlikely topics go to «later»; mocks at the hour of the real interview; logistics as its own item (link, time zone, equipment, a quiet room, the platform's sandbox opened on day one).
- Two days before the interview the material is frozen: only run-throughs aloud.

### Step 3. The prep document
One document, a tab per topic (`templates/prep-doc-tabs.md`): recruiter, company and role, answer cheat sheet, English, behavioral and manager questions, values, system design, a one-page plan, metrics, «one sentence», final round and references. Answers come from the pack and are fitted to the company: another order, another emphasis, new bridges to this role. Facts do not change. Every answer keeps its block IDs.

Stories across rounds: `templates/story-split.md` — one row per round with its people; each round has its own main stories. Interviewers compare notes: one story must not be told in every round.

### Step 4. Learn: from the document to memory
The prep document is the reserve. What the candidate takes into the room is the **learning sheet** (`templates/learning-sheet.md`), built from the document in the same session:
- **Stories, not answers.** 5–7 stories cover almost every likely question. Each gets an anchor in four steps — the answer in one sentence → the situation → what I did → the number and the lesson — plus what not to say. The candidate learns the anchor, not the text: the words in the interview will differ, the facts will not.
- **A map on one page:** the 12–16 most likely questions → the first sentence, learned word for word → which story. Two questions for the interviewer, word for word. A likely question with no story in the pack is a gap for step 3 (compose with the candidate, `answer-blocks`), never a sheet row with words of Claude's own.
- **Recall, not rereading.** Read an anchor once, close it, tell it aloud. Rereading feels like knowing and does not hold under pressure.
- **Aloud, timed, shuffled.** 60–90 seconds an answer, a case up to 60; the questions in random order, as an interviewer asks them.
- **Repeat only the misses.** A mark per question in every drill: ✓ — the first sentence and all four steps, no prompt, in time; ~ — a pause, too long, or no number; ✗ — not recalled or off the point. ✗ comes back the same evening and the next morning; ✓ two days running leaves the drill.
- **A plan by days:** day 1 — read each anchor once and tell each story aloud twice; then a drill a day (`/mock drill`) with the marks in the sheet; a full mock at the hour of the interview two days before, and from then the material is frozen (step 2): only drills; the interview day — the map rewritten by hand from memory.
- **In the interview language.** A Russian interview — Russian drills; an English one — the anchors in English, with the errors from `me/voice.md` checked in every drill.

### Step 5. Trainers (by format)
- System design: skill `system-design`.
- Live coding in SQL or Python: skill `live-coding`.
- A coding screen on the company's domain or stack (TypeScript, Go, an API platform …): skill `company-trainer`.

### Step 6. Audits
Every couple of days an independent pass (a separate agent where possible): does it match the format, are numbers and examples right, do tabs contradict each other, is anything over-complicated or missing, is authorship of stories right. Every code example is run; the output is real.

### Step 7. The day before
Nothing new. Rewrite the one-page plan and the learning map by hand from memory. One short drill «the summary in a minute». 1–2 questions per interviewer for the end.

### Step 8. Final round
A founder, CTO or senior leader: 3 main questions and spares; 30–45-second answers to «tell me about yourself», «why us», risks, the first 90 days, plans. With a CTO — more on engineering strategy, quality, AI in teams. References: a memo with dates and facts and a request message; the answers are not a script (`templates/references.md`). After the decision — a retro of the process (`templates/retro.md`).

## Behavioral and manager answers
- **The first sentence answers the question.** Then one example: the situation in 1–2 sentences, what I did, the result with a number, the lesson. 60–90 seconds, then stop.
- **«The answer in a minute»** for the 20 most likely questions: a 4-part anchor + 110–135 words + «if they ask» (`templates/answer-card.md`), built from recipes.
- **Values.** Find what is really checked: the values page, leadership principles, the candidate guide, the engineering blog, reviews of the values round; ask the recruiter which values this round checks and who runs it. Not published — prepare the usual set: ownership, bias for action, customer focus, collaboration, candour / disagree and commit, learning, raising the bar, ambiguity. For each value: what it means at this company in their words → which story → the first line. Prepare the slipperiest one first (for example work-life balance).
- **No exact story** — «I do not have a perfect example, but the closest one is…».
- **Speak at the level of the role:** for manager roles, decisions and ownership rather than «I wrote it myself», unless the posting asks for hands-on.
- **Questions at the end** relate to that interviewer's work; with a founder, strategy and the company's finances are fine; money and contracts only with the recruiter (bank section Z).

## Mocks
- Claude plays the interviewer of that stage: answers only what is asked, keeps time, gives no hints unless asked, and at the end asks what an interviewer would ask.
- By voice: the voice mode of the Claude desktop or mobile app (Claude Code has none — there, a text mock, or the brief for an outside voice tool below). For system design: talk by voice, draw in Excalidraw, and at three checkpoints (after the questions, after the skeleton, at the end) paste a screenshot.
- Outside Claude (a voice-agent tool, a friend): write the brief from `templates/recruiter-mock-brief.md`; for pronunciation work, `templates/voice-coach-brief.md`.
- The debrief is by the points of the protocol, with timing, without smoothing. Repeating errors go to «My errors»: as it was → as it should be → the English phrase; speech errors and fillers to `me/voice.md`.
- At least 2–3 full system-design mocks with a real person, who picks the task.
- **Drill** (`/mock drill`): practice of the learning sheet, not an interview. Claude asks the map's questions in random order, one at a time, waits for the whole answer, compares it with the anchor and gives a mark with one line on what was missing (the first sentence, a step, the number) or «too long». ✗ come back at the end of the same drill. The marks go into the sheet's table; ✓ two days running leaves the drill. 15–25 minutes, by voice where possible. No sheet yet — build it first (step 4).

## Debrief
The same day, from the transcript or notes (`templates/debrief.md`): who the interviewer was, the flow by time, what worked, where the interviewer led and how the answer could be stronger, English, form. Then:
- new facts → `me/facts.md` (ask about anything new or contradictory), phrasings that worked → blocks, failed answers → what to say instead, new questions → the bank or the prep document;
- lessons go into the next stage's prep at once;
- the tracker: status, next step, when to expect an answer (skill `tracker`); the follow-up date if there is silence;
- a rating on the Strong yes / Yes / Lean yes / Lean no / No scale only on request (`templates/assessment.md`).

## A live response from a company
A person from the company invites to a call, asks for a slot, sends a take-home, invites to a stage or makes an offer → a separate prep session at once (`templates/live-response-session-prompt.md`): the role and company with sources, a draft reply, the slot from the calendar, the prep plan. The candidate sends the reply.

## Take-home task
- **Before starting:** the time box, what is evaluated, whether AI tools are allowed, the language and stack, how to submit, whether there is a review call. Anything unclear → questions for the recruiter (a draft; the candidate sends).
- **A plan by the time box:** the core that answers the task first, extras only after it works. Stop at the time box: going far over it reads as not managing scope.
- **The README is part of the answer:** assumptions, how to run, what was left out and why, what comes next with more time, where AI was used if it was allowed.
- **Everything runs:** tests, the example from the task, a clean checkout. The candidate understands every line and follows the company's rule on AI; Claude does not hand in work the candidate could not explain.
- **The candidate submits.** Then prepare the review call: a 5-minute walk-through, the trade-offs, «what would you change», likely follow-up changes done live. Debrief after it as usual.

## Offer
An offer is a live response: a separate session at once (above). Claude prepares; every reply, counter and acceptance is the candidate's. Template: `templates/offer.md`.
1. **Read it whole** into the context file: base and currency, contract form and country, bonus and its conditions, equity (type, number, vesting, cliff, strike, last valuation if known), start date, probation, notice, non-compete, IP and confidentiality, remote or relocation terms, the date of the first review. What is unclear → a list of questions for the recruiter.
2. **Compare** with `money.floor` and `money.say_aloud` in `me/profile.yaml`, with the other open processes in the tracker, and with what the frame says matters. The floor is never said to anyone.
3. **Never decide in the moment:** «Thank you — I need a day to look at the whole package.» A deadline shorter than 2–3 working days is worth asking to move.
4. **Counter with one number,** tied to the role and its scope, not to needs, without a range. If the base is capped: a review in N months against agreed metrics, with the number and the date in the offer; a signing bonus; equity. Non-cash parts come on top of the cash, not instead of it.
5. **Other processes:** companies at a final stage hear that there is an offer and its deadline (drafts; the candidate sends). Earlier stages — only if the candidate wants to speed them up.
6. **Before signing:** the contract against the offer, line by line; terms that limit future work (non-compete, IP on «ideas discussed», governing law) are flagged with a plain explanation. Claude is not a lawyer: for unusual terms, suggest one.
7. **After the decision:** accept or decline in the candidate's words (drafts); on acceptance — polite withdrawals from the other processes, thanks to references, the tracker closed out, the scheduled tasks paused (`schedules/README.md`), a retro (`templates/retro.md`).

## Checklist
Start: project and context file · guide, reviews, interviewers · weights and plan · references warned · recording rules.
Prep: story split · minute answers with a timer · first line for every value · the learning sheet and a drill a day with marks · trainers by format · 2–3 full mocks · an audit every couple of days.
Day before: nothing new · the one-page plan by hand · questions for the end.
After the call: debrief the same day · lessons into the next stage.
Offer: read it whole · compare with the floor and other processes · no decision in the moment · one number · contract against the offer · withdrawals, references, schedules, retro.
