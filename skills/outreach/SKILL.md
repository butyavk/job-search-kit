---
name: outreach
description: Find the people to write to at a company (hiring manager, recruiter, former colleagues, a referral path) and draft notes, follow-ups and replies to employers. Use for /people, the note in /apply, follow-ups in /today, and any message the candidate will send to someone at a company.
---

# People and messages

A cold application gets a reply from a person about 9% of the time. A short note to the right person on the day of applying, or a referral, changes that more than any CV edit.

## 1. Who to look for
In this order, for one role:
1. **The hiring manager** — the person the role reports to. Clues: «reports to the Director of Platform» in the posting, the team name, the product area. Search LinkedIn for that title at the company; check that their area matches the team (a Director of Payments is not the manager of a Subscriptions EM). Open-source roles: the repository's `MAINTAINERS`, `CODEOWNERS`, recent release notes.
2. **The recruiter for the role** — «Talent Partner», «Technical Recruiter» at the company, in the right region; the name sometimes appears in the posting or the ATS confirmation email. LinkedIn: `linkedin.com/company/<slug>/people/?keywords=recruiter`, scroll and read the cards (promoted posts have no «hiring team» card — go through People).
3. **People the candidate knows there** — first-degree contacts, former colleagues (search by past companies in the pack), second-degree contacts with many mutual connections: a possible referral.
4. **Peers** — engineers or managers in the same team — only as a source of context, not a cold channel.

Opening a profile can show the person «viewed your profile»: research in a live session, and say so if the candidate prefers private browsing mode in LinkedIn settings.

For each person: name, title, since when, region, degree of connection, why they are relevant, source link. Do not guess who the hiring manager is: «not found with confidence» is an answer.

## 2. Who not to write to
- People in `me/never-say.md` → «People not to contact» (also for references, offer replies and withdrawals). Ask before writing to anyone the candidate has a history with.
- Possible future reports, and well-known public figures at the company, cold — no.
- **One team, one direction at a time.** Do not approach the same team from two sides on the same day. Write to the second person after the first replies or after a week.
- Nobody written to in the last 14 days, and anybody with a «do not follow up» note in the tracker's follow-up log.

## 3. Channels and limits
- LinkedIn connection note: **300 characters** at most, no links. Count them.
- InMail: limited credits — keep them for people with no free route.
- Email: when the address is public or came in a thread. Mail drafts without links (connectors may rewrite them).
- The ATS thread: for replies to the company after an application.

## 4. How to write
- **The first sentence of a cold note** is the candidate's strongest aggregate claim, from the pack (for example «nearly ten years in engineering leadership, more than six as a manager»). Then one fact that answers the role. Then the fact of applying («On 18 October I applied for …»).
- **A reply in an ATS thread**: 2–3 sentences, status and interest. No aggregate, no CV retelling.
- **No questions** in notes and letters: not about money, currency, location, visa or remote. State the fact: «I am based in <city> (UTC+N) and open to relocation». Questions about location twice led to a fast rejection.
- One or two numbers, only if they answer a requirement. A gap only once, only on a must-have.
- Do not repeat the first sentence word for word to the same person in a follow-up.
- Every text goes through `english-register` (the script, with its numbers in the reply). A text in another language (a German or Spanish note) follows that language's conventions: the formal address (Sie, usted) to a stranger, the salutation and closing the country expects («Sehr geehrte Frau …», «Mit freundlichen Grüßen»), gender-fair job titles as the posting writes them (Entwickler:in); the script then checks only never-say and the sentence length.

## 5. Follow-ups
The rule lives in the tracker's config (`[followups]`; default: follow-up 1 at application + 10 days, weekends → Monday; follow-up 2 at +14 more); silent applications are closed with `close_stale` (default 30 days) in `/review`. `followups_due` lists what is due. A follow-up names the role and the date of applying, adds one new relevant fact if there is one, and asks for nothing.

## 6. After sending
The candidate says it is sent (or Claude sent it under an `autonomy` rule in a live session): write it to the tracker with `log_followup` — who, channel, date — and the next touch date. Notes not yet sent stay as drafts with the date they are for.

## 7. Output
A table: person — title — why — channel — draft (with character count for LinkedIn) — when to send — status. Plus the people found but not to write to, with the reason, so the next session does not find them again.
