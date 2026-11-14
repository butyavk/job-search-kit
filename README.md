# Job search kit

[Русская версия](README.ru.md) · **Site:** [butyavk.github.io/job-search-kit](https://butyavk.github.io/job-search-kit/)

The whole job search with Claude, from «I want a new job» to the offer. Claude finds and ranks vacancies, finds the people to write to, builds every application, keeps the tracker and the follow-ups, checks your mail every morning, prepares you for each stage, runs mocks and debriefs. **Claude prepares; you send.**

It grew out of a real two-month search for engineering-manager roles: about a hundred applications, interviews up to final rounds, and the numbers behind every rule — the screener gate, the follow-up timing, the keyword coverage of a CV.

## The path — 9 commands

| Step | Command | What Claude does | What stays with you |
| --- | --- | --- | --- |
| 1. Start | `/start` | Builds your pack from your CV and a few interview sessions. Proposes roles, levels, countries, remote or relocation, and money floors from the market. Sets up the tracker and the schedule. | choose from the options, confirm facts |
| 2. Search | `/find` | Reads LinkedIn, company boards through ATS APIs, job sites (hiring.cafe, Himalayas, HN «Who is hiring», levels.fyi…) and country boards; checks each vacancy two ways, runs a five-point gate as a screener sees it, ranks the rest. A short list goes into the tracker. | choose where to apply |
| 3. People | `/people <company>` | Finds the hiring manager, the recruiter, people you know there, a referral path; drafts the notes. | send them |
| 4. Apply | `/apply <vacancy>` | The gate, a CV tailored with a keyword table, the letter, form answers; fills the form without submitting; plans the note and the follow-ups. | press «submit», say «applied» |
| 5. Every day | `/today` (and on a schedule) | Mail and LinkedIn into the tracker, new vacancies from alerts, follow-ups due with drafts, interviews this week. | send the drafts |
| 6. A stage | `/prep <company> <stage>` | Format and people, likely questions with answers from your blocks, a trainer for the format, a plan by days, and a one-page learning sheet: first sentences and story anchors. | learn it aloud |
| 7. Mock | `/mock <kind>` | A daily drill of the learning sheet with marks, or a full mock: recruiter, manager, behavioral, system design, live coding — by voice or text, with an honest debrief. | do the drill and the mock |
| 8. After a call | `/debrief` | What happened and the next step; new facts into your pack; reminders. | tell how it went |
| 9. Monthly | `/review` | Funnel, rejection analysis, what to change in the frame, the CV or the sources; a pack and fact check. | agree to the changes |

Everything else is plain words: «compose an answer to B03», «add a fact», «X rejected me», «I applied to Y».

**What runs by itself:** the daily check every morning (in the desktop app, a push only when there is something to do), a weekly search pass, a monthly review — as scheduled tasks in the Claude desktop app, or from cron in Claude Code (`schedules/`, with what each one can and cannot reach). Follow-up dates also go to your calendar from the tracker.

## Your data stays yours
Everything about you lives in a separate folder, the **pack** `me/`: facts with sources, answer blocks, recipes, what never to say, your profile and search frame. The kit reads it and writes to it only what you confirm. Work per company (`companies/<company>/`: prep, debriefs) and per application (`applications/<date>/`: CVs, form answers) sits next to it in your search folder. None of it goes into this repository (`.gitignore` blocks `me/`, `companies/` and `applications/`).

**Answer blocks** are the heart of the pack: small checked sentences — the whole story, the first line, context, your action, the result, the lesson — in English, plus your native language if it is not English. Any answer to any question for any company is a chain of them, so your facts stay the same in every interview. See `examples/example-story.md`.

## Autonomy
By default Claude asks before every outward action, and you do it: submit, send, accept, book. If you want Claude to send some kind of message itself — say, the first follow-up in an existing ATS thread, from the template — tell it the rule; it writes it into your profile with the date and your words. Rules work only in a live session that you start; scheduled runs never send anything. Passwords, accounts, money and offers are always yours.

## Install

**Claude Code (or the Claude desktop app with plugins):**
```
/plugin marketplace add butyavk/job-search-kit
/plugin install job-search-kit@job-search-kit
```
Then, in an empty folder for your search: `/start`. To update later: `claude plugin marketplace update job-search-kit`, then `claude plugin update job-search-kit@job-search-kit` (folder mode: `git pull` in `kit/`). The pack is never touched.

**As a folder** (any Claude with file access): clone it as `kit/` next to your future `me/`:
```
mkdir job-search && cd job-search
git clone https://github.com/butyavk/job-search-kit kit
echo '@kit/CLAUDE.md' >> CLAUDE.md
```
The one-line `CLAUDE.md` makes Claude Code load the kit's rules in every session started in `job-search/` (it does not read `kit/CLAUDE.md` on its own). In another client, start with «read kit/CLAUDE.md first». Then say «start my job search».

**claude.ai project:** turn on code execution, upload the skill zips and add the project files from the latest [release](https://github.com/butyavk/job-search-kit/releases/latest), and put `CLAUDE.md` into the project instructions. Commands become plain words; Claude gives you each pack file to add. Step by step: [docs/how-it-works.md](docs/how-it-works.md#claudeai).

**The tracker** is the open-source MCP server [tracker-mcp](https://github.com/butyavk/tracker-mcp); `/start` sets it up (`uvx tracker-mcp new …`, then one `claude mcp add` line, or the `.mcpb` file for the desktop app). Requires `uv` and tracker-mcp 0.8 or later.

## What to connect
The kit works with whatever your Claude has; each connection unlocks a part of the path.
| Connection | What it gives |
| --- | --- |
| Mail (Gmail connector) | replies, rejections and invitations into the tracker; follow-up drafts in the right thread |
| Calendar (Google Calendar connector) | interviews this week; free slots for a reply |
| Claude in Chrome | logged-in LinkedIn (alerts, search, People, messages), sites behind a login, and every application form — filled in your browser; submitted only when you name it and say so |
| The built-in browser (Claude desktop app) | job sites that block plain fetch (hiring.cafe, levels.fyi), the LinkedIn guest API |
| tracker-mcp | the tracker, follow-up dates, funnel, calendar export |
| A call recorder with transcripts (optional) | same-day debriefs from the transcript, where the company allows recording |
| Scheduled tasks | the daily check, the weekly pass, the monthly review |

Where vacancies come from — LinkedIn, company ATS boards, job sites, country boards — and how each one reads: [skills/job-search/sources.md](skills/job-search/sources.md).

## Companion projects
- [tracker-mcp](https://github.com/butyavk/tracker-mcp) — the tracker server: write with a preview, version checks, backups, undo; follow-ups, funnel, calendar export.
- [System Design Map](https://butyavk.github.io/system-design/) — system design theory and practice in English and Russian.
- [Live Coding Map](https://butyavk.github.io/live-coding/) — SQL and Python interview tasks with in-browser checking, mocks with a timer.
- [The laws of software teams](https://github.com/butyavk/laws-of-software-teams) — 20 short episodes on the laws behind team work (Brooks, Conway, Goodhart…), good material for manager answers.

## What is inside
```
.claude-plugin/   plugin and marketplace manifests
CLAUDE.md         the rules for Claude (folder mode); the same in skills/job-search-kit
commands/         the 9 commands
hooks/            a session-start reminder in a search folder (plugin)
skills/           13 skills: job-search-kit (entry), onboarding, answer-blocks, job-search,
                  outreach, tracker, tailoring-cv, english-register, job-application-forms,
                  interview-prep, system-design, live-coding, company-trainer
schedules/        prompts for the daily, weekly and monthly scheduled tasks
bank/             the universal question bank: 134 questions, 26 core, role packs, 13 story archetypes
pack-template/    an empty pack to copy as me/
templates/        prep context, recruiter call, debrief, story split, design card, references, …
scripts/          check_pack.py (pack check), english_check.py (English register and never-say),
                  check_kit.py (the kit's own consistency)
tests/            regression tests on two made-up packs
tools/            Apple Notes export (a source for the fact check)
examples/         one made-up story cut into blocks
docs/             how it works, in English and Russian
site/             the GitHub Pages site (Astro Starlight), built from docs/ and the sources list
```

## Preparing for an interview
The cycle for every stage: `/prep` → learn the one-page sheet → a daily `/mock drill` → a full mock two days before → the interview → `/debrief` the same day. Step by step: [the site](https://butyavk.github.io/job-search-kit/prep/).

## How it works
[docs/how-it-works.md](docs/how-it-works.md) — the search, the gate and its numbers, applications, follow-ups, interview prep, answer blocks, and what did not work.

## Contributing
Issues and pull requests are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Changes are listed in [CHANGELOG.md](CHANGELOG.md); privacy and reporting in [SECURITY.md](SECURITY.md).

## License
MIT.
