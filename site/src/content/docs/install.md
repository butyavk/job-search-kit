---
title: Install and connect
description: Install the kit in Claude Code, as a folder, or in a claude.ai project, and connect mail, calendar, browser and the tracker.
---

## Claude Code (or the Claude desktop app with plugins)
```
/plugin marketplace add butyavk/job-search-kit
/plugin install job-search-kit@job-search-kit
```
Then, in an empty folder for your search: `/start`.

## As a folder
Any Claude with file access: clone the kit as `kit/` next to your future `me/`.
```
mkdir job-search && cd job-search
git clone https://github.com/butyavk/job-search-kit kit
echo '@kit/CLAUDE.md' > CLAUDE.md
```
The one-line `CLAUDE.md` makes Claude Code load the kit's rules in every session started in `job-search/` (it does not read `kit/CLAUDE.md` on its own). In another client, start with «read kit/CLAUDE.md first». Then say «start my job search».

## A claude.ai project without a shell
- Skills: zip each folder in `skills/` and upload it in Settings → Skills.
- Project instructions: the text of `CLAUDE.md`.
- Project files: `commands/` (no slash commands there: Claude reads a command's file when you say it), `bank/questions.md`, `pack-template/`, `templates/`, `schedules/` — each named with its path and `__` (`commands__debrief.md`, `templates__debrief.md`: some names repeat across folders).
- Claude gives you each pack file to upload; commands become plain words.

## What to connect
Each connection unlocks a part of the path; the kit works with whatever your Claude has.

| Connection | What it gives |
| --- | --- |
| Mail (Gmail connector) | replies, rejections and invitations into the tracker; follow-up drafts in the right thread |
| Calendar (Google Calendar connector) | interviews this week; free slots for a reply |
| Claude in Chrome | logged-in LinkedIn (alerts, search, People, messages), sites behind a login, and every application form — filled in your browser, never submitted |
| The built-in browser (Claude desktop app) | job sites that block plain fetch (hiring.cafe, levels.fyi), the LinkedIn guest API |
| [tracker-mcp](https://github.com/butyavk/tracker-mcp) | the tracker, follow-up dates, funnel, calendar export (needs `uv`) |
| A call recorder with transcripts (optional) | same-day debriefs from the transcript, where the company allows recording |
| Scheduled tasks | the daily check, the weekly pass, the monthly review |

## Update
Plugin: `claude plugin marketplace update job-search-kit`, then `claude plugin update job-search-kit@job-search-kit`, and restart (or `/plugin` in the app → the marketplace → update). Folder: `git pull` in `kit/`. Your pack is separate and never touched by an update.
