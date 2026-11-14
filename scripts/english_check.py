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
    if i + 1 >= len(args):
        sys.exit("--me needs the pack folder: --me <path to me/>")
    me = Path(args[i + 1]).expanduser()
    args = args[:i] + args[i + 2:]
if me is None:
    env = os.environ.get("JOB_SEARCH_ME")
    cands = ([Path(env).expanduser()] if env else []) + [Path(__file__).resolve().parent.parent.parent / "me", Path.cwd() / "me"]
    me = next((c for c in cands if (c / "never-say.md").exists()), None)

IDIOMS = ["earn their keep", "connective tissue", "moved the needle", "low-hanging", "deep dive",
          "at the end of the day", "double down", "north star", "have the bandwidth", "no bandwidth",
          "in the weeds", "boil the ocean", "tip of the iceberg", "hit the ground running", "wear many hats",
          "that said,", "boils down to"]
AI_WORDS = ["delve", "robust", "seamless", "holistic", "synergy",
            "testament to", "underscore", "pivotal", "landscape", "realm", "crucial", "furthermore",
            "moreover", "cornerstone", "spearhead", "leverage", "passionate", "proven track record", "genuinely"]

t = open(args[0], encoding="utf-8").read() if args else sys.stdin.read()
t = t.replace("\u2019", "'").replace("\u2018", "'")   # curly apostrophes count as straight ones
s = [x for x in re.split(r'(?<=[.!?])\s+', t.replace('\n', ' ')) if len(x.split()) > 1]
w = re.findall(r"[A-Za-z][A-Za-z'\-]*", t)
lw = [x for x in w if len(x) >= 8]
IS_S = {"it's", "that's", "let's", "there's", "here's", "what's", "who's", "he's", "she's", "where's", "how's"}
contr = [x for x in w if re.search(r"[a-z]'(t|m|re|ve|ll|d|s)$", x, re.I)
         and (not x.lower().endswith("'s") or x.lower() in IS_S)]
def idiom_re(i):  # one word matches its forms too: leverage → leveraging, synergy → synergies
    if " " in i or "-" in i:
        tail = "" if i.endswith(",") else r"\b"
        return r"\b" + r"[\s-]+".join(re.escape(w) for w in re.split(r"[\s-]+", i)) + tail
    stem = re.sub(r"(e|y)$", "", i) if len(i) > 5 else i
    return r"\b" + re.escape(stem) + r"\w*"
found = [i.rstrip(",") for i in IDIOMS if re.search(idiom_re(i), t, re.I)]
ai = [i for i in AI_WORDS if re.search(idiom_re(i), t, re.I)]
native_en = False   # a native English speaker: contractions and idioms are their own register
if me is not None and (me / "profile.yaml").exists():
    mn = re.search(r"^\s*native:\s*([^#\n]+)", (me / "profile.yaml").read_text(encoding="utf-8"), re.M)
    native_en = bool(mn and re.match(r"^(english\b|en(?:[-_][a-z]{2})?$)", mn.group(1).strip().strip("\"'").lower()))
if not t.strip():
    sys.exit("no text")
off = []
if w and s:
    avg, longp = len(w) / len(s), 100 * len(lw) / len(w)
    if not native_en and not 12 <= avg <= 15:
        off.append(f"{avg:.1f} words per sentence")
    if not native_en and longp >= 13:
        off.append(f"{longp:.1f}% long words")
    print(f"words: {len(w)}, sentences: {len(s)}")
    print(f"average words per sentence: {len(w)/len(s):.1f} (target 12–15)")
    print(f"long words: {100*len(lw)/len(w):.1f}% (target under 13%)")
    print(f"longest sentence: {max(len(x.split()) for x in s)} words (target under ~30)")
else:
    print("register numbers: skipped (not English text); never-say still checked")
print(f"contractions: {contr or 'none'}" + (" (native English: fine)" if native_en and contr else ""))
print(f"idioms: {found or 'none'}" + (" (native English: fine)" if native_en and found else ""))
print(f"AI words: {ai or 'none'}")
if me is not None:
    def loose(p):  # any run of spaces or line breaks between the words
        return r"(?<!\w)" + r"\s+".join(re.escape(w) for w in p.split()) + r"(?!\w)"
    hits = [p for p, _ in never_claims(me / "never-say.md") if re.search(loose(p), t, re.I)]
    fillers = [p for p in never_say_phrases(me / "never-say.md") if re.search(loose(p), t, re.I)]
    print(f"never-claim ({me}): {hits or 'none'}")
    print(f"speech fillers from never-say: {fillers or 'none'} (a slip in speech; in writing, cut them)")
else:
    hits = fillers = []
    print("never-say: no pack found (pass --me <pack>)")
bad = bool(hits or ai or (not native_en and (contr or found)))
warn = off + ([f"fillers {fillers}"] if fillers else [])
if bad:
    print("verdict: FIX — " + ", ".join(x for x in (["never-claim phrases"] if hits else []) + (["AI words"] if ai else [])
                                      + (["contractions"] if contr and not native_en else [])
                                      + (["idioms"] if found and not native_en else [])) + " above")
elif warn:
    print("verdict: OK, but check: " + "; ".join(warn) + " (targets 12–15 words, under 13% long words)")
else:
    print("verdict: OK")
sys.exit(1 if bad else 0)
