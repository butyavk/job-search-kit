---
description: Start a job search — build the candidate pack, agree the search frame, set up the tracker and the schedule
argument-hint: "[CV, LinkedIn link, or anything you already have]"
---
Material from the candidate: $ARGUMENTS

Follow the `onboarding` skill from the step that is not done yet. If a pack already exists, run `python3 "${CLAUDE_PLUGIN_ROOT:-kit}/scripts/check_pack.py"`, say in three lines what is there, and continue from the first gap — never start over.

The order: pack (facts, the story set, blocks for the core questions) → search frame (`me/search-rules.md`: roles and levels, where and how they can work, money, what to skip — Claude proposes options from the candidate's experience and the market, the candidate picks) → tracker (skill `tracker`, setup section) → schedule (`schedules/README.md`: daily check, weekly search, monthly review, or calendar reminders where scheduled tasks are not available) → autonomy (explain the default «Claude prepares, you send» in two lines; write a rule only if the candidate asks).

End with what is ready, what is next (usually `/find`), and the few things only the candidate can do.
