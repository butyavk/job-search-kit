---
description: The monthly review — funnel, rejections and silence, what to change in the frame, CV or sources; a pack and fact check
argument-hint: "[funnel | rejections | pack | facts] (empty = all)"
---
Scope: $ARGUMENTS

1. Funnel and reply times from the tracker (`funnel`, `reply_times`, `stale_applications`); also `funnel` by the Source and Gate columns where they exist — do applications with a gate zero get replies at all? With fewer than about 20 applications in a group, say the numbers are too few to change a rule on. Close silent rows by the rule (dry run, then the candidate's yes).
2. Rejections and silence: `templates/rejection-analysis.md` — real fit against fit as the screener saw it, knockouts in the gate, keyword coverage of the CV. Propose changes to `me/search-rules.md`, the master CV or the sources, each with the evidence; change them only after the candidate agrees, with the date.
3. The pack: `python3 <kit>/scripts/check_pack.py --cv <master CV>` (format, links, register, gaps, and the CV's numbers against `me/facts.md`).
4. Facts: an independent check of every block against every source in `fact_sources` of `me/profile.yaml` — by a separate agent where the session can start one, so the work does not grade itself (skill `answer-blocks`, section «Fact check»).
