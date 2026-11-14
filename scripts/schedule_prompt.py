#!/usr/bin/env python3
"""Print a scheduled run's prompt: the kit's schedules/<name>.md with its <…> values filled in.

Usage: python3 <kit>/scripts/schedule_prompt.py daily|weekly|monthly [--me <pack>]

The values come from <pack>/schedules/values.yaml (name, roles, city, time zone, language);
<kit> is this kit's own folder. Placeholders that a run fills itself (<date>, <company>,
<stage>, <the date it came>) stay as they are. The prompt text is always the kit's: a scheduled
run never reads a prompt file from the pack, so nobody can change what it does by editing one.

Each value is a short phrase: letters, digits, spaces and , . ( ) ' & / + - only, and a word
limit per key. A value that does not fit stops the run (exit 1) and says why.
"""
from __future__ import annotations

import os
import re
import sys
import unicodedata
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
KEYS = {"name": 6, "roles": 8, "city": 6, "time zone": 4, "language": 4}   # key -> most words
FORMAT = {   # what each value may look like, beyond the shared character set
    "name": (re.compile(r"[^\W\d_]+(?:[ '.-][^\W\d_]+)*\.?"), "letters only (a name)"),
    "time zone": (re.compile(r"[A-Z][A-Za-z]+(?:/[A-Z][A-Za-z_+-]+){1,2}|UTC|GMT|UTC[+-]\d{1,2}(?::\d{2})?"),
                  "an IANA zone such as Europe/Berlin, or UTC+4"),
    "language": (re.compile(r"[^\W\d_]+(?:[ ,/-]+[^\W\d_]+){0,3}"), "language names only"),
}
RUN_TIME = {"<date>", "<company>", "<stage>", "<the date it came>"}
ALLOWED = re.compile(r"[\w ,.()'&/+\-]+")


def find_pack(argv: list[str]) -> Path:
    if "--me" in argv:
        i = argv.index("--me")
        if i + 1 >= len(argv):
            sys.exit("--me needs the pack folder")
        return Path(argv[i + 1]).expanduser()
    env = os.environ.get("JOB_SEARCH_ME")
    for c in ([Path(env).expanduser()] if env else []) + [KIT.parent / "me", Path.cwd() / "me"]:
        if (c / "profile.yaml").exists():
            return c
    sys.exit("no pack found: pass --me <path to me/>")


def read_values(path: Path) -> dict[str, str]:
    if path.is_symlink() or path.parent.is_symlink():
        sys.exit(f"{path} is a link: a scheduled run reads only a real file in the pack")
    if not path.exists():
        sys.exit(f"{path} is missing: write name, roles, city, time zone and language there (see the kit's "
                 "pack-template/schedules/values.yaml)")
    values: dict[str, str] = {}
    for n, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([a-z ]+):\s*(.*?)\s*(?:#.*)?$", line)
        if not m or m.group(1) not in KEYS:
            sys.exit(f"{path.name}:{n}: only {', '.join(KEYS)} go here, one per line")
        if m.group(1) in values:
            sys.exit(f"{path.name}:{n}: «{m.group(1)}» is set twice; keep one line")
        values[m.group(1)] = unicodedata.normalize("NFC", m.group(2).strip().strip("\"'"))
    for key, most in KEYS.items():
        v = values.get(key, "")
        if not v or v.startswith("<"):
            sys.exit(f"{path.name}: «{key}» is not filled")
        if not ALLOWED.fullmatch(v) or len(v) > 120:
            sys.exit(f"{path.name}: «{key}» may hold only letters, digits, spaces and , . ( ) ' & / + - "
                     f"(at most 120 characters)")
        if len(v.split()) > most:
            sys.exit(f"{path.name}: «{key}» is a short phrase, at most {most} words")
        if ("_" in v and key != "time zone") or re.search(r"\w{4,}[.!?]\s+\w", v):
            sys.exit(f"{path.name}: «{key}» is a phrase, not sentences or code names")
        if key in FORMAT and not FORMAT[key][0].fullmatch(v):
            sys.exit(f"{path.name}: «{key}» must be {FORMAT[key][1]}")
    return values


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in ("daily", "weekly", "monthly"):
        sys.exit(__doc__)
    me = find_pack(argv)
    values = read_values(me / "schedules" / "values.yaml")
    text = (KIT / "schedules" / f"{argv[0]}.md").read_text(encoding="utf-8-sig")

    def fill(m: re.Match) -> str:
        slot = m.group(0)
        if slot in RUN_TIME:
            return slot
        if slot == "<kit>":
            return str(KIT)
        key = slot[1:-1]
        if key not in values:
            sys.exit(f"the kit's {argv[0]}.md has {slot}, which values.yaml does not fill")
        return values[key]

    sys.stdout.write(re.sub(r"<[^<>\n]{1,80}>", fill, text))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
