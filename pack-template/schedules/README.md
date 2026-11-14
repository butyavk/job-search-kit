# Scheduled runs: what they take from the pack

- `values.yaml` — your name, roles, city, time zone and language. A run's prompt is always the kit's (`schedules/daily.md`, `weekly.md`, `monthly.md`), filled with these values when it starts (`scripts/schedule_prompt.py`), so a kit update reaches the runs by itself and an edited file in the pack cannot change what they do.
- `tracker-ro.mcp.json` — the read-only tracker for Claude Code scheduled runs: put the absolute paths to `uvx` (`which uvx`; cron has no PATH) and to the tracker in it; the version range keeps the read-only server from changing under it.

`python3 <kit>/scripts/check_pack.py --me me --schedules` checks both before every run.
