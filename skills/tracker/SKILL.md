---
name: tracker
description: Set up and keep the candidate's job-application tracker through the tracker-mcp server — install, statuses, applications, follow-up dates, the follow-up log, funnel and reply times, calendar export. Use in /start (setup), and whenever an application, a status, a follow-up or the funnel comes up.
---

# The tracker

The tracker is a spreadsheet (.xlsx, .csv or a Google Sheet) that the candidate owns. Claude changes it only through the open-source MCP server **tracker-mcp** (https://github.com/butyavk/tracker-mcp): every write shows the change first, checks the row version, keeps a backup and can be undone.

## 1. Setup (in `/start`)
0. **`uv` is needed** (`uvx`): `curl -LsSf https://astral.sh/uv/install.sh | sh` on macOS or Linux, or `brew install uv` — the candidate runs it.
1. Version: tracker-mcp 0.8.3 or later (`uvx tracker-mcp --version`; `uvx --refresh tracker-mcp` updates it).
2. **Existing tracker?** Ask where it is. `uvx tracker-mcp init <file or Google Sheets URL>` writes a config that maps its columns and statuses; show the mapping and fix it with the candidate.
3. **No tracker:** `mkdir -p ~/Documents && uvx tracker-mcp new ~/Documents/job-tracker.xlsx --lang <en|ru>` (other languages: `en`, then rename the statuses in its config) creates an empty one with its config (columns, a status list, a summary sheet, the follow-up rule). The candidate runs it, or Claude does where it has a shell on their computer.
4. **Connect the server:**
   - Claude Code: `claude mcp add tracker -e TRACKER_PATH="$HOME/Documents/job-tracker.xlsx" -- uvx tracker-mcp`
   - For Claude Code scheduled runs, a read-only server list of their own, `me/schedules/tracker-ro.mcp.json` (not a second `claude mcp add`, so everyday sessions see only `tracker`):
     ```json
     {"mcpServers": {"tracker-ro": {"command": "<absolute path to uvx: run `which uvx`>",
       "args": ["--from", "tracker-mcp>=0.8.3,<0.9", "tracker-mcp", "--read-only"],
       "env": {"TRACKER_PATH": "<absolute path to the tracker>"}}}}
     ```
     The read-only server previews and refuses every write. `schedules/README.md` runs it with `--strict-mcp-config`, so the read-write server is not loaded in that run.
   - Claude desktop app: the `.mcpb` file from the latest release of tracker-mcp — double-click, pick the tracker. Its setting «Confirm only in the app's dialog» (tracker-mcp 0.8.1) makes every write wait for the candidate's answer in the app; propose turning it on.
   - Other clients: the agent setup guide, https://raw.githubusercontent.com/butyavk/tracker-mcp/main/docs/agent-setup.md
   - macOS with the tracker in Documents, Desktop or Downloads: see the macOS section of the server's README.
5. **Check:** `check_tracker`, then `describe_tracker` — Claude says in two lines what it sees. If the tracker has no **Source** and **Gate** columns (section 5), propose adding them now (`add_column`, previewed): `/review` measures the search by them.
6. Write the path to `me/profile.yaml` → `paths.tracker`.

No MCP client at all (claude.ai web only): the candidate keeps the spreadsheet by hand, with the columns of `templates/tracker.csv` (the same as `tracker-mcp new` makes, plus Gate); Claude gives the exact row changes as a table. The rules the server would apply, done by hand:
- Status, one of: Not applied, Applied, Screening, Interview, Offer, Rejected, Withdrawn, No response, Closed (Furthest stage: Screening, Interview or Offer). These are the English names; a tracker made with `--lang ru` or renamed has its own, and `describe_tracker` maps them — use the tracker's names with the candidate.
- Follow-up date: Applied on + 10 days; after a follow-up is sent, + 14 days from the sending; a reply from the company clears it.
- No response: 30 days after the last touch with no follow-up due.
Where claude.ai can run code, Claude can also `pip install tracker-mcp` in its sandbox and make the file there (`tracker-mcp new job-tracker.xlsx`) for the candidate to download. Later, the desktop app's `.mcpb` can point at that same file (a .csv, or saved from Excel as .xlsx) — no terminal needed.

**Processes already under way** (onboarding step 1): one `add_applications` batch with a row per process (company, role, the date applied if known, status Screening or Interview, Next step with the next date), as a dry run; after the yes, `mark_applied(applied_on=<the real date>, followup_on=<the next contact date, or null when a stage is booked>)` for rows whose date is known, and `set_statuses` for the stages. A process with an interview booked gets no follow-up date: the interview is the next touch.

## 2. Writing
- Every write: read the row (`get_application` → version) → the change with `expected_version` as a dry run → show the preview → write after the candidate's yes (the server asks for this on every write). Batches (`add_applications`, `set_statuses`) always as a dry run first; write after the candidate's yes.
- Only clear facts: a rejection email, an application confirmation, a reply from a person. A guess is a question in the summary, not a write.
- A reply from the company (a screen booked, a next stage): the planned follow-up is moot — `reschedule_followup(on=<the next step's date>)`, or `on=null` to clear it, as its own previewed write right after the status.
- A wrong write: `recent_writes`, then `undo_last_write` — each call steps back one write, newest first; it stops if the file was edited by hand after that write.
- One writer at a time. The candidate may open and edit the file by hand, but not while a session is writing.

## 3. Habits
- After each event, one sentence from the candidate is enough: «applied to X via the site», «X rejected», «sent follow-up to X», «don't write to X before Friday». Claude finds the row, shows the change, writes after «yes».
- Applications: `mark_applied` (date, channel); the server sets the follow-up dates by the rule in its config.
- Follow-ups: `followups_due`, `log_followup` after sending, `reschedule_followup` for «not before …» notes.
- Silence: `stale_applications(days=…)` with the frame's «No response» days (default 30, counted from the last touch), then `close_stale` after a dry run and a yes. A row whose follow-up is still due is not silent yet: send the follow-up first.
- The picture: `funnel`, `reply_times` (by channel), `summary`.
- Mail: `match_emails` links messages to rows.

## 4. Reminders without a scheduler
`export_followups_calendar` (or `uvx tracker-mcp calendar --tracker <file>` in a shell) writes an .ics file with the open follow-ups (overdue ones on today); the candidate imports it into their calendar and re-imports after big changes. With a calendar connector, `calendar_events` gives the same events to add directly. Interviews are already in the calendar from the invitations.

## 5. Columns worth adding
`add_column` adds a column and extends dropdowns. Useful ones:
- **Source** — where the vacancy was found (a tracker made by `tracker-mcp new` has it as «Found via»: check `describe_tracker` before adding any column);
- **Geography — checked <date>** — what the posting really says about location and remote;
- **Money (published)** — the range from the posting;
- **Gate** — the five-point line, e.g. `L2 S2 D1 G0 M2`;
- **Route** — the person, if the entry is through someone;
- **Prepared** and **Folder** — where the CV, letter and form answers are;
- for the rejection analysis: **Main reason**, **Second factor**, **CV keyword coverage**, **Missing in words / real gap**.
