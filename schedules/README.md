# Schedules

Three prompts run the search without the candidate starting them. Each is a complete instruction: paste it into a scheduled task, or run it by hand with the matching command.

| Prompt | When | Same as |
| --- | --- | --- |
| `daily.md` | every morning, before the candidate's working day | `/today` |
| `weekly.md` | once a week | `/find` over everything outside the daily alerts |
| `monthly.md` | once a month, or after every 30–50 applications | `/review` |

## Where to schedule
- **Claude app (web, desktop, Cowork): Scheduled tasks.** `/start` creates them when the session has a scheduling tool. Turn on push notifications for the daily task: it notifies only when there is something to do.
- **Where it runs matters:** the task must run on the computer that holds the pack and the tracker (a local scheduled task in the Claude desktop app, or cron). A cloud task cannot see local files or a local tracker server; with the pack in a claude.ai project it reads the project copy and plans tracker changes as a table.
- **Claude Code with cron:** fill the prompt once into the pack's `me/schedules/` folder, then `cd <search folder> && claude -p "$(cat me/schedules/daily.md)" --allowedTools "Read,Write,Glob,Grep,mcp__tracker__list_applications,mcp__tracker__get_application,mcp__tracker__followups_due,mcp__tracker__match_emails,mcp__tracker__set_status,mcp__tracker__mark_applied"` (plugin mode: add `--plugin-dir` only if the plugin is not installed). Writes stay dry runs by the rule below.
- **No scheduler:** run `/today` in the morning. Follow-up dates still reach you: the tracker exports them to a calendar file (`tracker-mcp calendar`, or ask Claude «export follow-ups to my calendar»); interviews are in the calendar from the invitations.

## Rules for every scheduled run
- Read and prepare only. Nothing is sent, submitted, accepted, booked or published, whatever `autonomy` rules say: those work only in a live session.
- The tracker: dry runs only, never `confirm` — the changes are listed in the summary and written in the next live session after the candidate's yes. Anything unclear becomes a question in the summary.
- LinkedIn is not silent: opening a message thread marks it read for the sender, and opening a profile can show «viewed your profile». Scheduled runs read only the inbox list, notifications and job alerts; threads and profiles are opened in a live session.
- Forms are never touched by a scheduled run.
- A run that finds nothing says so in one line.
- Fill the `<…>` placeholders once, when the task is created: name, roles, city, time zone, language — and keep the filled copies in `me/schedules/`.

## Pause or end
- **«Pause my search»** (a holiday, a busy month): disable the three tasks (or comment out the cron lines); follow-ups due in the pause move with `reschedule_followup`; say when it resumes.
- **«I found a job» or «I stop searching»:** withdrawals to the open processes (drafts; the candidate sends), thanks to references, the tracker closed out (`set_statuses` «Withdrawn»), the tasks deleted, a retro (`templates/retro.md`). The pack stays: the next search starts from it.
