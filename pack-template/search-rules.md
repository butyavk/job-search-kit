# Search frame and working rules — <name>, updated <date>

The single source of truth for the search. Read it first in every session about vacancies. When the frame changes, edit this file in the same turn: date, decision, my words. Do not delete old decisions; mark them «outdated since <date>».

## Who I am looking for
- Roles and levels: (for example Engineering Manager, Senior EM, Head of Engineering)
- Preferences that do not filter: (company stage, domain, size)
- What I do not take: (pure IC roles, outsourcing, …)

## Channels, in priority order
| Channel | What it means for me | Priority |
| --- | --- | --- |
| Remote | (which countries and time zones accept me) | |
| Home country | | |
| Visa-free countries | | |
| Sponsorship | (where it is realistic) | |
| Relocation | (where I would move) | |

## Hard filters — only these
1. A must-have I cannot honestly meet (language, certificate, citizenship, experience I do not have). Quote it in full.
2. Geography: (where I can work, where I would move, where a visa is needed and how real it is).
3. Money: below the floor for that level or channel. The numbers live in one place, `profile.yaml` → `money` (`floor`, `say_aloud`, `form_numeric_field`); never copy them here.

Free-text salary field: «…». I never ask about money or currency myself.

## Gate before applying (0 / 1 / 2 as the screener sees it)
Level · stack · domain · geography · money. A zero — no cold application (a route through a person, or a conscious application marked in the tracker). Exceptions I decided not to count as zero: …

## Ranking weights
(for example: remote counts double; a route through a person +2)

## Facts for forms
Contacts, start date, work authorization, employment form and the standing form answers live in `profile.yaml` (one place). Here only what is wording:
- Experience wording: «…» (years, level, team sizes as I say them).
- «Why this company» frame: «…».

## Message rules
- First sentence of a cold note: «…».
- Stack paragraph: core → overlap with their list → one honest gap, only on a must-have → principle.
- Never write: (see `never-say.md`).
- No questions in letters and notes.

## Timing and follow-ups
These are defaults — ask the candidate whether to keep them; unconfirmed ones stay marked «default».
- (default) Apply within 24 hours of the package being ready; Monday to Thursday, Tuesday best; the company's morning (6–10 a.m. their time). Fresh posts first; age is not a filter (skill `job-search`, sections 3 and 7).
- Follow-ups: the dates come from the tracker's config (`[followups]` in `<tracker>.tracker-mcp.toml`; defaults: +10 days, then +14, «No answer» 30 days later). Change them there, not here.
- (default) One application per company in 3–4 weeks.

## Sources and technique
| Source | How it reads | Status | Notes |
| --- | --- | --- | --- |
| LinkedIn alerts | logged-in browser; guest API | | |
| Company boards | ATS APIs (Ashby, Greenhouse, Lever …) | | |
| | | | |

## Where things are
- Tracker: … (changes only through its MCP server)
- Master CV and its build: …
- Application texts: `applications/<date>/FORM-ANSWERS.md`
- Ready CVs: …

## Active processes
(one line per company in process, with a link to its prep document)
