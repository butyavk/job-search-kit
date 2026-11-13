# Schedules

Three prompts run the search without the candidate starting them. Each is a complete instruction: paste it into a scheduled task, or run it by hand with the matching command.

| Prompt | When | Same as |
| --- | --- | --- |
| `daily.md` | every morning, before the candidate's working day | `/today` |
| `weekly.md` | once a week | `/find` over everything outside the daily alerts |
| `monthly.md` | once a month, or after every 30–50 applications | `/review` |

## Where to schedule
- **Claude app (web, desktop, Cowork): Scheduled tasks.** `/start` creates them when the session has a scheduling tool. Turn on push notifications for the daily task: it notifies only when there is something to do.
- **Claude Code:** a cloud routine, or your own cron with `claude -p "$(cat kit/schedules/daily.md)"` in the folder that holds `kit/` and `me/`.
- **No scheduler:** run `/today` in the morning. Follow-up dates still reach you: the tracker exports them to a calendar file (`tracker-mcp calendar`, or ask Claude «export follow-ups to my calendar»); interviews are in the calendar from the invitations.

## Rules for every scheduled run
- Read and prepare only. Nothing is sent, submitted, accepted, booked or published, whatever `autonomy` rules say: those work only in a live session.
- Tracker writes go through its MCP server, with a dry run first, and only for clear facts (a rejection email, an application confirmation). Anything unclear becomes a question in the summary.
- A run that finds nothing says so in one line.
- Fill the `<…>` placeholders once, when the task is created: name, roles, city, time zone, language.
