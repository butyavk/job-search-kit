#!/usr/bin/env python3
"""Check a candidate pack against the kit.

Usage:
    python3 kit/scripts/check_pack.py [--me PATH] [--kit PATH] [--strict] [--ready] [--cv CV] [--mark-synced]

The pack is --me, else $JOB_SEARCH_ME, else ../me next to the kit folder, else ./me. The script reads
me/blocks/*.md, me/recipes.md, me/never-say.md and kit/bank/questions.md, and
reports:

  errors   duplicate block IDs, recipes that point to missing blocks or questions,
           blocks without EN text or without the native-language line (any `- XX:`
           two-letter code, required unless languages.native is English),
           unknown block types;
  warnings English that breaks the C1 register (contractions, a sentence over 30
           words, more than 13% long words), phrases from never-say.md (the
           filler list and the English parts of the «never claim» table) found
           in block text, blocks that cannot stand alone (start with "Then",
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
                         r"|Luego|Entonces|Después|Eso |Esto |También|Pero |Además)")   # Russian and Spanish openers
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*")


def parse_blocks(blocks_dir: Path):
    blocks: dict[str, dict] = {}
    errors: list[str] = []
    for path in sorted(blocks_dir.glob("*.md")):
        current = None
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
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
    for line in bank.read_text(encoding="utf-8").splitlines():
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
    for line in recipes.read_text(encoding="utf-8").splitlines():
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
    text = path.read_text(encoding="utf-8")
    m = re.search(r"## (?:Фразы-паразиты|Filler words)[^\n]*\n+(.+?)(\n## |\Z)", text, re.S)
    if not m:
        return []
    phrases = []
    for item in m.group(1).replace("\n", " ").split(" · "):
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
    m = re.search(r"## (?:Утверждения|Never claim)[^\n]*\n(.+?)(\n## |\Z)", path.read_text(encoding="utf-8"), re.S)
    if not m:
        return []
    out = []
    for line in m.group(1).splitlines():
        if not line.startswith("|") or line.startswith("| ---") or line.startswith("| Нельзя") or line.startswith("| Never"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        allowed = set(REF_RE.findall(line))
        for part in re.split(r"[;/]|, ", cells[0]):
            part = part.strip().strip("«»\"' ")
            if len(part) < 4 or re.search(r"[А-Яа-яЁё<]", part):
                continue  # Russian descriptions and placeholders need a human
            out.append((part, allowed))
    return out


LANG_CODES = {"russian": "RU", "ukrainian": "UK", "belarusian": "BE", "german": "DE", "spanish": "ES",
              "french": "FR", "italian": "IT", "portuguese": "PT", "polish": "PL", "dutch": "NL",
              "turkish": "TR", "georgian": "KA", "armenian": "HY", "kazakh": "KK", "serbian": "SR",
              "chinese": "ZH", "japanese": "JA", "korean": "KO", "hebrew": "HE", "arabic": "AR", "hindi": "HI",
              "русский": "RU", "украинский": "UK", "español": "ES", "espanol": "ES", "deutsch": "DE",
              "français": "FR", "francais": "FR", "português": "PT", "portugues": "PT", "italiano": "IT",
              "polski": "PL", "türkçe": "TR", "nederlands": "NL"}

# thousands: 450 000 · 450,000 · 65.000 (not «3 100-person»: a group glued to a word is its own number)
NUM_RE = re.compile(r"(?<![\w.,])(\d{1,3}(?:[ \u00a0,.]\d{3})+(?![\d\w-]|[,.]\d)|\d+(?:[.,]\d+)?)(\s?%)?")


def norm_number(raw: str, pct: str | None) -> str:
    if re.fullmatch(r"\d{1,3}(?:[ \u00a0,.]\d{3})+", raw):  # 450 000 · 450,000 · 65.000 — thousands
        n = re.sub(r"[ \u00a0,.]", "", raw)
    else:
        n = raw.replace(",", ".")  # 2,1 — a decimal comma
    return n + ("%" if pct else "")


def fact_numbers(path: Path) -> set[str]:
    """Numbers stated as facts: table cells after the ID and before the source and confirmation columns."""
    if not path.exists():
        return set()
    out = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| F-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        for cell in cells[1:-2] if len(cells) > 3 else cells[1:]:
            out |= {norm_number(m.group(1), m.group(2)) for m in NUM_RE.finditer(cell)}
            for m in SUFFIX_RE.finditer(cell):   # €1M, 10K, 2 млн → the whole number too
                v = float(m.group(1).replace(",", ".")) * SUFFIX[m.group(2)]
                out.add(str(int(v)) if v == int(v) else str(v))
    return out


MONTHS = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?"
NOT_AMOUNTS = re.compile(
    r"`[^`]*`"                                             # code spans
    r"|\b[A-Z]{1,6}-[A-Z]?\d+\b"                           # block and fact IDs: PAY-S1, F-99
    r"|\+\d[\d\s().-]{6,}\d"                               # phone numbers
    r"|\b\d{1,2}[/.]\d{4}\b|\b\d{4}-\d{2}(?:-\d{2})?\b"    # 11/2026, 2026-11-14
    r"|\b\d{1,2}(?:st|nd|rd|th)?\s+" + MONTHS + r"|\b" + MONTHS + r"\s+\d{1,2}\b"   # 15 March, March 15
    r"|\b(?:v|Python|Java|Go|Node(?:\.js)?|PHP|Ruby|Scala|Kotlin|Swift|C\+\+|\.NET|Postgre(?:s|SQL)|MySQL|Terraform|Rust|TypeScript|Spark|Windows|Java|iOS|Android|"
    r"ISO|IEC|SOC|PCI(?: DSS)?|HTTP|TLS|IPv|React|Angular|Vue|Next\.js|Spring|Rails|Django|Ubuntu|Debian|k8s|"
    r"Kubernetes|Java ?SE|ES|Python ?3|Swift ?UI)\s?/?\d[\d.]*"  # versions and standards
    r"|\b\d+/\d+\b"                                          # ratios and rules: 80/20, 24/7
    r"|\b\d+[A-Za-z][\w-]*")                                  # names glued to digits: 37signals, 2FA, 3rd
SCALED_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*(million|billion|thousand|M|K|k|bn)\b(?!-)")
SCALE_OF = {"million": 1_000_000, "billion": 1_000_000_000, "thousand": 1_000, "M": 1_000_000, "K": 1_000,
            "k": 1_000, "bn": 1_000_000_000}


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
        return subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True).stdout
    if path.suffix.lower() == ".docx":
        import zipfile
        try:
            xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8", "replace")
        except (zipfile.BadZipFile, KeyError):
            return None
        return re.sub(r"<[^>]+>", "", xml.replace("</w:p>", "\n").replace("<w:tab/>", " "))
    if path.suffix.lower() not in (".tex", ".md", ".txt", ".html", ".htm"):
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".tex":   # the document body only, without comments, layout sizes and commands
        if "\\begin{document}" in text:
            text = text.split("\\begin{document}", 1)[1]
        text = re.sub(r"(?<!\\)%.*", "", text)
        text = re.sub(r"\d*\.?\d+\s*(in|pt|cm|mm|em|ex|bp)\b|\d*\.?\d+\s*\\(text|line|column)width", " ", text)
        text = re.sub(r"\\[a-zA-Z]+\*?(?:\{[\d.,\s]*\}|\[[^\]]*\])+", " ", text)   # \fontsize{10}{12}, \definecolor[...]
        text = re.sub(r"\b\d{1,3},\d{1,3},\d{1,3}\b", " ", text)                 # colours like 0,102,204
        text = text.replace("\\%", "%")
        text = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", text)
    elif path.suffix.lower() in (".html", ".htm"):
        text = re.sub(r"<[^>]+>", " ", text)
    return text


NO_RULE = re.compile(r"password|account|payment|\bpay\b|money|salary|offer|accept|consent|terms|delete|"
                     r"submit|(?<![a-z])forms?(?![a-z])|(?<![a-z])appl(?:y|ies|ication)|(?<![a-z])sign", re.I)


def autonomy_errors(ptxt: str) -> list[str]:
    """Rules in profile.yaml → autonomy.rules: each one a block entry with action, since (a date) and
    said (the candidate's words), and none for what no rule may cover (CLAUDE.md §5)."""
    if re.search(r"^autonomy:[ \t]*\{", ptxt, re.M):
        return ["profile.yaml: autonomy must be written as a block with one key per line, not «{…}»"]
    m = re.search(r"^autonomy:[^\n]*\n((?:[ \t]+[^\n]*\n?|\n)*)", ptxt, re.M)
    if not m:
        return []
    body = "\n".join(l for l in m.group(1).splitlines() if not l.lstrip().startswith("#"))
    mr = re.search(r"^([ \t]*)rules:[ \t]*(.*)$", body, re.M)
    if not mr:
        return []
    inline = mr.group(2).split("#")[0].strip()
    if inline and inline not in ("[]", "~", "null"):
        return ["profile.yaml: autonomy.rules must be a list with one key per line (not «" + inline[:40] + "»)"]
    rest = body[mr.end():]
    first = re.search(r"^([ \t]*)-(?:[ \t]|$)", rest, re.M)
    if not first:
        return []
    entries = re.split(r"^" + re.escape(first.group(1)) + r"-(?:[ \t]+|$)", rest, flags=re.M)[1:]
    out = []
    for e in entries:
        action = re.search(r"(?:^|\n)\s*action:\s*([^\n]+)", "\n" + e)
        if not action:
            out.append("profile.yaml: an autonomy rule without `action:` — it does not count")
            continue
        said = re.search(r"(?:^|\n)\s*(?:quote|said):[ \t]*([|>][-+]?[ \t]*\n((?:[ \t]+.*\n?)*)|[^\n]*)", "\n" + e)
        said_text = (said.group(2) if said and said.group(2) is not None else (said.group(1) if said else "")).strip().strip("\"'")
        if not re.search(r"(?:^|\n)\s*since:\s*\d{4}-\d{2}-\d{2}", "\n" + e) or not said_text \
                or said_text.startswith("<"):
            out.append("profile.yaml: an autonomy rule without `since:` (a date) and `said:` (the candidate's words) — it does not count")
        act = action.group(1).split("#")[0].strip().strip("\"'")
        what = act + " " + " ".join(re.findall(r"(?:^|\n)\s*(?:when|checks):\s*([^\n]+)", "\n" + e))
        if not re.fullmatch(r"send_followup|send_note|other \(.+\)", act):
            out.append(f"profile.yaml: autonomy rule «{act[:40]}» — the action is send_followup, send_note or "
                       "other (what, in words); nothing else can become a rule")
        elif NO_RULE.search(what):
            out.append(f"profile.yaml: autonomy rule «{action.group(1).strip()[:40]}» covers what no rule may "
                       "(passwords, accounts, money, offers, terms, consents, forms, deleting) — remove it")
    return out


def schedule_problems(me: Path, kit: Path, strict: bool = False) -> list[str]:
    """What a scheduled run trusts in the pack: the values its prompt is filled with, the read-only
    tracker entry, and the dates of earlier run files."""
    out = []
    values = me / "schedules" / "values.yaml"
    unfilled = values.exists() and re.search(r"<[^<>\n]+>", values.read_text(encoding="utf-8"))
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
    elif re.search(r"<[a-z][^<>\"\n]*\s[^<>\"\n]*>", ro.read_text(encoding="utf-8")) and not strict:
        pass   # the template, not filled yet: nothing runs from it
    else:
        try:
            servers = json.loads(ro.read_text(encoding="utf-8")).get("mcpServers", {})
        except (ValueError, AttributeError) as e:
            servers = None
            out.append(f"schedules/tracker-ro.mcp.json: not valid JSON ({e})")
        if servers is not None:
            entry = servers.get("tracker-ro") if isinstance(servers, dict) and list(servers) == ["tracker-ro"] else None
            ok = isinstance(entry, dict) and set(entry) <= {"command", "args", "env"}
            if ok:
                cmd, args, env = str(entry.get("command", "")), entry.get("args", []), entry.get("env") or {}
                ok = (re.fullmatch(r"(/|~/)[\w./ -]*/uvx(\.exe)?", cmd) is not None and not cmd.startswith(("/tmp/", "/var/tmp/"))
                      and isinstance(args, list) and len(args) == 4 and args[0] == "--from"
                      and re.fullmatch(r"tracker-mcp(==\d+(\.\d+)*|>=\d+(\.\d+)*(,<\d+(\.\d+)*)?)", str(args[1])) is not None
                      and args[2] == "tracker-mcp" and args[3] == "--read-only"
                      and isinstance(env, dict) and set(env) <= {"TRACKER_PATH", "TRACKER_CONFIG", "TRACKER_BACKUP_DIR"})
            if not ok:
                out.append("schedules/tracker-ro.mcp.json: not exactly one `tracker-ro` server run by an absolute "
                           "uvx path as `--from tracker-mcp<version> tracker-mcp --read-only` — a scheduled run must not use it")
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
                    help="also check a CV (.tex, .md, .txt, .html, or .pdf with pdftotext): every number in it must be in facts.md")
    ap.add_argument("--mark-synced", action="store_true",
                    help="record that the pack was just copied to the claude.ai project")
    a = ap.parse_args()
    if a.me is None:
        env = os.environ.get("JOB_SEARCH_ME")
        cands = [Path(env).expanduser()] if env else []
        cands += [a.kit.parent / "me", Path.cwd() / "me"]
        a.me = next((c for c in cands if c.is_dir()), cands[0])

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
    if prof_path.exists():
        mn = re.search(r"^\s*native:\s*([^#\n]+)", prof_path.read_text(encoding="utf-8"), re.M)
        native_value = mn.group(1).strip().strip("\"'").lower() if mn else ""
        if native_value and not native_value.startswith("<") and \
                re.search(r"(^|\s)english\b|^en(?:[-_][a-z]{2})?$", native_value):
            NEED_L2 = False   # English, English (UK), en, en-GB, en_US
    expect_code = ""
    if prof_path.exists():
        mn2 = re.search(r"^\s*native:\s*([^#\n]+)", prof_path.read_text(encoding="utf-8"), re.M)
        lang = mn2.group(1).strip().strip("\"'").lower() if mn2 else ""
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
        mt = re.search(r"^\s*track:\s*([A-Za-z]+)", prof.read_text(encoding="utf-8"), re.M)
        track = mt.group(1).lower() if mt else ""

    fact_ids = set(re.findall(r"^\| (F-[\w-]+) \|", (a.me / "facts.md").read_text(encoding="utf-8"), re.M)) \
        if (a.me / "facts.md").exists() else set()
    for qid in dict.fromkeys(DUP_RECIPES):
        errors.append(f"recipes.md: {qid} has more than one row (the last one wins); keep one")
    for path in sorted((a.me / "blocks").glob("*.md")):   # F- facts named in block notes
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
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
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
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

    for phrase in never_say_phrases(a.me / "never-say.md"):
        pat = re.compile(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", re.IGNORECASE)
        for b in blocks.values():
            for field in ("en", "ru"):
                if pat.search(b[field]):
                    warnings.append(f"{b['file']}:{b['line']} {b['id']}: never-say phrase «{phrase}» in {field.upper()}")

    for phrase, allowed in never_claims(a.me / "never-say.md"):
        pat = re.compile(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", re.IGNORECASE)
        for b in blocks.values():
            # the row's own blocks (and their topic) are where the claim is handled honestly
            if b["id"] in allowed or b["id"].split("-")[0] in {x.split("-")[0] for x in allowed} \
                    or {"G", "Q"} & set(b["types"]):
                continue
            if pat.search(b["en"]):
                warnings.append(f"{b['file']}:{b['line']} {b['id']}: «{phrase}» is in the never-claim table")

    known = fact_numbers(a.me / "facts.md")
    if prof_path.exists():   # money lives only in the profile (LOG-6 says money.say_aloud)
        mm = re.search(r"^money:[^\n]*\n((?:[ \t]+.*\n?|[ \t]*\n|[ \t]*#.*\n)*)", prof_path.read_text(encoding="utf-8"), re.M)
        floor_numbers: set[str] = set()
        if mm:   # only say_aloud is said; the floor and the current salary must never appear in a block
            money = re.sub(r"#.*", "", mm.group(1))
            first = re.search(r"^([ \t]+)[a-z_]+:", money, re.M)   # the first level under money:, nested keys stay inside
            ind = re.escape(first.group(1)) if first else r"[ \t]+"
            parts = re.split(r"^(" + ind + r"[a-z_]+:)", money, flags=re.M)
            for key, val in zip(parts[1::2], parts[2::2]):
                nums = {norm_number(m.group(1), m.group(2))
                        for m in NUM_RE.finditer(SCALED_RE.sub(_scaled, NOT_AMOUNTS.sub(" ", val)))}
                if key.strip().startswith("say_aloud"):
                    known |= nums
                elif key.strip().startswith(("floor", "current_or_last")):
                    floor_numbers |= {n for n in nums if float(n.rstrip("%")) >= 100}
        for b in blocks.values():
            said = set(block_numbers(b["en"]) + block_numbers(b["ru"]))
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
            errors.append(f"--cv: cannot read {a.cv} (.tex, .md, .txt, .html, .docx, or .pdf with pdftotext)")
        else:   # contact lines (phone, email, address, links) carry no claims
            cv_text = "\n".join(l for l in cv_text.splitlines()
                                if not re.search(r"@|https?://|www\.|linkedin|github|\+\d|\btel\b|\bphone\b", l, re.I))
            cv_loose = [n for n in block_numbers(cv_text) if not known_number(n, known)]
            cv_loose += [n for n in word_numbers(cv_text) if not known_number(n, known, rounded=True)]
            if cv_loose:
                warnings.append(f"CV {a.cv.name}: numbers not in facts.md: {', '.join(dict.fromkeys(cv_loose))} "
                              "(a difference between the CV and facts.md is a question for the candidate)")
            else:
                print(f"CV {a.cv.name}: every number is in facts.md")

    if prof_path.exists():
        ptxt = prof_path.read_text(encoding="utf-8")
        errors += autonomy_errors(ptxt)
    errors += schedule_problems(a.me, a.kit)
    for name in ("facts.md", "profile.yaml", "search-rules.md"):
        f = a.me / name
        if f.exists():
            lines = f.read_text(encoding="utf-8").splitlines()
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
        old = json.loads(sync_file.read_text(encoding="utf-8"))
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


if __name__ == "__main__":
    sys.exit(main())
