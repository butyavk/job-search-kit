#!/usr/bin/env python3
"""Check an English text against the non-native C1 register.

Usage: python3 english_check.py [--me <pack>] [file.txt]   or   echo "text" | python3 english_check.py
Targets: 12–15 words per sentence on average; long words (8+ letters) under 13%; longest sentence under ~30 words;
contractions (don't, I'm): 0; idioms and «AI words»: 0; phrases from the pack's never-say.md: 0.
The pack is found like check_pack.py does: --me, then JOB_SEARCH_ME, then me/ next to the kit or in the working folder.
"""
import os, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_pack import never_claims, never_say_phrases  # noqa: E402

args = sys.argv[1:]
me = None
if "--me" in args:
    i = args.index("--me")
    me = Path(args[i + 1]).expanduser()
    args = args[:i] + args[i + 2:]
if me is None:
    env = os.environ.get("JOB_SEARCH_ME")
    cands = ([Path(env).expanduser()] if env else []) + [Path(__file__).resolve().parent.parent.parent / "me", Path.cwd() / "me"]
    me = next((c for c in cands if (c / "never-say.md").exists()), None)

IDIOMS = ["earn their keep", "connective tissue", "moved the needle", "low-hanging", "deep dive",
          "at the end of the day", "double down", "north star", "bandwidth", "in the weeds",
          "boil the ocean", "tip of the iceberg", "hit the ground running", "wear many hats",
          "that said", "boils down to", "delve", "robust", "seamless", "holistic", "synergy",
          "testament to", "underscore", "pivotal", "landscape", "realm", "crucial", "furthermore",
          "moreover", "cornerstone", "spearhead", "leverage", "passionate", "proven track record", "genuinely"]

t = open(args[0], encoding="utf-8").read() if args else sys.stdin.read()
s = [x for x in re.split(r'(?<=[.!?])\s+', t.replace('\n', ' ')) if len(x.split()) > 1]
w = re.findall(r"[A-Za-z][A-Za-z'\-]*", t)
lw = [x for x in w if len(x) >= 8]
contr = [x for x in w if re.search(r"[a-z]'(t|m|re|ve|ll|d|s)$", x, re.I) and not x.lower().endswith("'s")]
found = [i for i in IDIOMS if re.search(r'\b' + re.escape(i) + r'\b', t, re.I)]
if not s:
    sys.exit("no sentences")
print(f"words: {len(w)}, sentences: {len(s)}")
print(f"average words per sentence: {len(w)/len(s):.1f} (target 12–15)")
print(f"long words: {100*len(lw)/len(w):.1f}% (target under 13%)")
print(f"longest sentence: {max(len(x.split()) for x in s)} words (target under ~30)")
print(f"contractions: {contr or 'none'}")
print(f"idioms and AI words: {found or 'none'}")
if me is not None:
    banned = [p for p, _ in never_claims(me / "never-say.md")] + never_say_phrases(me / "never-say.md")
    def loose(p):  # any run of spaces or line breaks between the words
        return r"(?<!\w)" + r"\s+".join(re.escape(w) for w in p.split()) + r"(?!\w)"
    hits = [p for p in banned if re.search(loose(p), t, re.I)]
    print(f"never-say ({me}): {hits or 'none'}")
    if hits:
        sys.exit(1)
else:
    print("never-say: no pack found (pass --me <pack>)")
