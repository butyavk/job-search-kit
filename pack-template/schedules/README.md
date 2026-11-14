# Filled schedule prompts

`tracker-ro.mcp.json` is the read-only tracker for Claude Code scheduled runs: put the absolute path to the tracker in it. `/start` copies the kit's `schedules/daily.md`, `weekly.md` and `monthly.md` here with your name, roles, city, time zone and language filled in. The scheduled tasks (or cron) run these copies. After a kit update, compare them with the kit's versions: new rules come from there.
