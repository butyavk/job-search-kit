#!/usr/bin/env python3
"""Check a candidate pack against the kit.

Usage:
    python3 kit/scripts/check_pack.py [--me PATH] [--kit PATH] [--strict]

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
           marked `черновик` counts as a draft, not as covered;
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
DANGLING_RU = re.compile(r"^(Потом|Это |Так |Плюс|Тоже|Также|И |Но |Там |Он |Она |Они |Поэтому|После этого|Здесь|Вместо|Ещё |Дальше)")
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
              "русский": "RU", "украинский": "UK"}

NUM_RE = re.compile(r"(?<![\w.,])(\d{1,3}(?:[ \u00a0,]\d{3})+(?![\d,.])|\d+(?:[.,]\d+)?)(\s?%)?")


def norm_number(raw: str, pct: str | None) -> str:
    if re.fullmatch(r"\d{1,3}(?:[ \u00a0,]\d{3})+", raw):  # 450 000 · 450,000 — thousands
        n = re.sub(r"[ \u00a0,]", "", raw)
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
    return out


def block_numbers(en: str) -> list[str]:
    """Numbers worth a source: percentages, decimals and whole numbers of 10 and more; years are skipped."""
    out = []
    for m in NUM_RE.finditer(en):
        n = norm_number(m.group(1), m.group(2))
        bare = n.rstrip("%")
        if re.fullmatch(r"(19|20)\d\d", bare) and not n.endswith("%"):
            continue
        if n.endswith("%") or "." in bare or float(bare) >= 10:
            out.append(n)
    return out


def register(en: str):
    sents = [s for s in SENT_SPLIT.split(en) if len(s.split()) > 1]
    words = WORD_RE.findall(en)
    longest = max((len(s.split()) for s in sents), default=0)
    contractions = CONTRACTION_RE.findall(en)
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
    ap.add_argument("--mark-synced", action="store_true",
                    help="record that the pack was just copied to the claude.ai project")
    a = ap.parse_args()
    if a.me is None:
        env = os.environ.get("JOB_SEARCH_ME")
        cands = [Path(env).expanduser()] if env else []
        cands += [a.kit.parent / "me", Path.cwd() / "me"]
        a.me = next((c for c in cands if c.is_dir()), cands[0])

    if a.mark_synced:
        manifest = pack_hashes(a.me)
        (a.me / SYNC_FILE).write_text(json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
        print(f"marked as synced: {len(manifest)} files")
        return 0

    if not a.me.is_dir():
        print(f"no candidate pack at {a.me}: pass --me <path to me/> or run /start")
        return 1
    for name in ("recipes.md", "never-say.md", "facts.md"):
        if not (a.me / name).exists():
            print(f"note: {name} is missing in the pack (copy it from kit/pack-template/)")
    global NEED_L2
    prof_path = a.me / "profile.yaml"
    if prof_path.exists():
        mn = re.search(r"^\s*native:\s*([^#\n]+)", prof_path.read_text(encoding="utf-8"), re.M)
        if mn and mn.group(1).strip().strip("\"'").lower() in ("english", "en"):
            NEED_L2 = False
    expect_code = ""
    if prof_path.exists():
        mn2 = re.search(r"^\s*native:\s*([^#\n]+)", prof_path.read_text(encoding="utf-8"), re.M)
        lang = mn2.group(1).strip().strip("\"'").lower() if mn2 else ""
        expect_code = LANG_CODES.get(lang, lang.upper() if re.fullmatch(r"[a-z]{2}", lang) else "")
    blocks, errors = parse_blocks(a.me / "blocks")
    questions = parse_questions(a.kit / "bank" / "questions.md")
    recipes, empty = parse_recipes(a.me / "recipes.md")
    warnings: list[str] = []

    track = ""
    prof = a.me / "profile.yaml"
    if prof.exists():
        mt = re.search(r"^\s*track:\s*([A-Za-z]+)", prof.read_text(encoding="utf-8"), re.M)
        track = mt.group(1).lower() if mt else ""

    for qid, refs in recipes.items():
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
        if contr:
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
    if (a.me / "facts.md").exists():
        for b in blocks.values():
            if b["draft"]:
                continue
            loose = [n for n in block_numbers(b["en"]) + block_numbers(b["ru"]) if n not in known and n.rstrip("%") not in known]
            if loose:
                warnings.append(f"{b['file']}:{b['line']} {b['id']}: numbers not in facts.md: {', '.join(dict.fromkeys(loose))}")

    if prof_path.exists():
        ptxt = prof_path.read_text(encoding="utf-8")
        for rule in re.findall(r"^  - action:.*?(?=^  - |^\S|\Z)", ptxt, re.M | re.S):
            if not re.search(r"^\s+since:\s*\d{4}-\d{2}-\d{2}", rule, re.M) or not re.search(r"^\s+(?:quote|said):\s*\S", rule, re.M):
                errors.append("profile.yaml: an autonomy rule without `since:` (a date) and `said:` (the candidate's words) — it does not count")
    for name in ("facts.md", "profile.yaml", "search-rules.md"):
        f = a.me / name
        if f.exists():
            left = len(re.findall(r"<[^<>\n]{1,80}>|\bTODO\b", "\n".join(l for l in f.read_text(encoding="utf-8").splitlines() if not l.lstrip().startswith("#"))))
            if left:
                warnings.append(f"{name}: {left} placeholder(s) left to fill")

    if total_words and long_words / total_words > 0.13:
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
    if errors or (a.strict and warnings):
        return 1
    print("OK" if not warnings else f"OK with {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
