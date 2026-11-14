"""Regression tests for the kit's scripts, on made-up packs in tests/fixtures/.

maria — native Russian, manager track, three stories, a never-say row.
sam   — native English (no second line), engineer track, one story, no facts.

Run: python3 -m unittest discover -s tests
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
FIX = KIT / "tests" / "fixtures"


def run(script, *args, stdin=None, env=None):
    p = subprocess.run([sys.executable, str(KIT / "scripts" / script), *args], input=stdin,
                       capture_output=True, text=True, env={**os.environ, **(env or {})})
    return p.returncode, p.stdout + p.stderr


class PackCheck(unittest.TestCase):
    def test_empty_template_has_no_recipes(self):
        code, out = run("check_pack.py", "--me", str(KIT / "pack-template"))
        self.assertEqual(code, 0, out)
        self.assertIn("with a recipe: 0", out)          # template drafts (ASK-, LOG-) do not count
        self.assertIn("draft: X01, X02, X03", out)       # logistics linked to LOG- drafts
        self.assertNotIn("project copy", out)            # no project copy → no line about it
        self.assertNotIn("EN register", out)             # placeholders do not count

    def test_maria_manager_russian(self):
        code, out = run("check_pack.py", "--me", str(FIX / "maria"))
        self.assertEqual(code, 0, out)
        self.assertIn("with a recipe: 4", out)
        self.assertIn("(manager)", out)
        self.assertIn("stories with a whole S block: 3/3", out)
        self.assertNotIn("numbers not in facts.md", out)

    def test_sam_english_engineer(self):
        code, out = run("check_pack.py", "--me", str(FIX / "sam"))
        self.assertEqual(code, 0, out)
        self.assertNotIn("native-language line", out)   # native English needs no second line
        self.assertIn("role ◆: 0/3 (engineer)", out)
        self.assertIn("numbers not in facts.md: 300, 6%", out)

    def test_pack_found_through_env(self):
        with tempfile.TemporaryDirectory() as d:
            code, out = run("check_pack.py", env={"JOB_SEARCH_ME": str(FIX / "sam")})
            self.assertEqual(code, 0, out)

    def test_missing_native_line_is_an_error(self):
        with tempfile.TemporaryDirectory() as d:
            me = Path(d) / "me"
            shutil.copytree(FIX / "maria", me)
            f = me / "blocks" / "20-hiring.md"
            f.write_text("\n".join(l for l in f.read_text(encoding="utf-8").splitlines()
                                   if not l.startswith("- RU:")), encoding="utf-8")
            code, out = run("check_pack.py", "--me", str(me))
            self.assertNotEqual(code, 0, out)
            self.assertIn("no native-language line", out)

    def test_wrong_number_is_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            me = Path(d) / "me"
            shutil.copytree(FIX / "maria", me)
            f = me / "blocks" / "10-payouts.md"
            f.write_text(f.read_text(encoding="utf-8").replace("to 0.4% between", "to 0.3% between"), encoding="utf-8")
            code, out = run("check_pack.py", "--me", str(me))
            self.assertIn("PAY-R1: numbers not in facts.md: 0.3%", out)

    def test_sync_marks(self):
        with tempfile.TemporaryDirectory() as d:
            me = Path(d) / "me"
            shutil.copytree(FIX / "maria", me)
            run("check_pack.py", "--me", str(me), "--mark-synced")
            _, out = run("check_pack.py", "--me", str(me))
            self.assertIn("project copy: in sync", out)
            (me / "facts.md").write_text((me / "facts.md").read_text(encoding="utf-8") + "\n", encoding="utf-8")
            _, out = run("check_pack.py", "--me", str(me))
            self.assertIn("changed since the last copy", out)


class EnglishCheck(unittest.TestCase):
    def test_register_numbers(self):
        code, out = run("english_check.py", stdin="I build small teams. They ship often.")
        self.assertEqual(code, 0, out)
        self.assertIn("contractions: none", out)

    def test_never_say_from_the_pack(self):
        _, out = run("english_check.py", "--me", str(FIX / "maria"),
                     stdin="I led managers at Fintrek. So, yeah, we did fine.")
        self.assertIn("'led managers'", out)
        self.assertIn("'so, yeah'", out)

    def test_contraction_and_idiom(self):
        _, out = run("english_check.py", stdin="I don't think we should deep dive into it. We leverage data.")
        self.assertIn("don't", out)
        self.assertIn("deep dive", out)


class KitCheck(unittest.TestCase):
    def test_kit_is_consistent(self):
        code, out = run("check_kit.py")
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main()
