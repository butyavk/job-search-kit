#!/usr/bin/env python3
"""Check a candidate pack against the kit.

Usage:
    python3 kit/scripts/check_pack.py [--me PATH] [--kit PATH] [--strict] [--ready] [--cv CV] [--mark-synced]
    python3 kit/scripts/check_pack.py --me PATH --schedules   (only what a scheduled run trusts; before every run)

The pack is --me, else $JOB_SEARCH_ME, else ../me next to the kit folder, else ./me. The script reads
me/blocks/*.md, me/recipes.md, me/never-say.md and kit/bank/questions.md, and
reports:

  errors   duplicate block IDs, recipes that point to missing blocks or questions,
           blocks without EN text or without the native-language line (any `- XX:`
           two-letter code, required unless languages.native is English),
           unknown block types;
  warnings English that breaks the C1 register (contractions, a sentence over 30
           words, more than 13% long words), phrases from never-say.md (the
           filler list and the «never claim» table) found in either line of a
           block (and with --cv in the CV), blocks that cannot stand alone (start with "Then",
           "That", "Потом", "Это"...), confirmed blocks with <placeholders>;
  coverage bank questions with no recipe yet (core ★ first, then role ◆ for the
           candidate's track from profile.yaml); a recipe that uses a block
           marked `draft` counts as a draft, not as covered;
           stories (topics with an R block, or an O and an L block) that have no whole `S` block.

Exit code 1 if there are errors (or warnings with --strict).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

TYPES = {"S", "O", "C", "A", "R", "D", "L", "P", "G", "Q"}
BLOCK_RE = re.compile(r"^#### ([A-Z][A-Z0-9]*-[A-Z0-9]+[a-z]?) · (.+)$")
TYPE_RE = re.compile(r"`([A-Z])`")
SPAN_RE = re.compile(r"`([^`]+)`")
ID_RE = re.compile(r"\b([A-Z][A-Z0-9]*-[A-Z0-9]*\d[A-Z0-9]*[a-z]?|[A-Z][A-Z0-9]*-[A-Z])\b")


class _Refs:
    """IDs inside any code span, including chains like `A-O1 → A-R1`."""

    @staticmethod
    def findall(text: str) -> list[str]:
        out = []
        for span in SPAN_RE.findall(text):
            if len(span) == 1:  # a type marker such as `A`
                continue
            out.extend(ID_RE.findall(span))
        return out


REF_RE = _Refs()
QROW_RE = re.compile(r"^\| ([A-Z]\d{2})(?: ([★◆]))? \|")
CONTRACTION_RE = re.compile(
    r"\b(\w+n't|I'm|I've|I'd|I'll|you're|we're|they're|it's|that's|there's|what's|let's|we've|they've|we'll|you'll)\b",
    re.IGNORECASE,
)
DANGLING_EN = re.compile(
    r"^(Then|So|That|This|These|Those|It|Also|Later|And|But|Plus|After that|Since then|There|He|She|They|Here|Instead|Because)\b")
NEED_L2 = True  # set from profile.yaml in main()
DANGLING_RU = re.compile(r"^(Потом|Это |Так |Плюс|Тоже|Также|И |Но |Там |Он |Она |Они |Поэтому|После этого|Здесь|Вместо|Ещё |Дальше"
                         r"|Luego|Entonces|Después|Eso |Esto |También|Pero |Además"
                         r"|Dann |Danach|Das |Dies |Aber |Und |Auch |Außerdem|Deshalb|Daher )")   # RU, ES, DE openers
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*")


def parse_blocks(blocks_dir: Path):
    blocks: dict[str, dict] = {}
    errors: list[str] = []
    for path in sorted(blocks_dir.glob("*.md")):
        current = None
        for n, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            m = BLOCK_RE.match(line)
            if m:
                bid = m.group(1)
                if bid in blocks:
                    errors.append(f"{path.name}:{n}: duplicate block ID {bid} (first in {blocks[bid]['file']})")
                current = {"id": bid, "title": m.group(2), "file": path.name, "line": n,
                           "types": [], "en": "", "ru": "", "notes": [], "draft": False}
                blocks[bid] = current
                continue
            if line.startswith("###") and not m:
                errors.append(f"{path.name}:{n}: a heading that is not a block — a block starts with «#### ID · Title»")
                current = None
                continue
            if current is None:
                continue
            if line.startswith("## ") or line.startswith("# "):
                current = None
                continue
            if not current["types"] and line.startswith("`"):
                if re.search(r"\bdraft\b|черновик", line):
                    current["draft"] = True
                for part in line.split(" · "):
                    m_t = re.fullmatch(r"`([A-Z])`", part.strip())
                    if not m_t:
                        break
                    current["types"].append(m_t.group(1))
            elif line.startswith("- EN:"):
                current["en"] = line[5:].strip()
            elif re.match(r"^- (?!EN:)[A-Z]{2}:", line):
                current["ru"] = line[5:].strip()  # the native-language line, whatever its code
                current["l2code"] = line[2:4]
            elif line.startswith("- ⚠"):
                current["notes"].append(line)
    for b in blocks.values():
        where = f"{b['file']}:{b['line']} {b['id']}"
        if not b["types"]:
            errors.append(f"{where}: no type")
        bad = [t for t in b["types"] if t not in TYPES]
        if bad:
            errors.append(f"{where}: unknown type {bad}")
        if not b["en"]:
            errors.append(f"{where}: no EN text")
        if not b["ru"] and NEED_L2:
            errors.append(f"{where}: no native-language line (- XX:)")
    return blocks, errors


AUDIENCE: dict[str, str] = {}


def parse_questions(bank: Path):
    questions: dict[str, str] = {}
    for line in bank.read_text(encoding="utf-8-sig").splitlines():
        m = QROW_RE.match(line)
        if m:
            questions[m.group(1)] = m.group(2) or ""
            AUDIENCE[m.group(1)] = line.rstrip(" |").rsplit("|", 1)[-1].strip()
    return questions


DUP_RECIPES: list[str] = []


def parse_recipes(recipes: Path):
    rows: dict[str, list[str]] = {}
    empty: list[str] = []
    if not recipes.exists():
        return rows, empty
    for line in recipes.read_text(encoding="utf-8-sig").splitlines():
        m = re.match(r"^\| ([A-Z]\d{2}) \|(.*)$", line)
        if not m:
            continue
        cells = m.group(2).split("|")
        # first phrase, short chain, long chain; the notes column is free text
        refs = REF_RE.findall("|".join(cells[:3]))
        if m.group(1) in rows:
            DUP_RECIPES.append(m.group(1))
        rows[m.group(1)] = refs
        if not refs:
            empty.append(m.group(1))
    # Z questions map to ASK blocks as a group
    return rows, empty


def never_say_phrases(path: Path) -> list[str]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8-sig")
    m = re.search(r"## (?:Фразы-паразиты|Filler words)[^\n]*\n+(.+?)(\n## |\Z)", text, re.S)
    if not m:
        return []
    phrases = []
    lines = m.group(1).splitlines()
    bullets = [re.sub(r"^\s*[-*]\s+", "", l) for l in lines if re.match(r"\s*[-*]\s+", l)]
    items = bullets if bullets else m.group(1).replace("\n", " ").split(" · ")
    for item in items:
        item = item.strip()
        if not item or "(" in item:  # qualified items need a human: skip
            continue
        phrases.append(item)
    return phrases


def never_claims(path: Path) -> list[tuple[str, set]]:
    """English phrases from the «Never claim» table, with the blocks
    named in the row (those blocks are where the claim is handled, so skip them)."""
    if not path.exists():
        return []
    m = re.search(r"## (?:Утверждения|Never claim)[^\n]*\n(.+?)(\n## |\Z)", path.read_text(encoding="utf-8-sig"), re.S)
    if not m:
        return []
    out = []
    rows = m.group(1).splitlines()
    for i, line in enumerate(rows):
        if not line.startswith("|") or re.match(r"\|\s*:?-{3,}", line):
            continue
        if i + 1 < len(rows) and re.match(r"\|\s*:?-{3,}", rows[i + 1]):
            continue   # the table's header row
        cells = [c.strip() for c in line.strip("|").split("|")]
        allowed = set(REF_RE.findall(line))
        # markdown is how the row looks, not what a block says: **bold**, `code`, [text](link)
        claim = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", cells[0])
        claim = re.sub(r"\*\*|__|`", "", claim).strip()
        quoted = re.findall(r"«([^»]+)»|\"([^\"]+)\"", claim)   # «a» or «b»: the quoted parts
        if quoted:
            parts = [x or y for x, y in quoted]
        else:
            # «Adyen; PSD2; fraud, underwriting» lists single words that are claims: each is checked.
            # A false ban here is only a warning; a word left out would be a claim never checked.
            parts = [p.strip() for p in re.split(r"[;/]|, | or ", claim)]
        for part in parts:
            part = part.strip().strip("«»\"' ")
            # a short title (CTO, VP, PhD) only when it is quoted or the whole claim
            short_ok = re.fullmatch(r"[A-Z]{2,4}|PhD", part) and (quoted or part == claim.strip("«»\"' "))
            if (len(part) < 4 and not short_ok) or "<" in part or (not quoted and re.search(r"[А-Яа-яЁё]", part)):
                continue  # placeholders and Russian descriptions need a human; their English terms are still checked
            out.append((part, allowed))
    return out


def yaml_scalars(text: str) -> tuple[dict[str, str], list[str]]:
    """The profile's scalar values by their dotted path (`languages.native`), read the way a YAML
    reader takes them: by indentation, not by the first matching line anywhere. Also the keys set
    twice under one parent, which a reader would silently take the last of."""
    values: dict[str, str] = {}
    dups: list[str] = []
    stack: list[tuple[int, str]] = []          # (indent, key) of the open mappings
    seen: dict[str, set[str]] = {}
    item = 0
    block_from = None                          # inside a | or > block scalar: lines deeper than this
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        ind = len(raw) - len(raw.lstrip())
        if block_from is not None:
            if ind > block_from:
                continue
            block_from = None
        line = raw.strip()
        if line.startswith("- ") or line == "-":   # a list item opens a fresh mapping
            item += 1
            while stack and stack[-1][0] >= ind:
                stack.pop()
            stack.append((ind, f"[{item}]"))
            line = line[1:].strip()
            ind += 2
            if not line:
                continue
        m = re.match(r"""(?:"([^"]+)"|'([^']+)'|([^\s:#][^:#]*?))\s*:(?:\s+|$)(.*)$""", line)
        if not m:
            continue
        key = (m.group(1) or m.group(2) or m.group(3)).strip()
        while stack and stack[-1][0] >= ind:
            stack.pop()
        parent = ".".join(k for _, k in stack)
        if key in seen.setdefault(parent, set()):
            dups.append(f"{parent}.{key}" if parent else key)
        seen[parent].add(key)
        rest = m.group(4)
        q = re.match(r"""\s*(?:"((?:[^"\\]|\\.)*)"|'((?:[^']|'')*)')""", rest)
        if q:   # a quoted value ends at its closing quote; a comment may follow
            val = q.group(1) if q.group(1) is not None else q.group(2).replace("''", "'")
            val = "'" + val + "'"   # kept quoted here, unquoted below
        else:
            val = re.split(r"\s+#", rest, maxsplit=1)[0]
        val = val.strip()
        path = f"{parent}.{key}" if parent else key
        if val[:1] in ("|", ">"):
            block_from = ind
            values[path] = ""
        elif val:
            values[path] = val[1:-1] if q else val
        stack.append((ind, key))
    return values, dups


def profile_syntax_errors(text: str) -> list[str]:
    """YAML the kit's readers do not follow, refused so that what the checks read is what a YAML
    reader reads: quoted keys, a space before the colon, anchors, aliases and merge keys, and flow
    mappings ({…}) — the profile is written one key per line."""
    out = []
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.split(" #")[0] if not raw.lstrip().startswith("#") else ""
        body = re.sub(r"^\s*-\s+", "", line)
        if re.match(r"""\s*["'][^"']*["']\s*:""", body):
            out.append(f"profile.yaml:{n}: a quoted key; write keys bare (`autonomy:`, not `\"autonomy\":`)")
        elif re.match(r"\s*[\w.-]+[ \t]+:(?:\s|$)", body):
            out.append(f"profile.yaml:{n}: a space before the colon; write `key: value`")
        if re.search(r"""(?:^|:\s|-\s)\s*[&*][\w-]+\s*$|^\s*<<\s*:""", body):
            out.append(f"profile.yaml:{n}: anchors, aliases and merge keys (&x, *x, <<) are not used in a profile")
        if re.search(r""":\s*\{""", body):
            out.append(f"profile.yaml:{n}: a {{…}} mapping; write one key per line")
    return out


def native_is_english(value: str) -> bool:
    """English, English (UK), British English, en, en-GB, en_US — not «Russian, English» or a placeholder."""
    v = value.strip().strip("\"'").lower()
    return bool(v and not v.startswith("<") and re.match(
        r"^(?:(?:british|american|australian|canadian|irish|us|uk)\s+)?english\b(?!\s*(?:,|and|\+|/))"
        r"|^en(?:[-_][a-z]{2})?$", v))


def find_pack(explicit: str | Path | None, kit: Path, need: str | None = None) -> Path | None:
    """The pack every script uses, in one order: --me; else JOB_SEARCH_ME (and only it: a wrong value
    stops the script instead of quietly checking another pack); else me/ next to the kit, then
    me/ in the working folder. `need` is the file the script reads (none: any folder)."""
    def ok(c: Path) -> bool:
        return (c / need).exists() if need else c.is_dir()
    if explicit:
        return Path(explicit).expanduser()
    env = os.environ.get("JOB_SEARCH_ME")
    if env:
        c = Path(env).expanduser()
        if ok(c):
            return c
        sys.exit(f"JOB_SEARCH_ME={env} is not a pack (no {need or 'folder'} there): fix it, unset it, or pass --me")
    return next((c for c in (kit.parent / "me", Path.cwd() / "me") if ok(c)), None)


def fold(text: str) -> str:
    """The form both a phrase and the text it is looked for in are compared in: composed Unicode
    (NFC), no invisible format characters (zero-width, bidi, soft hyphen)."""
    import unicodedata
    text = unicodedata.normalize("NFC", text)
    return "".join(ch for ch in text if unicodedata.category(ch) != "Cf")


def phrase_pattern(phrase: str) -> re.Pattern:
    """A never-say or never-claim phrase as the text may write it: any spaces between the words,
    straight or curly apostrophes on either side, any case. Search `fold(text)` with it.
    check_pack and english_check share it."""
    words = [re.escape(w.replace("\u2019", "'")).replace("'", "['\u2019]") for w in fold(phrase).split()]
    return re.compile(r"(?<!\w)" + r"\s+".join(words) + r"(?!\w)", re.IGNORECASE)


LANG_CODES = {"russian": "RU", "ukrainian": "UK", "belarusian": "BE", "german": "DE", "spanish": "ES",
              "french": "FR", "italian": "IT", "portuguese": "PT", "polish": "PL", "dutch": "NL",
              "turkish": "TR", "georgian": "KA", "armenian": "HY", "kazakh": "KK", "serbian": "SR",
              "chinese": "ZH", "japanese": "JA", "korean": "KO", "hebrew": "HE", "arabic": "AR", "hindi": "HI",
              "bengali": "BN", "tamil": "TA", "telugu": "TE", "marathi": "MR", "gujarati": "GU", "kannada": "KN",
              "malayalam": "ML", "punjabi": "PA", "urdu": "UR",
              "русский": "RU", "украинский": "UK", "español": "ES", "espanol": "ES", "deutsch": "DE",
              "français": "FR", "francais": "FR", "português": "PT", "portugues": "PT", "italiano": "IT",
              "polski": "PL", "türkçe": "TR", "nederlands": "NL"}

# thousands: 450 000 · 450,000 · 65.000 (not «3 100-person»: a group glued to a word is its own number)
NUM_RE = re.compile(r"(?<![\w.,])(\d{1,2}(?:,\d{2})+,\d{3}(?![\d\w-]|[,.]\d)|\d{1,3}(?:[ \u00a0,.]\d{3})+(?![\d\w-]|[,.]\d)|\d+(?:[.,]\d+)?)(\s?%)?")


def norm_number(raw: str, pct: str | None) -> str:
    if re.fullmatch(r"\d{1,2}(?:,\d{2})+,\d{3}", raw):   # 48,00,000 — Indian grouping
        n = raw.replace(",", "")
    elif re.fullmatch(r"\d{1,3}(?:[ \u00a0,.]\d{3})+", raw):  # 450 000 · 450,000 · 65.000 — thousands
        n = re.sub(r"[ \u00a0,.]", "", raw)
    else:
        n = raw.replace(",", ".")  # 2,1 — a decimal comma
    return n + ("%" if pct else "")


def fact_numbers(path: Path) -> set[str]:
    """Numbers stated as facts: table cells after the ID and before the source and confirmation columns."""
    if not path.exists():
        return set()
    out = set()
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.startswith("| F-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        for cell in cells[1:-2] if len(cells) > 3 else cells[1:]:
            out |= {norm_number(m.group(1), m.group(2)) for m in NUM_RE.finditer(cell)}
            out |= {norm_number(m.group(1), m.group(2)) for m in NUM_RE.finditer(SCALED_RE.sub(_scaled, cell))}
            for m in SUFFIX_RE.finditer(cell):   # €1M, 10K, 2 млн → the whole number too
                v = float(m.group(1).replace(",", ".")) * SUFFIX[m.group(2)]
                out.add(str(int(v)) if v == int(v) else str(v))
    return out


MONTHS = (r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:t(?:ember)?)?"
          r"|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b\.?")
NOT_AMOUNTS = re.compile(
    r"`[^`]*`"                                             # code spans
    r"|\b[A-Z]{1,6}-[A-Z]?\d+\b"                           # block and fact IDs: PAY-S1, F-99
    r"|\+\d[\d\s().-]{6,}\d"                               # phone numbers
    r"|\b\d{1,2}[/.]\d{4}\b|\b\d{4}-\d{2}(?:-\d{2})?\b"    # 11/2026, 2026-11-14
    r"|\b\d{1,2}(?:st|nd|rd|th)?\s+" + MONTHS + r"|\b" + MONTHS + r"\s+\d{1,2}\b"   # 15 March, March 15
    r"|\b(?:ISO|IEC|SOC|PCI(?: DSS)?|HTTP|TLS|IPv|ES|RFC|WCAG|OAuth)\s?/?\d[\d.]*"   # standards: ISO 27001, HTTP/2
    # a version: one or two digits, or a dotted number; never one followed by %, a scale or more digits
    r"|\b(?:v|Python|Java|Go|Node(?:\.js)?|PHP|Ruby|Scala|Kotlin|Swift|C\+\+|\.NET|Postgre(?:s|SQL)|MySQL|Terraform"
    r"|Rust|TypeScript|Spark|Windows|iOS|Android|React|Angular|Vue|Next\.js|Spring|Rails|Django|Ubuntu|Debian|k8s"
    r"|Kubernetes|Java ?SE|Swift ?UI|Kafka|Elasticsearch|Redis|Spring ?Boot|C#|macOS|log4j|Laravel|Symfony|Unity"
    r"|Xcode|Gradle|Hadoop|Flink|Cassandra|MongoDB)\s?/?(?:\d+\.\d+(?:\.\d+)*|\d{1,2})(?!\d|[.,]\d|\s?(?:%|[kKM]\b|x\b"
    r"|million|thousand|billion|percent))"
    r"|\b\d+/\d+\b"                                          # ratios and rules: 80/20, 24/7
    r"|\b\d+(?:st|nd|rd|th)\b|\b\d+(?:signals|FA|D)\b"         # ordinals and names: 3rd, 37signals, 2FA, 3D
    r"|\bUTC[+-]\d{1,2}(?::\d{2})?|\b\d{1,2}:\d{2}\b")         # time zones and clock times: UTC+5:30, 10:30
SCALED_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*(million|billion|thousand|M|K|k|bn|Mio|Mrd|Tsd|Millionen|Milliarden|"
                       r"lakh|lakhs|crore|crores|LPA|млн|тыс|млрд)\b\.?(?!-)")
SCALE_OF = {"million": 1_000_000, "billion": 1_000_000_000, "thousand": 1_000, "M": 1_000_000, "K": 1_000,
            "k": 1_000, "bn": 1_000_000_000, "Mio": 1_000_000, "Millionen": 1_000_000, "Mrd": 1_000_000_000,
            "Milliarden": 1_000_000_000, "Tsd": 1_000, "lakh": 100_000, "lakhs": 100_000, "LPA": 100_000,
            "crore": 10_000_000, "crores": 10_000_000, "млн": 1_000_000, "тыс": 1_000, "млрд": 1_000_000_000}


def _scaled(m: re.Match) -> str:
    v = float(m.group(1).replace(",", ".")) * SCALE_OF[m.group(2)]
    return str(int(v)) if v == int(v) else str(v)


def block_numbers(en: str) -> list[str]:
    """Numbers worth a source: percentages, decimals and whole numbers of 10 and more; years, IDs,
    versions, dates and phone numbers are skipped; «12 million» is one number."""
    out = []
    en = NOT_AMOUNTS.sub(" ", SCALED_RE.sub(_scaled, en))   # «12M» becomes a number before names are dropped
    for m in NUM_RE.finditer(en):
        n = norm_number(m.group(1), m.group(2))
        bare = n.rstrip("%")
        if re.fullmatch(r"(19|20)\d\d", bare) and not n.endswith("%"):
            continue
        if n.endswith("%") or "." in bare or float(bare) >= 10:
            out.append(n)
    return out


UNITS = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen "
                                    "fourteen fifteen sixteen seventeen eighteen nineteen".split())}
TENS = {w: 10 * i for i, w in enumerate("_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()) if w != "_"}
SCALES = {"hundred": 100, "thousand": 1000, "million": 1_000_000}
# whole words only: «hundreds of calls» and «tens of thousands» are not numbers
WORDNUM_RE = re.compile(r"\b((?:(?:" + "|".join(list(TENS) + list(UNITS) + list(SCALES)) + r")\b[\s-]*)+)(per ?cent)?", re.I)
SUFFIX_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s?(M|K|k|bn|млн|тыс\.?|млрд)(?![\w])")
SUFFIX = {"k": 1_000, "K": 1_000, "тыс": 1_000, "тыс.": 1_000, "M": 1_000_000, "млн": 1_000_000,
          "bn": 1_000_000_000, "млрд": 1_000_000_000}


def word_numbers(en: str) -> list[str]:
    """Numbers written as words («two percent», «twenty-five», «three hundred»), in the same form as
    block_numbers: percentages, and whole numbers of 10 and more."""
    out = []
    for m in WORDNUM_RE.finditer(en):
        if re.search(r"\d\s*$", en[:m.start()]):   # «12 million»: the digits carry it (block_numbers)
            continue
        nums, total, cur, last = [], 0, 0, ""
        for w in re.split(r"[\s-]+", m.group(1).strip().lower()):
            if (w in UNITS and last in UNITS) or (w in TENS and (last in TENS or last in UNITS)):
                nums.append(total + cur)            # «ten twenty-person teams»: two numbers
                total = cur = 0
            if w in UNITS:
                cur += UNITS[w]
            elif w in TENS:
                cur += TENS[w]
            elif w == "hundred":
                cur = max(cur, 1) * 100
            elif w in SCALES:
                total += max(cur, 1) * SCALES[w]
                cur = 0
            last = w
        nums.append(total + cur)
        for i, n in enumerate(nums):
            if m.group(2) and i == len(nums) - 1:
                out.append(f"{n}%")
            elif n >= 10:
                out.append(str(n))
    return out


def known_number(n: str, known: set[str], rounded: bool = False) -> bool:
    """In facts.md as written; a number in words may also be a fact rounded («about two percent» = 2.1%)."""
    if n in known:
        return True
    if n.endswith("%") and n.rstrip("%") in known and not rounded:   # «2.1» written beside a «%» sign in facts
        return True
    if not rounded:
        return False
    pct, val = n.endswith("%"), float(n.rstrip("%"))
    for k in known:
        if k.endswith("%") == pct:
            try:
                if round(float(k.rstrip("%"))) == val:
                    return True
            except ValueError:
                pass
    return False


def read_cv(path: Path) -> str | None:
    if not path.exists():
        return None
    if path.suffix.lower() == ".pdf":
        import shutil
        import subprocess
        if not shutil.which("pdftotext"):
            return None
        out = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True,
                             errors="replace").stdout
        return out if out.strip() else None   # a scanned PDF has no text layer
    if path.suffix.lower() == ".docx":
        import html
        import zipfile
        try:
            z = zipfile.ZipFile(path)
            parts = ["word/document.xml"] + sorted(n for n in z.namelist()
                                                   if re.fullmatch(r"word/(?:header\d*|footer\d*|footnotes|endnotes)\.xml", n))
            xml = "\n".join(z.read(n).decode("utf-8", "replace") for n in parts)
        except (zipfile.BadZipFile, KeyError, OSError):
            return None
        xml = re.sub(r"<w:(?:br|cr)\b[^>]*/>", "\n", xml.replace("</w:p>", "\n").replace("<w:tab/>", " "))
        return html.unescape(re.sub(r"<[^>]+>", "", xml))
    if path.suffix.lower() not in (".tex", ".md", ".txt", ".html", ".htm"):
        return None
    raw = path.read_bytes()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):   # saved as UTF-16 by some editors
        text = raw.decode("utf-16", "replace")
    elif len(raw) > 3 and raw.count(b"\x00") > len(raw) // 4:   # UTF-16 without its mark
        text = raw.decode("utf-16-le" if raw[1:2] == b"\x00" else "utf-16-be", "replace")
    else:
        text = raw.decode("utf-8-sig", "replace")
    if path.suffix.lower() == ".tex":   # the document body only, without comments, layout sizes and commands
        if "\\begin{document}" in text:
            text = text.split("\\begin{document}", 1)[1]
        text = re.sub(r"(?<!\\)%.*", "", text)
        text = re.sub(r"\d*\.?\d+\s*(in|pt|cm|mm|em|ex|bp)\b|\d*\.?\d+\s*\\(text|line|column)width", " ", text)
        # \fontsize{10}{12}, \definecolor[...]; \textbf{45} and other text commands keep their number
        text = re.sub(r"\\(?!(?:text(?:bf|it|sc|tt|sf|rm|up|sl)|emph|underline|mbox|hl|strong)\b)[a-zA-Z]+\*?"
                      r"(?:\{[\d.,\s]*\}|\[[^\]]*\])+", " ", text)
        text = re.sub(r"\b\d{1,3},\d{1,3},\d{1,3}\b", " ", text)                 # colours like 0,102,204
        text = text.replace("\\%", "%")
        text = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", text)
    elif path.suffix.lower() in (".html", ".htm"):
        import html
        text = re.sub(r"(?is)<(style|script)\b.*?</\1\s*>|<!--.*?-->", " ", text)
        text = re.sub(r"(?i)<br\s*/?>|</(?:p|li|div|h\d|tr|td|section|ul|ol)\s*>", "\n", text)
        text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return text


NO_RULE = re.compile(
    r"password|\baccounts?\b|payment|\bpay(?:s|ing)?\b|money|salary|\boffers?\b|\baccept(?:s|ing)?\b|consent|"
    r"\bterms\b|\bdelet\w*|\bremov\w*|\bwithdraw\w*|\bbook\w*\s+(?:a\s+|the\s+)?(?:call|meeting|slot|interview)|"
    r"\bsubmit\w*\s+(?:\w+\s+){0,3}?(?:forms?|applications?)\b|\b(?:fill\w*|complete\w*)\s+(?:\w+\s+){0,3}?forms?\b|"
    r"\bforms?\b|\bapply(?:ing)?\s+(?:to|for)\b|\bsign(?:ing)?\s+(?:up|in|on|the|a|an|contracts?|offers?)\b|"
    r"\bsignatures?\b|\bsubmit\b(?!\w)(?!ted)", re.I)


def autonomy_errors(ptxt: str) -> list[str]:
    """Rules in profile.yaml → autonomy.rules: each one a block entry with action, since (a date) and
    said (the candidate's words), and none for what no rule may cover (CLAUDE.md §5). The file is read
    the way a YAML reader would take it, so a duplicate key, a second `autonomy:` or a comment line
    cannot hide a rule."""
    import unicodedata
    lines = ptxt.splitlines()
    tops = [i for i, l in enumerate(lines) if re.match(r"autonomy:", l)]
    if len(tops) > 1:
        return ["profile.yaml: `autonomy:` is written twice; keep one (a reader takes the last)"]
    if not tops:
        return []
    if re.match(r"autonomy:[ \t]*\{", lines[tops[0]]):
        return ["profile.yaml: autonomy must be written as a block with one key per line, not «{…}»"]
    body = []
    for l in lines[tops[0] + 1:]:
        if l.strip() == "" or l.lstrip().startswith("#"):
            continue   # blank and comment lines, at any indent, do not end the block
        if not l[:1].isspace():
            break
        body.append(l)
    ri = next((i for i, l in enumerate(body) if re.match(r"[ \t]+rules:", l)), None)
    if ri is None:
        return []
    inline = body[ri].split(":", 1)[1].split("#")[0].strip()
    if inline and inline not in ("[]", "~", "null"):
        return ["profile.yaml: autonomy.rules must be a list with one key per line (not «" + inline[:40] + "»)"]
    rind = len(body[ri]) - len(body[ri].lstrip())
    items: list[list[str]] = []
    dash = None   # the indent of the list's own «- »
    for l in body[ri + 1:]:
        ind = len(l) - len(l.lstrip())
        if ind <= rind and not l.lstrip().startswith("-"):
            break   # the next key under autonomy
        m = re.match(r"([ \t]*)-(?:[ \t]+|$)(.*)", l)
        if m and (dash is None or len(m.group(1)) == dash):
            dash = len(m.group(1))
            items.append([" " * (len(l) - len(m.group(2))) + m.group(2)] if m.group(2) else [])
        elif items:
            items[-1].append(l)
        else:
            return ["profile.yaml: autonomy.rules must be a list (each rule starts with «- »)"]
    out = []
    for e in items:
        keys: dict[str, str] = {}
        kind = None
        cur = None
        for l in e:
            if not l.strip():
                continue
            ind = len(l) - len(l.lstrip())
            if kind is None:
                kind = ind
            m = re.match(r"([A-Za-z_][\w ]*):(.*)$", l.strip())
            if ind == kind and m:
                cur = m.group(1).strip()
                if cur in keys:
                    out.append(f"profile.yaml: an autonomy rule sets «{cur}» twice — it does not count")
                keys[cur] = m.group(2)
            elif ind > kind and cur is not None:
                keys[cur] += "\n" + l.strip()   # a continuation: deeper than its key
            else:
                out.append("profile.yaml: an autonomy rule has a line out of place: «" + l.strip()[:40] + "»")
        action = keys.get("action")
        if action is None:
            out.append("profile.yaml: an autonomy rule without `action:` — it does not count")
            continue
        said_raw = keys.get("said", keys.get("quote", ""))
        said_text = re.sub(r"^[ \t]*[|>][-+]?[ \t]*", "", said_raw).split("#")[0] if not said_raw.lstrip().startswith(("|", ">")) \
            else re.sub(r"^[ \t]*[|>][-+]?[ \t]*", "", said_raw)
        said_text = said_text.strip().strip("\"'")
        if not re.match(r"\s*\d{4}-\d{2}-\d{2}", keys.get("since", "")) or not said_text or said_text.startswith("<"):
            out.append("profile.yaml: an autonomy rule without `since:` (a date) and `said:` (the candidate's words) — it does not count")
        act = unicodedata.normalize("NFKC", action.split("#")[0].strip().strip("\"'"))
        what = " ".join(f"{k}: {v}" for k, v in keys.items() if k not in ("said", "quote"))
        plain = fold(unicodedata.normalize("NFKC", what))   # the words as they read, without invisible characters
        if not re.fullmatch(r"send_followup|send_note", act):
            out.append(f"profile.yaml: autonomy rule «{act[:40]}» — the action is send_followup or send_note; "
                       "nothing else can become a rule")
        elif NO_RULE.search(plain):
            out.append(f"profile.yaml: autonomy rule «{act[:40]}» covers what no rule may "
                       "(passwords, accounts, money, offers, terms, consents, forms, deleting) — remove it")
        elif re.search(r"[^\x20-\x7e«»’“”—–]", what.replace("\n", " ")):   # allow, do not block: printable ASCII
            out.append(f"profile.yaml: autonomy rule «{act}»: write its conditions in plain English letters, with no "
                       "invisible or look-alike characters (only `said:` holds the candidate's own words, in any language)")
    return out


TMP_DIRS = ("/tmp", "/private/tmp", "/var/tmp", "/dev/shm", "/private/var/tmp", "/run/lock", "/var/lock",
            "/users/shared", "/var/folders", "/private/var/folders")   # compared case-folded


def safe_place(p: str, search: Path | None) -> bool:
    """A program or folder a scheduled run trusts: no `..`, not in a temporary folder anyone can write,
    and not inside the search folder, where a downloaded file could replace it."""
    if ".." in Path(p).parts:
        return False
    # macOS and Windows disks ignore case: /Private/Tmp is /private/tmp there, so compare without it
    real = os.path.realpath(os.path.expanduser(p)).casefold()
    given = os.path.normpath(os.path.expanduser(p)).casefold()
    for t in TMP_DIRS:
        if any(x == t or x.startswith(t + "/") for x in (real, given)):
            return False
    import stat
    import tempfile
    tmp = os.path.realpath(tempfile.gettempdir()).casefold()
    if real == tmp or real.startswith(tmp.rstrip("/") + "/"):
        return False
    for anc in Path(os.path.realpath(os.path.expanduser(p))).parents:   # anyone may write there: not trusted
        try:
            if os.stat(anc).st_mode & stat.S_IWOTH:
                return False
        except OSError:
            continue
    if search is not None:
        s = os.path.realpath(search).casefold().rstrip("/")
        if any(x == s or x.startswith(s + "/") for x in (real, given)):
            return False
    return True


def spec_ok(spec: str) -> bool:
    """tracker-mcp 0.8.3 or later in 0.8: the first version whose read-only mode also refuses undo of foreign files."""
    m = re.fullmatch(r"tracker-mcp(?:==0\.8\.(\d+)|>=0\.8\.(\d+),<0\.9)", spec)
    return bool(m) and int(m.group(1) or m.group(2)) >= 3   # pinned inside 0.8: a new minor is checked first


def settings_problems(folder: Path) -> list[str]:
    """Settings a scheduled run in this folder loads (--setting-sources project): hooks and environment
    there run before any check and outside the tool limits, so the run refuses them."""
    out = []
    for f in sorted((folder / ".claude").glob("settings*.json")) if (folder / ".claude").is_dir() else []:
        try:
            data = json.loads(f.read_text(encoding="utf-8-sig"))
        except (ValueError, OSError):
            out.append(f"{f.relative_to(folder)}: not readable JSON — a scheduled run here must not start")
            continue
        if not isinstance(data, dict):
            out.append(f"{f.relative_to(folder)}: not a settings object — a scheduled run here must not start")
            continue
        # only rules that narrow what a run may do: deny and ask lists; everything else (allows, extra
        # folders, modes, plugins and marketplaces, hooks, environment, helpers, status lines, MCP
        # servers) could widen it or run code before the run's own limits apply
        perms = data.get("permissions", {})
        bad = sorted(k for k in data if k not in ("$schema", "permissions"))
        bad += sorted(f"permissions.{k}" for k in (perms if isinstance(perms, dict) else {"?": 0})
                      if k not in ("deny", "ask"))
        if bad:
            out.append(f"{f.relative_to(folder)}: has {', '.join(bad)}; a scheduled run here takes only "
                       "`permissions.deny` and `permissions.ask` from it — move the rest to your user settings "
                       "(which the run does not load) or remove it")
    return out


def instruction_warnings(folder: Path) -> list[str]:
    """Instructions a run in this folder reads besides the kit's: the search folder's CLAUDE.md beyond
    the `@kit/CLAUDE.md` import, the project's other memory files, nested CLAUDE.md files (a cloned
    take-home in companies/), project agents, commands and skills, and parent folders' CLAUDE.md."""
    out = []
    own = folder / "CLAUDE.md"
    if own.is_file():
        extra = [l for l in own.read_text(encoding="utf-8-sig", errors="replace").splitlines()
                 if l.strip() and l.strip() != "@kit/CLAUDE.md"]
        if extra:
            out.append(f"CLAUDE.md in the search folder has {len(extra)} line(s) besides `@kit/CLAUDE.md`; "
                       "a scheduled run reads them as instructions — keep only what you wrote")
    for name in (".claude/CLAUDE.md", "CLAUDE.local.md"):
        if (folder / name).is_file():
            out.append(f"{name}: a scheduled run reads it as instructions; check it is yours")
    for sub in ("agents", "commands", "skills"):
        if (folder / ".claude" / sub).is_dir() and any((folder / ".claude" / sub).iterdir()):
            out.append(f".claude/{sub}/: project {sub} load into every run here; check they are yours")
    for area in ("companies", "applications", "me"):
        for f in sorted((folder / area).rglob("CLAUDE.md")) if (folder / area).is_dir() else []:
            out.append(f"{f.relative_to(folder)}: a CLAUDE.md inside {area}/ (a cloned take-home?) is read when "
                       "a run opens files there; remove it or move the project out")
    for parent in list(folder.resolve().parents)[:-1]:
        if (parent / "CLAUDE.md").is_file():
            out.append(f"{parent / 'CLAUDE.md'}: a parent folder's CLAUDE.md is read by every run here; check it is yours")
    return out


def schedule_problems(me: Path, kit: Path, strict: bool = False) -> list[str]:
    """What a scheduled run trusts in the pack: the values its prompt is filled with, the read-only
    tracker entry, and the dates of earlier run files."""
    out = []
    values = me / "schedules" / "values.yaml"
    unfilled = values.exists() and re.search(r"<[^<>\n]+>", values.read_text(encoding="utf-8-sig"))
    if (values.exists() and not (unfilled and not strict)) or strict:
        import subprocess
        r = subprocess.run([sys.executable, str(kit / "scripts" / "schedule_prompt.py"), "daily", "--me", str(me)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            out.append("schedules/values.yaml: " + (r.stderr.strip().splitlines() or ["cannot fill the prompt"])[-1])
    for name in ("daily.md", "weekly.md", "monthly.md"):
        if (me / "schedules" / name).exists():
            out.append(f"schedules/{name}: a filled prompt in the pack is no longer used (the run builds it from "
                       "the kit with `schedule_prompt.py`); delete it so nothing reads it")
    ro = me / "schedules" / "tracker-ro.mcp.json"
    if not ro.exists():
        if strict:
            out.append("schedules/tracker-ro.mcp.json is missing (skill `tracker`, setup step 4)")
    elif re.search(r"<[a-z][^<>\"\n]*\s[^<>\"\n]*>", ro.read_text(encoding="utf-8-sig")) and not strict:
        pass   # the template, not filled yet: nothing runs from it
    else:
        try:
            servers = json.loads(ro.read_text(encoding="utf-8-sig")).get("mcpServers", {})
        except (ValueError, AttributeError) as e:
            servers = None
            out.append(f"schedules/tracker-ro.mcp.json: not valid JSON ({e})")
        if servers is not None:
            entry = servers.get("tracker-ro") if isinstance(servers, dict) and list(servers) == ["tracker-ro"] else None
            ok = isinstance(entry, dict) and set(entry) <= {"command", "args", "env"}
            if ok:
                cmd, args, env = str(entry.get("command", "")), entry.get("args", []), entry.get("env") or {}
                spec = str(args[1]) if isinstance(args, list) and len(args) > 1 else ""
                ok = (re.fullmatch(r"(/|~/)[\w./ -]*/uvx(\.exe)?", cmd) is not None and safe_place(cmd, me.parent)
                      and isinstance(args, list) and len(args) == 4 and args[0] == "--from"
                      and spec_ok(spec) and args[2] == "tracker-mcp" and args[3] == "--read-only"
                      and isinstance(env, dict) and set(env) <= {"TRACKER_PATH", "TRACKER_CONFIG", "TRACKER_BACKUP_DIR"}
                      and all(isinstance(v, str) for v in env.values())
                      and all(re.match(r"(/|~/)", env[k]) and safe_place(env[k], None)
                              for k in ("TRACKER_CONFIG", "TRACKER_BACKUP_DIR") if k in env)
                      and ("TRACKER_PATH" not in env or env["TRACKER_PATH"].startswith("https://docs.google.com/")
                           or (re.match(r"(/|~/)", env["TRACKER_PATH"]) and safe_place(env["TRACKER_PATH"], None))))
            if not ok:
                out.append("schedules/tracker-ro.mcp.json: not exactly one `tracker-ro` server run by an absolute "
                           "uvx path outside temporary folders and the search folder, as `--from \"tracker-mcp>=0.8.3,<0.9\" "
                           "tracker-mcp --read-only` (TRACKER_CONFIG and TRACKER_BACKUP_DIR absolute too) — a scheduled "
                           "run must not use it")
    out += settings_problems(me.parent)
    today = __import__("datetime").date.today().isoformat()
    for folder in ("runs", "search"):
        for f in sorted((me / folder).rglob("*")) if (me / folder).is_dir() else []:
            m = re.match(r"(\d{4}-\d{2}-\d{2})", f.name)
            if f.is_file() and m and m.group(1) > today:
                out.append(f"{folder}/{f.relative_to(me / folder)}: dated in the future — not a real run; remove it")
    return out


def register(en: str):
    sents = [s for s in SENT_SPLIT.split(en) if len(s.split()) > 1]
    words = WORD_RE.findall(en)
    longest = max((len(s.split()) for s in sents), default=0)
    contractions = CONTRACTION_RE.findall(en.replace("\u2019", "'"))
    return len(words), len(sents), longest, contractions


SYNC_FILE = ".synced.json"


def pack_hashes(me: Path) -> dict[str, str]:
    """sha256 of every pack file, by path relative to the pack."""
    out = {}
    for f in sorted(me.rglob("*")):
        if f.is_file() and f.name != SYNC_FILE and f.suffix in {".md", ".yaml", ".yml"}:
            out[str(f.relative_to(me))] = hashlib.sha256(f.read_bytes()).hexdigest()
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    kit_default = Path(__file__).resolve().parent.parent
    ap.add_argument("--kit", type=Path, default=kit_default)
    ap.add_argument("--me", type=Path, default=None)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--ready", action="store_true",
                    help="fail until the pack can be used: no placeholders in profile and facts, the pitch I01 confirmed")
    ap.add_argument("--schedules", action="store_true",
                    help="check only what a scheduled run trusts (its values, the read-only tracker entry, run files): "
                         "exit 1 on any problem; run it before every scheduled run")
    ap.add_argument("--cv", type=Path, default=None,
                    help="also check a CV (.tex, .md, .txt, .html, .docx, or .pdf with pdftotext): every number in it must be in facts.md, "
                         "and the never-say phrases must not be in it")
    ap.add_argument("--mark-synced", action="store_true",
                    help="record that the pack was just copied to the claude.ai project")
    a = ap.parse_args()
    if a.me is None:
        a.me = find_pack(None, a.kit) or a.kit.parent / "me"

    if a.mark_synced and not a.me.is_dir():
        print(f"no candidate pack at {a.me}: pass --me <path to me/>")
        return 1
    if a.mark_synced:
        manifest = pack_hashes(a.me)
        (a.me / SYNC_FILE).write_text(json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
        print(f"marked as synced: {len(manifest)} files")
        return 0

    if not a.me.is_dir():
        print(f"no candidate pack at {a.me}: pass --me <path to me/> or run /start")
        return 1
    if a.schedules:
        problems = schedule_problems(a.me, a.kit, strict=True)
        for pr in problems:
            print("ERROR  " + pr)
        for w in instruction_warnings(a.me.parent):
            print("WARN   " + w)
        print("schedules: OK" if not problems else "schedules: do not run until this is fixed")
        return 1 if problems else 0
    if not any((a.me / n).exists() for n in ("profile.yaml", "facts.md")):
        print(f"{a.me} has neither profile.yaml nor facts.md, so it is not a pack: "
              "pass --me <path to me/> or run /start")
        return 1
    for name in ("recipes.md", "never-say.md", "facts.md", "profile.yaml"):
        if not (a.me / name).exists():
            print(f"note: {name} is missing in the pack (copy it from kit/pack-template/)")
    global NEED_L2
    prof_path = a.me / "profile.yaml"
    prof_values: dict[str, str] = {}
    prof_dups: list[str] = []
    if prof_path.exists():
        prof_values, prof_dups = yaml_scalars(prof_path.read_text(encoding="utf-8-sig"))
        if native_is_english(prof_values.get("languages.native", "")):
            NEED_L2 = False   # English, English (UK), en, en-GB, en_US
    expect_code = ""
    if prof_path.exists():
        lang = prof_values.get("languages.native", "").lower()
        expect_code = LANG_CODES.get(lang, lang.upper() if re.fullmatch(r"[a-z]{2}", lang) else "")
    blocks, errors = parse_blocks(a.me / "blocks")
    questions = parse_questions(a.kit / "bank" / "questions.md")
    if (a.me / "questions-extra.md").exists():   # the candidate's own questions, section Q
        questions.update(parse_questions(a.me / "questions-extra.md"))
    recipes, empty = parse_recipes(a.me / "recipes.md")
    warnings: list[str] = []

    track = ""
    prof = a.me / "profile.yaml"
    if prof.exists():
        mt = re.match(r"[A-Za-z]+", yaml_scalars(prof.read_text(encoding="utf-8-sig"))[0].get("target.track", ""))
        track = mt.group(0).lower() if mt else ""

    fact_ids = set(re.findall(r"^\| (F-[\w-]+) \|", (a.me / "facts.md").read_text(encoding="utf-8-sig"), re.M)) \
        if (a.me / "facts.md").exists() else set()
    for qid in dict.fromkeys(DUP_RECIPES):
        errors.append(f"recipes.md: {qid} has more than one row (the last one wins); keep one")
    for path in sorted((a.me / "blocks").glob("*.md")):   # F- facts named in block notes
        for n, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            for r in re.findall(r"\bF-\d+[\w-]*", line):
                if fact_ids and r not in fact_ids:
                    errors.append(f"{path.name}:{n}: fact {r} is not in facts.md")
    for qid, refs in recipes.items():
        for r in refs:
            if r.startswith("F-") and r not in fact_ids:
                errors.append(f"recipes.md: {qid} points to fact {r}, which is not in facts.md")
        if qid not in questions:
            errors.append(f"recipes.md: {qid} is not in the question bank")
        for r in refs:
            if r not in blocks and not r.startswith("F-"):
                errors.append(f"recipes.md: {qid} points to missing block {r}")

    # references inside block notes and chains
    for path in sorted((a.me / "blocks").glob("*.md")):
        for n, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            if line.startswith("#### "):
                continue
            for r in REF_RE.findall(line):
                if r not in blocks and not r.startswith("F-"):
                    errors.append(f"{path.name}:{n}: reference to missing block {r}")

    total_words = total_sents = 0
    long_words = 0
    for b in blocks.values():
        w, s, longest, contr = register(b["en"])
        if not b["draft"]:  # drafts and template placeholders do not count towards the register
            total_words += w
            total_sents += max(s, 1)
            long_words += sum(1 for x in WORD_RE.findall(b["en"]) if len(x) >= 8)
        where = f"{b['file']}:{b['line']} {b['id']}"
        if longest > 30:
            warnings.append(f"{where}: a sentence of {longest} words (target under 30)")
        if contr and NEED_L2:   # a native English speaker's contractions are their own voice
            warnings.append(f"{where}: contractions {contr}")
        # one-word slots such as <company> or <city> are filled per vacancy; longer ones are unfinished text
        if not b["draft"] and re.search(r"<[^<>]*(?:\s|…|\.\.\.)[^<>]*>|\bTODO\b|\bTBD\b|\[[^\]]*\b(?:number|name|date|company|цифра|имя|дата)\b[^\]]*\]", b["en"] + b["ru"]):
            warnings.append(f"{where}: confirmed block still has a placeholder (<…>, TODO, [number])")
        if expect_code and b.get("l2code") and b["l2code"] != expect_code:
            errors.append(f"{where}: the native-language line is «{b['l2code']}:», the profile says {expect_code}")
        if DANGLING_EN.match(b["en"]) or DANGLING_RU.match(b["ru"]):
            warnings.append(f"{where}: does not stand alone (starts with a link word); name the project or the subject")

    loose_pat = phrase_pattern

    for phrase in never_say_phrases(a.me / "never-say.md"):
        pat = loose_pat(phrase)
        for b in blocks.values():
            for field in ("en", "ru"):
                if pat.search(fold(b[field])):
                    label = "EN" if field == "en" else (b.get("l2code") or "the native line")
                    warnings.append(f"{b['file']}:{b['line']} {b['id']}: never-say phrase «{phrase}» in {label}")

    for phrase, allowed in never_claims(a.me / "never-say.md"):
        pat = loose_pat(phrase)
        for b in blocks.values():
            # the row's own blocks (and their topic) are where the claim is handled honestly
            if b["id"] in allowed or b["id"].split("-")[0] in {x.split("-")[0] for x in allowed} \
                    or {"G", "Q"} & set(b["types"]):
                continue
            if pat.search(fold(b["en"])) or pat.search(fold(b["ru"])):
                warnings.append(f"{b['file']}:{b['line']} {b['id']}: «{phrase}» is in the never-claim table")

    known = fact_numbers(a.me / "facts.md")
    if prof_path.exists():   # money lives only in the profile (LOG-6 says money.say_aloud)
        floor_numbers: set[str] = set()
        # only say_aloud is said; the floor and the current salary must never appear in a block.
        # Read by the YAML reader, so nesting, quotes and comments are taken as a YAML reader takes them
        for key, val in prof_values.items():
            nums = set(block_numbers(val)) | set(word_numbers(val))
            if key == "money.say_aloud" or key.startswith("money.say_aloud."):
                known |= nums
            elif re.match(r"money\.(?:floor|current_or_last)(?:\.|$)", key):
                floor_numbers |= {n for n in nums if float(n.rstrip("%")) >= 100}
        for b in blocks.values():
            said = set(block_numbers(b["en"]) + block_numbers(b["ru"]) + word_numbers(b["en"]))
            if floor_numbers & said:
                errors.append(f"{b['file']}:{b['line']} {b['id']}: says the money floor or the current salary "
                              f"({', '.join(sorted(floor_numbers & said))}) — those are never said aloud")
    if (a.me / "facts.md").exists():
        for b in blocks.values():
            if b["draft"]:
                continue
            loose = [n for n in block_numbers(b["en"]) + block_numbers(b["ru"]) if not known_number(n, known)]
            loose += [n for n in word_numbers(b["en"]) if not known_number(n, known, rounded=True)]
            if loose:
                warnings.append(f"{b['file']}:{b['line']} {b['id']}: numbers not in facts.md: {', '.join(dict.fromkeys(loose))}")

    if a.cv is not None:
        cv_text = read_cv(a.cv)
        if cv_text is None:
            errors.append(f"--cv: cannot read {a.cv} (.tex, .md, .txt, .html, .docx, or a .pdf with a text layer "
                          "and pdftotext installed; a scanned PDF has no text)")
        else:   # contact lines (phone, email, address, links) carry no claims
            cv_text = re.sub(r"\S+@\S+|https?://\S+|www\.\S+|(?:linkedin|github)\.com/\S*"
                             r"|(?<![\w%])\+\d[\d\s().-]{6,}\d", " ", cv_text, flags=re.I)   # contacts carry no claims
            cv_loose = [n for n in block_numbers(cv_text) if not known_number(n, known)]
            cv_loose += [n for n in word_numbers(cv_text) if not known_number(n, known, rounded=True)]
            if cv_loose:
                warnings.append(f"CV {a.cv.name}: numbers not in facts.md: {', '.join(dict.fromkeys(cv_loose))} "
                              "(a difference between the CV and facts.md is a question for the candidate)")
                for n in dict.fromkeys(cv_loose):   # where each one is, so it can be found in the CV
                    line = next((l.strip() for l in cv_text.splitlines()
                                 if n in block_numbers(l) + word_numbers(l)), "")
                    if line:
                        warnings.append(f"CV {a.cv.name}: {n} in «{line[:100]}»")
            else:
                print(f"CV {a.cv.name}: every number is in facts.md")
            for phrase, _ in never_claims(a.me / "never-say.md"):
                if " " in phrase.strip() and loose_pat(phrase).search(fold(cv_text)):   # phrases: a CV lists bare tool names
                    warnings.append(f"CV {a.cv.name}: «{phrase}» is in the never-claim table")

    if prof_path.exists():
        ptxt = prof_path.read_text(encoding="utf-8-sig")
        errors += profile_syntax_errors(ptxt)
        errors += autonomy_errors(ptxt)
        for k in prof_dups:
            if not k.startswith("autonomy."):   # autonomy_errors names those itself
                errors.append(f"profile.yaml: «{k}» is set twice; a reader takes the last one — keep one")
    errors += schedule_problems(a.me, a.kit)
    for name in ("facts.md", "profile.yaml", "search-rules.md"):
        f = a.me / name
        if f.exists():
            lines = f.read_text(encoding="utf-8-sig").splitlines()
            if name.endswith(".yaml"):   # YAML comments are instructions, not values
                lines = [l for l in lines if not l.lstrip().startswith("#")]
            # `<tracker>.toml` and «call recording <date>» are examples in the template's prose
            body = re.sub(r"`[^`\n]*`|«[^»\n]*»", "", "\n".join(lines))
            left = len(re.findall(r"<[^<>\n]{1,80}>|\bTODO\b", body))
            if left:
                warnings.append(f"{name}: {left} placeholder(s) left to fill")

    if NEED_L2 and total_words and long_words / total_words > 0.13:
        warnings.append(f"EN register: {100 * long_words / total_words:.1f}% words of 8+ letters (target under 13%): "
                        "swap long words for short ones")

    drafts = {q for q, refs in recipes.items() if refs and any(blocks.get(r, {}).get("draft") for r in refs)}
    covered = {q for q, refs in recipes.items() if refs} - drafts
    if any(q.startswith("Z") for q in questions) and any(k.startswith("ASK-") and not v["draft"] for k, v in blocks.items()):
        covered |= {q for q in questions if q.startswith("Z")}
    missing = [q for q in questions if q not in covered]
    core = [q for q in questions if questions[q] == "★"]
    role = [q for q in questions if questions[q] == "◆"]
    if track and track not in ("manager", "рук", "руководитель"):
        role = [q for q in role if AUDIENCE.get(q) not in ("рук.", "mgr")]
    core_missing = [q for q in core if q in missing]
    role_missing = [q for q in role if q in missing]
    topics: dict[str, set] = {}
    for bid, b in blocks.items():
        topics.setdefault(bid.split("-")[0], set()).update(b["types"])
    stories = {t for t, ts in topics.items() if "R" in ts or {"L", "O"} <= ts or "S" in ts}
    no_whole = sorted(t for t in stories if "S" not in topics[t])

    by_type: dict[str, int] = {}
    for b in blocks.values():
        for t in b["types"]:
            by_type[t] = by_type.get(t, 0) + 1

    print(f"blocks: {len(blocks)}  " + "  ".join(f"{t}:{by_type[t]}" for t in sorted(by_type)))
    print(f"questions: {len(questions)}  with a recipe: {len(covered)}  without: {len(missing)}")
    core_drafts = [q for q in core if q in drafts]
    print(f"core ★: {len(core) - len(core_missing)}/{len(core)}  role ◆: {len(role) - len(role_missing)}/{len(role)}"
          + (f" ({track})" if track else " (set `track:` in profile.yaml to count only your role)")
          + (f"  drafts, not counted: {len(drafts)}" if drafts else ""))
    print(f"stories with a whole S block: {len(stories) - len(no_whole)}/{len(stories)}")
    if total_sents:
        print(f"EN register: {total_words / total_sents:.1f} words per sentence, "
              f"{100 * long_words / max(total_words, 1):.1f}% words of 8+ letters (targets 12-15 and under 13%)")
    if core_missing:
        print("★ without a confirmed recipe: " + ", ".join(core_missing)
              + (f" (draft: {', '.join(core_drafts)})" if core_drafts else ""))
    if role_missing:
        print("◆ without a recipe: " + ", ".join(role_missing))
    rest = [q for q in missing if q not in core_missing and q not in role_missing]
    if rest:
        print("other without a recipe: " + ", ".join(rest))
    if no_whole:
        print("stories without a whole S block: " + ", ".join(no_whole))
    sync_file = a.me / SYNC_FILE
    if sync_file.exists():
        old = json.loads(sync_file.read_text(encoding="utf-8-sig"))
        if not isinstance(old, dict):
            raise ValueError(f"{sync_file} is not the manifest --mark-synced writes; delete it and mark again")
        now = pack_hashes(a.me)
        changed = sorted(f for f in now if old.get(f) != now[f]) + sorted(f for f in old if f not in now)
        if changed:
            print("changed since the last copy to the project (update it, then --mark-synced): " + ", ".join(changed))
        else:
            print("project copy: in sync")
    # no manifest: the candidate keeps no project copy, or has not marked it yet — say nothing
    for e in errors:
        print("ERROR  " + e)
    for w in warnings:
        print("WARN   " + w)
    if a.ready:
        not_ready = [w for w in warnings if w.startswith(("profile.yaml:", "facts.md:")) and "placeholder" in w]
        not_ready += [f"{n} is missing" for n in ("profile.yaml", "facts.md") if not (a.me / n).exists()]
        if "I01" not in covered:
            not_ready.append("the pitch I01 has no confirmed recipe")
        for r in not_ready:
            print("NOT READY  " + r)
        if not_ready:
            return 1
    if errors or (a.strict and warnings):
        return 1
    print("OK" if not warnings else f"OK with {len(warnings)} warning(s)")
    return 0


def _decodes(f: Path) -> bool:
    try:
        f.read_bytes().decode("utf-8")
        return True
    except (UnicodeDecodeError, OSError):
        return False


READ_ERRORS = (UnicodeDecodeError, IsADirectoryError, NotADirectoryError, PermissionError, FileNotFoundError, ValueError)


def friendly_errors() -> None:
    """For every kit script: a file that is not UTF-8 text, a folder where a file should be, a broken
    link or a damaged manifest gives one line saying which file, and exit 1 — never a traceback."""
    def hook(kind, e, tb):
        if not isinstance(e, READ_ERRORS):
            return sys.__excepthook__(kind, e, tb)
        name = getattr(e, "filename", None) or ""
        if isinstance(e, UnicodeDecodeError):   # the error does not carry the file: find the ones that fail
            me_arg = sys.argv[sys.argv.index("--me") + 1] if "--me" in sys.argv[:-1] else "me"
            files = [Path(x) for x in sys.argv[1:] if Path(x).is_file()]
            files += [f for f in sorted(Path(me_arg).rglob("*")) if f.is_file()
                      and f.suffix in (".md", ".yaml", ".yml", ".json", ".txt")] if Path(me_arg).is_dir() else []
            name = ", ".join(str(f) for f in files if not _decodes(f))[:400]
        print(f"cannot read {name or 'a file'}: {kind.__name__}: {e}. Save it as UTF-8 text "
              "(or replace the folder or broken link with the file) and run again.", file=sys.stderr)
        sys.exit(1)
    sys.excepthook = hook


if __name__ == "__main__":
    friendly_errors()
    sys.exit(main())
