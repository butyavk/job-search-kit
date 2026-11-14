# Tools

| File | What it does |
| --- | --- |
| `notes-export.applescript` | Exports Apple Notes (chosen folders, plus notes with chosen words from the rest) into one text file — a source for the fact check. Edit the three settings lines at the top, open it in Script Editor and press Run. The file holds other people's conversations too: keep it local, never upload it to a shared project or a repository. |

Scripts that Claude runs are in `scripts/`: `check_pack.py` (the pack check), `english_check.py` (the English register check), `schedule_prompt.py` (a scheduled run's prompt, filled with the pack's values) and `check_kit.py` (the kit's own consistency check).
