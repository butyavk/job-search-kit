# Filled schedule prompts

`tracker-ro.mcp.json` is the read-only tracker for Claude Code scheduled runs: put the absolute paths to `uvx` (`which uvx`; cron has no PATH) and to the tracker in it; the version range keeps the read-only server from changing under it. `/start` copies the kit's `schedules/daily.md`, `weekly.md` and `monthly.md` here with your name, roles, city, time zone and language filled in. The scheduled tasks (or cron) run these copies. After a kit update, compare them with the kit's versions: new rules come from there.
