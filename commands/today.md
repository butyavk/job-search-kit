---
description: The daily check — mail and LinkedIn into the tracker, new vacancies, follow-ups due with drafts, interviews this week
argument-hint: "[nothing, or 'quick']"
---
Run the kit's daily prompt in this session, filled with the pack's values: `python3 <kit>/scripts/schedule_prompt.py daily --me <pack>` prints it (`values.yaml` not filled yet: fill `schedules/daily.md`'s `<…>` from the profile), with the candidate's words if they added any ($ARGUMENTS; empty when typed as plain words). In a live session it uses the read-write `tracker`: writes after the candidate's yes. The same text runs as the morning scheduled task.

Read only and prepare: nothing is sent, submitted or accepted. Clear facts go to the tracker through its MCP server: a dry run, then the write after the candidate's yes in this session (a scheduled run stops at the dry run); anything unclear goes into the summary as a question. A live response from a company (a call, a slot, a take-home, an offer) gets its own prep session (`/prep`), not a paragraph here.

Without the tracker's MCP server: list the changes as a table (row or company → field → was → now, the columns of `templates/tracker.csv`) for the candidate to make by hand, and take follow-ups from the spreadsheet's dates.

End with one message in the candidate's language (each employer draft in its own quote block, in the vacancy's language): what came in, what changed in the tracker (row → was → now), new vacancies (at most 7 rows), what to send today (company → person → channel → text), interviews in the next 7 days. Nothing new — one line.
