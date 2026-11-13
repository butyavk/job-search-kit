#!/usr/bin/env python3
"""Check an English text against the non-native C1 register.

Usage: python3 english_check.py file.txt   or   echo "text" | python3 english_check.py
Targets: 12–15 words per sentence on average; long words (8+ letters) under 13%; longest sentence under ~30 words;
contractions (don't, I'm): 0; idioms and «AI words»: 0.
"""
import re, sys

IDIOMS = ["earn their keep", "connective tissue", "moved the needle", "low-hanging", "deep dive",
          "at the end of the day", "double down", "north star", "bandwidth", "in the weeds",
          "boil the ocean", "tip of the iceberg", "hit the ground running", "wear many hats",
          "that said", "boils down to", "delve", "robust", "seamless", "holistic", "synergy",
          "testament to", "underscore", "pivotal", "landscape", "realm", "crucial", "furthermore",
          "moreover", "cornerstone", "spearhead", "leverage", "passionate", "proven track record", "genuinely"]

t = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
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
