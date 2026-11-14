---
name: tailoring-cv
description: "Tailor the candidate's master CV to a specific vacancy and build the matching PDF and cover letter, with a keyword coverage pass. Use for CV, resume, or cover letter requests tied to a job application. Preserve confirmed facts; change only selection, order, emphasis and wording where the posting's word is true."
---

# Tailoring the CV to a vacancy

## Output
The vacancy-specific CV source and its PDF; a cover letter only when the form has a field for it or the candidate asks; the keyword coverage table. No research report, no alternate design. Never submit.

## Source of truth
1. The CV source the candidate named.
2. Otherwise the master CV (`paths.master_cv` in `me/profile.yaml`): facts, formal history, structure. No master yet, or the path does not open: stop and set it up first (skill `onboarding`, «The master CV»); never build a CV from the pack's blocks alone.
3. The vacancy text — for relevance only, never as evidence about the candidate.

Keep a reserve in the master (variant bullets, variant skill lines, `FACT:` and `ASK:` comments under the document) so every variant is built by **selection and order**, and a wording change is made once in the master. A small generator (spec per vacancy → build → PDF) pays off from the tenth application on.

## What tailoring is — the whole list
1. The positioning line under the name.
2. Bullet selection and order inside each position: what answers the posting goes first; drop the 2–4 irrelevant ones.
3. The order of Skills categories.
4. Bold emphasis, sparingly.
5. A company descriptor, only to make it relevant without inventing a domain.

Everything else — facts, titles, dates, contacts, numbers — stays canonical.

### The positioning line
- Fits on one line (count rendered characters). Three broad capability areas, occasionally four.
- No self-assessment (`Hands-On`, `Senior`, `Proven`, `Passionate`, `Results-Driven`).
- No words lifted from the vacancy; no specific technology or vendor; never claim what the letter disclaims; do not restate the vacancy title.

### Length
Two pages for a senior candidate; the second page at least half full. Recount lines after any structural change.

### Level
A Head / Director CV does not carry squad-level lines (one integration, a feature counter). Exception: postings that ask for hands-on work (`hands-on`, `player-coach`, `write / review code`) — then include hands-on lines from the reserve.

## Keywords and screening — every build
ATS search, recruiter search and AI ranking all match words. Handle this by coverage, never by stuffing. In one analysis of 48 applications, those that reached a human matched 62–80% of the posting's must-have terms in the posting's own words; the rest about 40%.

1. **Extract** must-have requirements and core responsibilities from the full posting (technologies, domains, practices, role words such as `Engineering Manager`, languages, location, employment model).
2. **Check verbatim presence** of each term in the tailored CV text (`pdftotext`), separately in Experience and Skills.
3. **Mark truth:** Y — true; P — adjacent, can be worded honestly; N — not true; ? — ask the candidate.
4. **Close Y and P gaps with the posting's own word** — in the master, once, after the candidate's yes, so every future build benefits.
5. **Leave N gaps honest.** An N on a must-have is a gate zero, not a wording problem.
6. **Target ≥80% verbatim coverage** of true must-have terms. Below that, do not report ready; propose master wording.
7. **Report the table:** term · Experience / Skills / absent · truth · action.

Market vocabulary often missing from engineering-leadership CVs (check each posting): Engineering Manager, hands-on, career development, 1:1s, remote / distributed team across time zones, roadmap, stakeholders, startup, revenue / business impact, developer experience, Agile / Scrum / retrospectives, DevOps / platform engineering, CI/CD, technical debt, SLO / SLA.

## Facts that must not change
Without the candidate's explicit confirmation never add or alter: employers, titles, dates, education, contacts, location; team sizes, metrics, money, percentages, periods, personal ownership; technologies, domains, language level, relocation status; causality between an action and a result. Adjacent experience stays adjacent. Keep the candidate's «never claim» list (`me/never-say.md`) and check every build against it. Watch attribution of shared numbers — mixing two stories' numbers is the kind of error an interviewer catches.

## Cover letters
- One page, visually matching the CV.
- Strengths first, caveats last; the posting's own words for what the candidate has.
- Do not repeat the CV or the form answers; at most one or two numbers.
- Never name a gap on a nice-to-have; never undersell a must-have the role is built on (if the honest answer is «not mine», the gate is zero).
- No questions at all; state location as a fact.
- No closing meta-line.
- Register and the check script — skill `english-register`.

## Building the PDF
Compile with the real engine of the master (LaTeX, or whatever the master uses); do not rebuild the CV in another layout system. A master in Markdown or plain text: build HTML from it with one fixed stylesheet kept next to the master and print it with headless Chromium; the same stylesheet every time. Letters can be HTML printed with headless Chromium; embed fonts as TrueType so ATS text extraction works (`pdffonts` shows `CID TrueType`).

## File naming
Build files per company (`Name_Surname__CV (Company).pdf`); the copy attached to a form gets a neutral name and neutral PDF metadata (skill `job-application-forms`). Identify a PDF the candidate sends by its positioning line, not its file name.

## Verification before «ready»
- diff the tailored source against the master and account for every factual change;
- `python3 <kit>/scripts/check_pack.py --cv <the tailored source or PDF>`: every number in it is in `me/facts.md`;
- compile; `pdfinfo` (page count), `pdffonts`, `pdftotext` (every rendered bullet exists verbatim in the master; no leftover markup);
- the positioning line renders on one line and contains no banned words or vacancy phrases;
- coverage table at ≥80% of true must-have terms;
- render pages to images and look: clipping, overlap, broken glyphs, orphan headings, empty space;
- remove build artefacts from the destination.
