---
description: After a call or an interview — what happened, the next step, new facts into the pack, reminders
argument-hint: "<company> [stage] [notes, transcript or recording link]"
---
Call: $ARGUMENTS

Follow the `interview-prep` skill, section «Debrief», with `templates/debrief.md`. Then feed the pack: new facts → `me/facts.md` (ask about anything new or contradictory), answers that worked → block edits, answers that failed → what to say instead, speech errors → `me/voice.md`, new questions → the bank or the company's prep document. Update the tracker (status, next step, the date to expect an answer) and say when the follow-up is due. Run `python3 "${CLAUDE_PLUGIN_ROOT:-kit}/scripts/check_pack.py"`.
