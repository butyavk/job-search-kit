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
if args and args[0] in ("-h", "--help"):
    print(__doc__.strip())
    sys.exit(0)
me = None
if "--me" in args:
    i = args.index("--me")
    if i + 1 >= len(args):
        sys.exit("--me needs the pack folder: --me <path to me/>")
    me = Path(args[i + 1]).expanduser()
    if not (me / "never-say.md").exists():
        sys.exit(f"--me {me}: no never-say.md there, so the never-say check cannot run; pass the pack folder")
    args = args[:i] + args[i + 2:]
if me is None:
    env = os.environ.get("JOB_SEARCH_ME")
    cands = ([Path(env).expanduser()] if env else []) + [Path(__file__).resolve().parent.parent.parent / "me", Path.cwd() / "me"]
    me = next((c for c in cands if (c / "never-say.md").exists()), None)

IDIOMS = ["earn their keep", "connective tissue", "move the needle", "low-hanging", "deep dive",
          "at the end of the day", "double down", "north star", "have the bandwidth", "no bandwidth",
          "in the weeds", "boil the ocean", "tip of the iceberg", "hit the ground running", "wear many hats",
          "boil down to"]   # «That said» is matched only where it opens a sentence (OPENERS)
OPENERS = [r"(?:^|[.!?]\s+)That said\b(?!\s+(?:nothing|something|it|that|so|no|yes|a|the)\b)"]   # «That said» opening a sentence, with or without a comma
AI_WORDS = ["delve", "robust", "seamless", "holistic", "synergy",
            "testament to", "underscores", "pivotal", "landscape", "realm", "crucial", "furthermore",
            "moreover", "cornerstone", "spearhead", "leverage", "passionate", "proven track record", "genuinely"]

t = open(args[0], encoding="utf-8").read() if args else sys.stdin.read()
t = t.replace("\u2019", "'").replace("\u2018", "'")   # curly apostrophes count as straight ones
s = [x for x in re.split(r'(?<=[.!?])\s+', t.replace('\n', ' ')) if len(x.split()) > 1]
w = re.findall(r"[A-Za-z][A-Za-z'\-]*", t)
lw = [x for x in w if len(x) >= 8]
IS_S = {"it's", "that's", "let's", "there's", "here's", "what's", "who's", "he's", "she's", "where's", "how's"}
contr = [x for x in w if re.search(r"[a-z]'(t|m|re|ve|ll|d|s)$", x, re.I)
         and (not x.lower().endswith("'s") or x.lower() in IS_S)]
ONLY_PLURAL = {"landscape", "realm", "cornerstone", "testament"}   # «landscaping» is gardening, not an AI word
def word_forms(word):  # move → moved, moving, moves; dive → dives; double → doubled; synergy → synergies
    if len(word) <= 3:
        return re.escape(word) + r"(?:s|es|ed|ing)?\b"
    if word in ONLY_PLURAL:
        return re.escape(word) + r"s?\b"
    stem = re.sub(r"(e|y)$", "", word)
    return re.escape(stem) + r"(?:e|es|ed|ing|s|d|y|ies|ied|ly|ely|ally)?\b"
def idiom_re(i):  # every word matches its forms: «moving the needle», «deep dives», «doubled down»
    if " " in i or "-" in i:
        tail = "" if i.endswith(",") else r"\b"
        words = re.split(r"[\s-]+", i.rstrip(","))
        return r"\b" + r"[\s-]+".join(word_forms(x) for x in words) + ("," if i.endswith(",") else "")
    return r"\b" + word_forms(i)
# Is it English at all? A Spanish or German text has few of these words; its AI-word «hits»
# («crucial», «robusto») are its own language, so only never-say is checked there.
EN_COMMON = {"the", "and", "of", "to", "a", "in", "is", "i", "we", "it", "that", "for", "with", "on", "was", "my"}
OTHER_COMMON = {"los", "las", "que", "por", "para", "con", "una", "del", "der", "das", "und", "ist", "nicht", "mit",
                "les", "des", "est", "une", "pour", "dans", "não", "che", "het", "een", "och", "att", "się", "jest",
                "el", "y", "il", "di", "et", "für", "auf", "von", "bei", "zu", "im", "ich", "ein", "eine", "den",
                "dem", "sich", "wir", "auch", "habe", "wurde", "über"}   # no English homographs (do, die, en, os, la, da)
letters = re.findall(r"[^\W\d_]", t)
non_latin = sum(1 for ch in letters if ord(ch) > 0x024F) / max(len(letters), 1)
en_hits = sum(1 for x in w if x.lower() in EN_COMMON)
other_hits = sum(1 for x in re.findall(r"[^\W\d_]+", t) if x.lower() in OTHER_COMMON)
# CV bullets have few function words, so «English» means: Latin letters and no more of another
# language's common words than of English ones
umlaut_words = len(re.findall(r"\b\w*[äöüßÄÖÜ]\w*\b", t))   # German, even in short CV bullets
is_english = bool(w) and non_latin < 0.2 and other_hits <= en_hits and umlaut_words < max(2, len(w) // 40)
found = [i.rstrip(",") for i in IDIOMS if re.search(idiom_re(i), t, re.I)] if is_english else []
found += ["that said"] if is_english and any(re.search(o, t) for o in OPENERS) else []
ai = [i for i in AI_WORDS if re.search(idiom_re(i), t, re.I)] if is_english else []
native_en = False   # a native English speaker: contractions and idioms are their own register
if me is not None and (me / "profile.yaml").exists():
    mn = re.search(r"^\s*native:[ \t]*([^#\n]*)", (me / "profile.yaml").read_text(encoding="utf-8-sig"), re.M)
    nv = mn.group(1).strip().strip("\"'").lower() if mn else ""
    native_en = bool(nv and not nv.startswith("<") and re.match(
        r"^(?:(?:british|american|australian|canadian|irish|us|uk)\s+)?english\b(?!\s*(?:,|and|\+|/))|^en(?:[-_][a-z]{2})?$", nv))
if not t.strip():
    sys.exit("no text")
off = []
if w and s and is_english:
    avg, longp = len(w) / len(s), 100 * len(lw) / len(w)
    if not native_en and not 12 <= avg <= 15:
        off.append(f"{avg:.1f} words per sentence")
    if not native_en and longp >= 13:
        off.append(f"{longp:.1f}% long words")
    print(f"words: {len(w)}, sentences: {len(s)}")
    tgt = "" if native_en else " (target 12–15)"
    print(f"average words per sentence: {len(w)/len(s):.1f}{tgt}")
    print(f"long words: {100*len(lw)/len(w):.1f}%" + ("" if native_en else " (target under 13%)"))
    print(f"longest sentence: {max(len(x.split()) for x in s)} words (target under ~30)")
else:
    print("register numbers: skipped (not English text); never-say still checked")
    sents = [x for x in re.split(r"(?<=[.!?])\s+", t.strip()) if len(x.split()) > 1]
    if sents:   # the length is still worth seeing in any language
        print(f"longest sentence: {max(len(x.split()) for x in sents)} words (under ~30 is easier to say)")
print(f"contractions: {contr or 'none'}" + (" (native English: fine)" if native_en and contr else ""))
print(f"idioms: {found or 'none'}" + (" (native English: fine)" if native_en and found else ""))
print(f"AI words: {ai or 'none'}")
if me is not None:
    def loose(p):  # any run of spaces or line breaks between the words
        return r"(?<!\w)" + r"\s+".join(re.escape(w).replace("'", "['’]") for w in p.split()) + r"(?!\w)"
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
