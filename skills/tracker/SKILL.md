---
name: tracker
description: Set up and keep the candidate's job-application tracker through the tracker-mcp server — install, statuses, applications, follow-up dates, the follow-up log, funnel and reply times, calendar export. Use in /start (setup), and whenever an application, a status, a follow-up or the funnel comes up.
---

# The tracker

The tracker is a spreadsheet (.xlsx, .csv or a Google Sheet) that the candidate owns. Claude changes it only through the open-source MCP server **tracker-mcp** (https://github.com/butyavk/tracker-mcp): every write shows the change first, checks the row version, keeps a backup and can be undone.

## 1. Setup (in `/start`)
0. **`uv` is needed** (`uvx`): `curl -LsSf https://astral.sh/uv/install.sh | sh` on macOS or Linux, or `brew install uv` — the candidate runs it.
1. **Existing tracker?** Ask where it is. `uvx tracker-mcp init <file or Google Sheets URL>` writes a config that maps its columns and statuses; show the mapping and fix it with the candidate.
2. **No tracker:** `mkdir -p ~/Documents && uvx tracker-mcp new ~/Documents/job-tracker.xlsx --lang <en|ru>` creates an empty one with its config (columns, a status list, a summary sheet, the follow-up rule). The candidate runs it, or Claude does where it has a shell on their computer.
3. **Connect the server:**
   - Claude Code: `claude mcp add tracker -e TRACKER_PATH="$HOME/Documents/job-tracker.xlsx" -- uvx tracker-mcp`
   - Claude desktop app: the `.mcpb` file from the latest release of tracker-mcp — double-click, pick the tracker.
   - Other clients: the agent setup guide, https://raw.githubusercontent.com/butyavk/tracker-mcp/main/docs/agent-setup.md
   - macOS with the tracker in Documents, Desktop or Downloads: see the macOS section of the server's README.
4. **Check:** `check_tracker`, then `describe_tracker` — Claude says in two lines what it sees.
5. Write the path to `me/profile.yaml` → `paths.tracker`.

No MCP client at all (claude.ai web only): the candidate keeps the spreadsheet by hand; Claude gives the exact row changes as a table.

## 2. Writing
- Every write: read the row (`get_application` → version) → the change with `expected_version` as a dry run → show the preview → write after the candidate's yes (the server asks for this on every write). Batches (`add_applications`, `set_statuses`) always as a dry run first; write after the candidate's yes.
- Only clear facts: a rejection email, an application confirmation, a reply from a person. A guess is a question in the summary, not a write.
- A wrong write: `recent_writes`, then `undo_last_write`.
- One writer at a time. The candidate may open and edit the file by hand, but not while a session is writing.

## 3. Habits
- After each event, one sentence from the candidate is enough: «applied to X via the site», «X rejected», «sent follow-up to X», «don't write to X before Friday». Claude finds the row, shows the change, writes after «yes».
- Applications: `mark_applied` (date, channel); the server sets the follow-up dates by the rule in its config.
- Follow-ups: `followups_due`, `log_followup` after sending, `reschedule_followup` for «not before …» notes.
- Silence: `stale_applications(days=…)` with the frame's «No answer» days (default 30, counted from the last touch), then `close_stale` after a dry run and a yes. A row whose follow-up is still due is not silent yet: send the follow-up first.
- The picture: `funnel`, `reply_times` (by channel), `summary`.
- Mail: `match_emails` links messages to rows.

## 4. Reminders without a scheduler
`export_followups_calendar` (or `tracker-mcp calendar` in a shell) writes an .ics file with the open follow-ups (overdue ones on today); the candidate imports it into their calendar and re-imports after big changes. With a calendar connector, `calendar_events` gives the same events to add directly. Interviews are already in the calendar from the invitations.

## 5. Columns worth adding
`add_column` adds a column and extends dropdowns. Useful ones:
- **Source** — where the vacancy was found;
- **Geography — checked <date>** — what the posting really says about location and remote;
- **Money (published)** — the range from the posting;
- **Gate** — the five-point line, e.g. `L2 S2 D1 G0 M2`;
- **Route** — the person, if the entry is through someone;
- **Prepared** and **Folder** — where the CV, letter and form answers are;
- for the rejection analysis: **Main reason**, **Second factor**, **CV keyword coverage**, **Missing in words / real gap**.
