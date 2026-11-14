---
description: Build an application — check the vacancy, run the gate, tailor the CV, write the letter and form answers, fill the form without submitting, plan the note and follow-ups
argument-hint: "<vacancy link or text>"
---
Vacancy: $ARGUMENTS

1. `job-search`: check the vacancy two ways and run the gate. Report the gate first. A zero means no cold application: propose a route through a person (`/people`) or a conscious «apply anyway», marked in the tracker. Go on only if there is no zero or the candidate says go.
2. `tailoring-cv` (with the keyword coverage table), `english-register` (the script on every text), `job-application-forms` (fill the form, do not submit, end with the pre-submit table). Facts and wording only from `me/facts.md` and `me/blocks/`; nothing from `me/never-say.md`. All texts in one `FORM-ANSWERS.md`.
3. `outreach`: one short note to the hiring manager or recruiter for the day of applying.
4. When the candidate says «applied»: the tracker (`mark_applied`, channel, date; follow-up dates come from the tracker's rule) and the note's send time.

Without a browser: everything goes into `FORM-ANSWERS.md` in the order of the form's fields; the candidate pastes it. Before any submit: the «Never twice» check in `job-application-forms`.

Submitting the form and sending the note are the candidate's, unless the candidate says in this message to submit these ready items (`job-application-forms`, «Never submit on your own initiative»), or an `autonomy` rule covers it and the candidate starts it in this session.
