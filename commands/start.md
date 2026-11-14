---
description: Start a job search — build the candidate pack, agree the search frame, set up the tracker and the schedule
argument-hint: "[CV, LinkedIn link, or anything you already have]"
---
Material from the candidate: $ARGUMENTS

Folder mode: if the search folder (the one holding `kit/`) has no `CLAUDE.md` with the line `@kit/CLAUDE.md`, add that line first (at the top of an existing `CLAUDE.md`, never replacing it), so every later session loads the kit's rules.

Follow the `onboarding` skill from the step that is not done yet. If a pack already exists, run `python3 <kit>/scripts/check_pack.py`, say in three lines what is there, and continue from the first gap — never start over.

The order puts the search first, so the first session already yields vacancies:
An interview in three days or less changes the order: onboarding «If an interview is close», «Three days or less».

1. **Session 1:** the CV and a draft (onboarding steps 0–2) → profile, master CV and the search frame (step 4: Claude proposes roles, levels and channels from the market with links, the candidate picks) → tracker and schedule (step 5) → the first `/find`.
2. **Next sessions:** the stories (step 3), 2–3 per session, alongside applications; bans and voice (step 6); the check (step 7).
3. Autonomy: explain the default «Claude prepares, you send» in two lines; write a rule only if the candidate asks.

If the candidate has an interview within a week, follow the skill's section «If an interview is close» and go to `/prep` as soon as the stories for that stage are confirmed.

End with what is ready, what is next (usually `/find`), and the few things only the candidate can do.
