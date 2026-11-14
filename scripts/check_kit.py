#!/usr/bin/env python3
"""Check the kit itself (run in CI and before a release).

1. Every kit path named in backticks in the kit's Markdown files exists
   (templates/…, skills/…, schedules/…, scripts/…, bank/…, pack-template/…,
   examples/…, docs/…, commands/…, tools/…), and every `me/…` file the
   instructions name exists in pack-template/.
   Relative Markdown links ([text](path)) in those files point to files that exist.
2. The two copies of the rules are the same text, line for line and in order:
   CLAUDE.md after its title, skills/job-search-kit/SKILL.md after its frontmatter
   (each one's note about the other copy aside).
3. Every skill named as «skill `x`» or «`x` skill» exists.

Exit code 1 on any problem.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
TICK = re.compile(r"`([^`\s]+)`")
KIT_DIRS = ("templates", "skills", "schedules", "scripts", "bank", "pack-template",
            "examples", "docs", "commands", "tools")
# files that describe paths inside a generated folder, not the kit
SKIP_FILES = {"skills/company-trainer/SKILL.md", "CHANGELOG.md"}


def md_files() -> list[Path]:
    out = []
    for p in KIT.rglob("*.md"):
        rel = p.relative_to(KIT).as_posix()
        if rel.startswith(("site/", ".git/", "node_modules/")) or "/node_modules/" in rel:
            continue
        out.append(p)
    return sorted(out)


def check_paths() -> list[str]:
    problems = []
    for f in md_files():
        rel = f.relative_to(KIT).as_posix()
        if rel in SKIP_FILES:
            continue
        for raw in TICK.findall(f.read_text(encoding="utf-8-sig")):
            p = re.sub(r"^(\$\{CLAUDE_PLUGIN_ROOT(:-kit)?\}|<kit>)/", "", raw)
            p = re.sub(r"^kit/", "", p).split("#")[0].rstrip(".,;:")
            if any(c in p for c in "<*…{") or p.endswith("/"):
                continue
            if p.startswith("me/"):
                if not (KIT / "pack-template" / p[3:]).exists():
                    problems.append(f"{rel}: `{raw}` — not in pack-template/")
            elif p.split("/")[0] in KIT_DIRS and "/" in p:
                if not (KIT / p).exists():
                    problems.append(f"{rel}: `{raw}` — no such file in the kit")
    return problems


LINK = re.compile(r"\]\(([^)\s]+)\)")


def check_links() -> list[str]:
    problems = []
    for f in md_files():
        rel = f.relative_to(KIT).as_posix()
        if rel in SKIP_FILES:
            continue
        for target in LINK.findall(f.read_text(encoding="utf-8-sig")):
            if target.startswith(("http://", "https://", "mailto:", "#", "/", "computer:")):
                continue
            path = target.split("#")[0]
            if path and not (f.parent / path).exists():
                problems.append(f"{rel}: link ({target}) — no such file")
    return problems


def rules_body(lines: list[str], frontmatter: bool) -> list[str]:
    if frontmatter:   # skip the --- … --- block
        if not lines or lines[0] != "---" or "---" not in lines[1:]:
            return ["(the front matter is not closed with ---)"]
        lines = lines[lines.index("---", 1) + 1:]
    else:             # skip the title
        lines = lines[1:]
    notes = {"The same rules are in `skills/job-search-kit/SKILL.md` (a plugin does not load this file). Change one, copy the change to the other.",
             "The same rules are in `CLAUDE.md` at the kit root (for folder mode). Change one, copy the change to the other."}
    return [l for l in lines if l not in notes]


def check_rules_copies() -> list[str]:
    import difflib
    claude = rules_body((KIT / "CLAUDE.md").read_text(encoding="utf-8-sig").splitlines(), False)
    router = rules_body((KIT / "skills" / "job-search-kit" / "SKILL.md").read_text(encoding="utf-8-sig").splitlines(), True)
    while claude and not claude[0].strip():
        claude = claude[1:]
    while router and not router[0].strip():
        router = router[1:]
    if claude == router:
        return []
    diff = [d for d in difflib.unified_diff(claude, router, "CLAUDE.md", "skills/job-search-kit/SKILL.md",
                                            lineterm="", n=0) if d[:1] in "+-" and d[:3] not in ("---", "+++")]
    return [f"the two copies of the rules differ: {d[:100]}" for d in diff[:10]]


def check_skill_names() -> list[str]:
    skills = {p.name for p in (KIT / "skills").iterdir() if p.is_dir()}
    problems = []
    pat = re.compile(r"skills? `([a-z0-9-]+)`|`([a-z0-9-]+)` skill")
    for f in md_files():
        text = f.read_text(encoding="utf-8-sig")
        if f.name == "SKILL.md" and (not text.startswith("---\n") or "\n---\n" not in text[4:]):
            problems.append(f"{f.relative_to(KIT).as_posix()}: the front matter is not closed with ---")
        for m in pat.finditer(text):
            name = m.group(1) or m.group(2)
            if name not in skills:
                problems.append(f"{f.relative_to(KIT).as_posix()}: skill `{name}` does not exist")
    return problems


def main() -> int:
    problems = check_paths() + check_links() + check_rules_copies() + check_skill_names()
    for p in problems:
        print("ERROR  " + p)
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.path.insert(0, str(KIT / "scripts"))
    from check_pack import friendly_errors
    friendly_errors()
    sys.exit(main())
