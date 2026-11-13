---
name: english-register
description: "Write or rewrite English application text in a confident non-native register at the candidate's level (C1 by default) instead of native-writer register. Use for cover letters, application form answers, LinkedIn notes, follow-ups and any English the candidate submits as their own words."
---

# English register for a non-native candidate

The candidate's English level and first language are in `me/profile.yaml` → `languages` (`english`, `native`). The targets below are for C1. For B2, aim for 10–13 words per sentence and under 11% long words; for C2, 13–17 words and under 15%. Written English must not be noticeably more sophisticated than their spoken English, or the gap shows in the first interview and raises a question nobody needed.

This is a register problem, not a simplification problem. Do not dumb the content down. Change how sentences are built, not what they say.

**Run this on every English text, every time, in full.** Run the script below and report its numbers before calling anything done. A count by eye is not a check: texts once went out at 16–17 words per sentence because the check was done by eye.

## Targets

| Metric | Target |
|---|---|
| Average sentence length | 12–15 words |
| Words of 8+ characters | under 13% (higher only when domain terms force it) |
| Longest sentence | under ~30 words |
| Contractions (`don't`, `I'm`) | zero |
| Native idioms | zero |

```python
import re
s=[x for x in re.split(r'(?<=[.!?])\s+', t.replace('\n',' ')) if len(x.split())>1]
w=re.findall(r"[A-Za-z][A-Za-z'\-]*", t); lw=[x for x in w if len(x)>=8]
print(len(w), len(s), round(len(w)/len(s),1), round(100*len(lw)/len(w),1))
```

Sentence boundaries are `.`, `!`, `?` only. A colon does not end a sentence. The same check with an idiom list is in `scripts/english_check.py` (`python3 "${CLAUDE_PLUGIN_ROOT:-kit}/scripts/english_check.py" file.txt`, or text on stdin).

## What reads as a native writer — strip on sight
- **Fragments without a verb** used for rhythm. Fold them into the previous sentence.
- **Appositive pile-ups.** Two plain sentences instead.
- **Stacked metaphors.** One figurative expression per answer at most.
- **Conversational openers:** `The short version:`, `Here's the thing`, `Look,`.
- **Idioms:** earn their keep, connective tissue, moved the needle, low-hanging, deep dive, at the end of the day, double down, north star, bandwidth, in the weeds, boil the ocean, tip of the iceberg, hit the ground running, wear many hats, that said, boils down to.
- **LLM-flavoured words:** delve, robust, seamless, holistic, synergy, testament to, underscore, pivotal, landscape, realm, crucial, furthermore, moreover, cornerstone, spearhead, leverage (verb), passionate, proven track record, genuinely.

## What to keep
One concrete, vivid line per answer earns its place: short, specific, only someone who did the work would write it. Do not sand it off in the name of simplicity.

## Structural rules for application text
- **Answer the question that was asked.** Read it twice; map each clause to a sentence. Count sub-questions.
- **Strongest aggregate claim first, then details** in a cold note: the widest true statement about experience, then one company, team or project. Inside an ATS thread (the reader has the CV open) — no aggregate, no CV recap.
- **Strengths first, caveats last.** Never open with what you lack.
- **No self-terminating offers** (`If that is a hard requirement, tell me and I will not take your time`).
- **No meta-commentary** (`The rest is in my CV`).
- **State a gap once, plainly, in one place**, and only on a must-have item — never on an «is a plus» item.
- **Do not recite the CV.** At most one or two numbers, each answering a requirement of the posting.
- **Write at the level of the role.** For EM / Head / Director: ownership and decisions (`I owned…`, `I keep architecture review with me`), not an engineer's task report — unless the posting asks for hands-on work or the question asks for personal experience.

## Content rules — fill in your own (do not relitigate once set)
- No questions in letters, notes and free-text answers — about money, currency, location, visa, remote work, or anything else. State the fact and stop: `I am based in <city> (UTC+N) and open to relocation.` Never end on a question.
- Stack paragraph: (1) your core; (2) the overlap with their list; (3) one line for a real gap on a must-have item only; (4) the principle (`service boundaries, asynchronous interaction, API contracts and observability do not depend on the language`); (5) a fact about leading teams on a stack that was new to you, if true.
- Claims never to make: the «never claim» table in me/never-say.md.
- Attribution: who built what. Never present a teammate's work as your own.

## Duplication
Repeating material across different companies is fine. Near-identical sentences between the letter and the form answers of the same company read as copy-paste: diff them and reword.

## When the candidate supplies the content
If they write the substance in their language and ask for a translation, translate faithfully: no added claims, no summarising conclusion they did not make, no upgraded phrasing. Flag anything that contradicts the CV, and any unanswered part of a multi-part question.

If the employer requires answers «in your own words», the candidate writes the English; you give structure and facts in their language and check the result.
