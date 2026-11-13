---
description: The monthly review — funnel, rejections and silence, what to change in the frame, CV or sources; a pack and fact check
argument-hint: "[funnel | rejections | pack | facts] (empty = all)"
---
Scope: $ARGUMENTS

1. Funnel and reply times from the tracker (`funnel`, `reply_times`, `stale_applications`); close silent rows by the rule (dry run, then the candidate's yes).
2. Rejections and silence: `templates/rejection-analysis.md` — real fit against fit as the screener saw it, knockouts in the gate, keyword coverage of the CV. Propose changes to `me/search-rules.md`, the master CV or the sources, each with the evidence; change them only after the candidate agrees, with the date.
3. The pack: `python3 "${CLAUDE_PLUGIN_ROOT:-kit}/scripts/check_pack.py"` (format, links, register, gaps).
4. Facts: an independent check of every block against every source in `fact_sources` of `me/profile.yaml` — by a separate agent where the session can start one, so the work does not grade itself (skill `answer-blocks`, section «Fact check»).
