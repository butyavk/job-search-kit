#!/usr/bin/env python3
"""Print a scheduled run's prompt: the kit's schedules/<name>.md with its <…> values filled in.

Usage: python3 <kit>/scripts/schedule_prompt.py daily|weekly|monthly [--me <pack>]

The values come from <pack>/schedules/values.yaml (name, roles, city, time zone, language);
<kit> is this kit's own folder. Placeholders that a run fills itself (<date>, <company>,
<stage>, <the date it came>) stay as they are. The prompt text is always the kit's: a scheduled
run never reads a prompt file from the pack, so nobody can change what it does by editing one.

Each value names something, in a short phrase: letters of any script, digits, spaces and
, . ( ) ' & / + - only (and : in the time zone), a word limit per key, no sentences and no words
that tell a run what to do (send, submit, always, then…); a name has no digits, a time zone is
one the system knows (or UTC+H, UTC+H:MM); a key set twice or a file that is a link is refused.
A value that does not fit stops the run (exit 1) and says why.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KIT / "scripts"))
from check_pack import LANG_CODES, find_pack as _find_pack, friendly_errors  # noqa: E402
LANG_NAMES = set(LANG_CODES)
KEYS = {"name": 6, "roles": 8, "city": 6, "time zone": 4, "language": 4}   # key -> most words
RUN_TIME = {"<date>", "<company>", "<stage>", "<the date it came>"}
ABBREV = {"st", "mt", "ft", "ste", "sr", "jr", "dr", "mr", "mrs", "ms", "sta", "san"}   # «St. Petersburg»
# A value names something. Allowed: words that start with a capital (Head of Engineering, Sendai),
# the small linking words names and titles use, digits, and scripts without capitals (हिन्दी, 東京).
# A word in lower case outside that list — «forward mail», «do not ask» — is how an order reads.
LINKS = {"of", "and", "for", "the", "a", "an", "in", "on", "at", "to", "de", "da", "do", "das", "dos", "di", "du",
         "del", "della", "la", "le", "les", "el", "al", "van", "von", "der", "den", "ter", "y", "e", "i", "und",
         "et", "bin", "ibn", "binti", "dei", "degli", "zu", "af", "av", "og", "och", "or", "with", "&"}
# and words that still read as orders with a capital, unless they are part of a known title
ORDERS = re.compile(r"\b(?:send(?:s|ing)?|submit(?:s|ted|ting)?|apply|applying|repl(?:y|ies|ying)|respond(?:s|ing)?|"
                    r"accept(?:s|ing)?|approve[sd]?|pay(?:s|ing)?|delete[sd]?|deleting|remove[sd]?|removing|"
                    r"ignor(?:e|es|ing)|disregard|forget|skip|always|never|must|should|execute|run|fetch(?:es|ing)?|"
                    r"click(?:s|ing)?|install(?:s|ing)?|upload|post|push|sign|wire|transfer|forward|email(?:ing)?|"
                    r"mail|share|book|bcc|confirm(?:s|ed|ing|ation)?|don't|please|instead|override|instructions?|prompt|rules?|then)\b", re.I)
TITLES = re.compile(r"\b(?:Forward Deployed|Email Marketing|Prompt Engineer\w*|Open Source|Rules Engine|"
                    r"Post[- ]?Sales|Push Notifications?|Sign[- ]?Up|Run Team|Share ?Point)\b", re.I)


def script_ok(v: str) -> bool:
    """No invisible characters, no combining mark on a Latin letter (NFC composes the real ones),
    and one alphabet per word: «ѕubmit» with a Cyrillic ѕ is not a word that names anything."""
    import unicodedata
    prev = ""
    for ch in v:
        cat = unicodedata.category(ch)
        if cat in ("Cf", "Co", "Cn", "Cs", "Cc"):
            return False
        if cat.startswith("M") and prev.isascii() and prev.isalpha():
            return False
        prev = ch
    for word in re.findall(r"[^\W\d_]+", v):
        scripts = {unicodedata.name(ch, "?").split()[0] for ch in word if ch.isalpha()}
        if len(scripts) > 1:
            return False
    return True


def letters_ok(v: str, extra: str) -> bool:
    """Letters of any script (with their combining marks, as in Devanagari), digits and a few signs."""
    import unicodedata
    return all(ch.isalnum() or ch in extra or unicodedata.category(ch).startswith("M") for ch in v)


def find_pack(argv: list[str]) -> Path:
    explicit = None
    if "--me" in argv:
        i = argv.index("--me")
        if i + 1 >= len(argv):
            sys.exit("--me needs the pack folder")
        explicit = argv[i + 1]
    return _find_pack(explicit, KIT, "profile.yaml") or sys.exit("no pack found: pass --me <path to me/>")


def zone_ok(v: str) -> bool:
    m = re.fullmatch(r"(?:UTC|GMT)(?:([+-])(\d{1,2})(?::(\d{2}))?)?", v)
    if m:
        minutes = int(m.group(2) or 0) * 60 + int(m.group(3) or 0)   # real offsets run from −12:00 to +14:00
        limit = 14 * 60 if m.group(1) != "-" else 12 * 60
        return not m.group(2) or (minutes <= limit and (m.group(3) or "00") in ("00", "15", "30", "45"))
    try:
        import zoneinfo
        zones = zoneinfo.available_timezones()
    except Exception:   # no zone data on this system: fall back to the shape of a zone name
        zones = set()
    if zones:
        return v in zones
    return re.fullmatch(r"[A-Z][A-Za-z]+(?:/[A-Z][A-Za-z_+-]+){1,2}", v) is not None


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
        m = re.match(r"^([a-z ]+):\s*(.*?)\s*(?:\s#.*)?$", line)   # «C# Developer» keeps its #
        if not m or m.group(1) not in KEYS:
            sys.exit(f"{path.name}:{n}: only {', '.join(KEYS)} go here, one per line")
        if m.group(1) in values:
            sys.exit(f"{path.name}:{n}: «{m.group(1)}» is set twice; keep one line")
        raw = m.group(2).strip()
        q = re.fullmatch(r"'((?:[^']|'')*)'|\"((?:[^\"\\]|\\.)*)\"", raw)   # YAML quotes: '' is one '
        raw = (q.group(1).replace("''", "'") if q.group(1) is not None else q.group(2)) if q else raw
        # NFKC: full-width and other compatibility forms read as the letters they look like
        values[m.group(1)] = unicodedata.normalize("NFKC", raw)
    for key, most in KEYS.items():
        v = values.get(key, "")
        if not v or v.startswith("<"):
            sys.exit(f"{path.name}: «{key}» is not filled")
        if not letters_ok(v, " ,.()'&/+-_#—–’" + (":" if key == "time zone" else "")) or len(v) > 120:
            sys.exit(f"{path.name}: «{key}» may hold only letters, digits, spaces and , . ( ) ' & / + - # "
                     f"(at most 120 characters)")
        if len(v.split()) > most:
            sys.exit(f"{path.name}: «{key}» is a short phrase, at most {most} words")
        # an initial (Ivan S. Rykov) or a short abbreviation (St., Eng., Dipl.-Ing.) is not the end of a sentence
        sentence = "!" in v or "?" in v or any(
            len(m.group(1)) > 4 and m.group(1).lower() not in ABBREV for m in re.finditer(r"(\w+)\.\s+\w", v))
        if ("_" in v and key != "time zone") or sentence:
            sys.exit(f"{path.name}: «{key}» is a phrase, not sentences or code names")
        if not script_ok(v):
            sys.exit(f"{path.name}: «{key}» mixes alphabets in one word, or holds invisible or stray marks")
        lower = [w for w in re.findall(r"[^\W\d_][\w'’-]*", v) if w[0].islower() and w.lower() not in LINKS]
        if lower and key != "language":
            sys.exit(f"{path.name}: «{key}» names something: «{lower[0]}» in lower case reads as an order "
                     "(write names and titles with capitals)")
        if key == "language" and any(w.lower() not in LANG_NAMES and not w[0].isupper() for w in lower):
            sys.exit(f"{path.name}: «language» must be language names")
        if ORDERS.search(TITLES.sub(" ", v)):
            sys.exit(f"{path.name}: «{key}» names something; «{ORDERS.search(TITLES.sub(' ', v)).group(0)}» "
                     "tells a run what to do")
        if key == "name" and not all(letters_ok(w, "'’.-") and not any(c.isdigit() for c in w) for w in v.split()):
            sys.exit(f"{path.name}: «name» must be letters only (a name)")
        if key == "time zone" and not zone_ok(v):
            sys.exit(f"{path.name}: «time zone» must be an IANA zone such as Europe/Berlin, or UTC+4 / UTC+5:30")
        if key == "language" and not all(letters_ok(w, ",/-") and not any(c.isdigit() for c in w) for w in v.split()):
            sys.exit(f"{path.name}: «language» must be language names only")
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
    friendly_errors()
    sys.exit(main(sys.argv[1:]))
