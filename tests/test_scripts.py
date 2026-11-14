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

    def test_template_is_not_ready(self):
        code, out = run("check_pack.py", "--me", str(KIT / "pack-template"), "--ready")
        self.assertNotEqual(code, 0, out)
        self.assertIn("NOT READY", out)

    def test_maria_is_ready(self):
        code, out = run("check_pack.py", "--me", str(FIX / "maria"), "--ready")
        self.assertEqual(code, 0, out)

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


class PackCheckBreakage(unittest.TestCase):
    """Broken copies of maria that the check must catch."""

    def broken(self, edit):
        d = Path(tempfile.mkdtemp()) / "me"
        shutil.copytree(FIX / "maria", d)
        edit(d)
        return run("check_pack.py", "--me", str(d))

    def test_wrong_heading_level(self):
        code, out = self.broken(lambda d: (d / "blocks" / "20-hiring.md").write_text(
            (d / "blocks" / "20-hiring.md").read_text(encoding="utf-8").replace("#### HIR-O1", "### HIR-O1"), encoding="utf-8"))
        self.assertNotEqual(code, 0, out)
        self.assertIn("a heading that is not a block", out)

    def test_wrong_language_code(self):
        code, out = self.broken(lambda d: (d / "blocks" / "20-hiring.md").write_text(
            (d / "blocks" / "20-hiring.md").read_text(encoding="utf-8").replace("- RU: В Fintrek я перестроила", "- DE: В Fintrek я перестроила"), encoding="utf-8"))
        self.assertIn("«DE:», the profile says RU", out)

    def test_autonomy_rule_needs_date_and_words(self):
        code, out = self.broken(lambda d: (d / "profile.yaml").write_text(
            (d / "profile.yaml").read_text(encoding="utf-8").replace("  rules: []", "  rules:\n  - action: send_followup\n    when: \"x\""), encoding="utf-8"))
        self.assertIn("autonomy rule without", out)

    def test_todo_in_confirmed_block(self):
        code, out = self.broken(lambda d: (d / "blocks" / "20-hiring.md").write_text(
            (d / "blocks" / "20-hiring.md").read_text(encoding="utf-8").replace("hired five engineers in a year.", "hired TODO engineers in a year."), encoding="utf-8"))
        self.assertIn("placeholder", out)

    def test_number_in_native_line(self):
        code, out = self.broken(lambda d: (d / "blocks" / "10-payouts.md").write_text(
            (d / "blocks" / "10-payouts.md").read_text(encoding="utf-8").replace("с 2,1% до 0,4%", "с 2,1% до 0,3%"), encoding="utf-8"))
        self.assertIn("0.3%", out)

    def test_autonomy_rule_indented_deeper(self):
        code, out = self.broken(lambda d: (d / "profile.yaml").write_text(
            (d / "profile.yaml").read_text(encoding="utf-8").replace("  rules: []", "  rules:\n    - action: send_followup\n      when: \"x\""), encoding="utf-8"))
        self.assertIn("autonomy rule without", out)

    def test_recipe_points_to_a_missing_fact(self):
        def edit(d):
            f = d / "recipes.md"
            f.write_text("\n".join(l.replace("`WHO-S1`", "`WHO-S1` `F-99`", 1) if l.startswith("| I01 ") else l
                                   for l in f.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
        code, out = self.broken(edit)
        self.assertIn("F-99", out)

    def test_native_english_variants_need_no_second_line(self):
        for variant in ("English (UK)", "en-GB"):
            d = Path(tempfile.mkdtemp()) / "me"
            shutil.copytree(FIX / "sam", d)
            prof = d / "profile.yaml"
            text = prof.read_text(encoding="utf-8")
            import re
            prof.write_text(re.sub(r"(native:\s*)[^#\n]+", lambda m: m.group(1) + variant, text, count=1), encoding="utf-8")
            code, out = run("check_pack.py", "--me", str(d))
            self.assertEqual(code, 0, variant + out)
            self.assertNotIn("native-language line", out)

    def test_empty_folder_is_not_a_pack(self):
        code, out = run("check_pack.py", "--me", tempfile.mkdtemp())
        self.assertNotEqual(code, 0, out)
        code, out = run("check_pack.py", "--me", str(Path(tempfile.mkdtemp()) / "nope"), "--mark-synced")
        self.assertNotEqual(code, 0, out)
        self.assertNotIn("Traceback", out)

    def test_number_in_words_is_checked(self):
        code, out = self.broken(lambda d: (d / "blocks" / "10-payouts.md").write_text(
            (d / "blocks" / "10-payouts.md").read_text(encoding="utf-8").replace("about two percent of our payouts failed and",
                                                                                  "about five percent of our payouts failed and"), encoding="utf-8"))
        self.assertIn("5%", out)

    def test_vague_plurals_are_not_numbers(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("cp", KIT / "scripts" / "check_pack.py")
        cp = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cp)
        self.assertEqual(cp.word_numbers("hundreds of calls, tens of thousands of lines"), [])
        self.assertEqual(cp.word_numbers("twenty-five engineers, about two percent"), ["25", "2%"])

    def test_cv_numbers_against_facts(self):
        d = Path(tempfile.mkdtemp())
        good, bad = d / "good.txt", d / "bad.tex"
        good.write_text("Fintrek, 2022-2026. Failed payouts from 2.1% to 0.4%.\n", encoding="utf-8")
        bad.write_text("\\item Failed payouts from 2.1\\% to 0.3\\% % a comment with 99\n", encoding="utf-8")
        code, out = run("check_pack.py", "--me", str(FIX / "maria"), "--cv", str(good))
        self.assertEqual(code, 0, out)
        self.assertIn("every number is in facts.md", out)
        code, out = run("check_pack.py", "--me", str(FIX / "maria"), "--cv", str(bad), "--strict")
        self.assertNotEqual(code, 0, out)
        self.assertIn("0.3%", out)
        self.assertNotIn("99", out.split("CV bad.tex")[1].split("\n")[0])

    def test_autonomy_rule_shapes(self):
        def put(rules):
            return lambda d: (d / "profile.yaml").write_text(
                (d / "profile.yaml").read_text(encoding="utf-8").replace("  rules: []", "  rules:" + rules), encoding="utf-8")
        _, out = self.broken(put(" [{action: send_note}]"))
        self.assertIn("one key per line", out)
        _, out = self.broken(put("\n  - when: \"x\"\n    action: send_followup"))
        self.assertIn("autonomy rule without", out)
        _, out = self.broken(put("\n  - action: other (accept invites)\n    since: 2026-11-14\n    said: \"ok\""))
        self.assertIn("covers what no rule may", out)
        code, out = self.broken(put("\n  - action: send_followup\n    since: 2026-11-14\n    said: \"send FU-1 yourself\""))
        self.assertNotIn("autonomy", out)

    def test_schedule_prompt_drift(self):
        import re
        def edit(d):
            (d / "schedules").mkdir(exist_ok=True)
            filled = re.sub(r"<[^<>\n]{1,80}>", "Maria", (KIT / "schedules" / "daily.md").read_text(encoding="utf-8"))
            (d / "schedules" / "daily.md").write_text(filled + "\n8. Submit the forms for Acme.\n", encoding="utf-8")
        _, out = self.broken(edit)
        self.assertIn("differ from the kit's prompt", out)
        self.assertIn("Submit the forms", out)

    def test_cv_noise_is_not_a_claim(self):
        d = Path(tempfile.mkdtemp())
        cv = d / "cv.md"
        cv.write_text("Maria · +49 151 2345678 · maria@example.com · linkedin.com/in/maria\n"
                      "Fintrek, 11/2026. Python 3.11, ISO 27001, on 15 March. Failed payouts from 2.1% to 0.4% (F-04).\n",
                      encoding="utf-8")
        code, out = run("check_pack.py", "--me", str(FIX / "maria"), "--cv", str(cv))
        self.assertIn("every number is in facts.md", out)
        bin_cv = d / "cv.pages"
        bin_cv.write_bytes(b"\x00\x01binary")
        code, out = run("check_pack.py", "--me", str(FIX / "maria"), "--cv", str(bin_cv))
        self.assertIn("cannot read", out)


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
        code, out = run("english_check.py", "--me", str(FIX / "maria"), stdin="I led\nmanagers there.")
        self.assertNotEqual(code, 0, out)  # a hit fails, line breaks do not hide it

    def test_contraction_and_idiom(self):
        _, out = run("english_check.py", stdin="I don't think we should deep dive into it. We leverage data.")
        self.assertIn("don't", out)
        self.assertIn("deep dive", out)

    def test_curly_apostrophes_and_hyphens(self):
        code, out = run("english_check.py", stdin="It\u2019s a deep-dive. I don\u2019t know why we do this.")
        self.assertNotEqual(code, 0, out)
        self.assertIn("It's", out)
        self.assertIn("don't", out)
        self.assertIn("deep dive", out)

    def test_non_english_text_does_not_crash(self):
        code, out = run("english_check.py", "--me", str(FIX / "maria"), stdin="Я руководила командой платежей.")
        self.assertNotIn("Traceback", out)
        self.assertIn("never-say", out)

    def test_idiom_forms_and_other_languages(self):
        code, out = run("english_check.py", stdin="We kept moving the needle with deep dives. That said we shipped.")
        self.assertNotEqual(code, 0, out)
        for x in ("move the needle", "deep dive", "that said"):
            self.assertIn(x, out)
        code, out = run("english_check.py", stdin="Fue crucial y robusto para el equipo de pagos.")
        self.assertEqual(code, 0, out)
        code, out = run("english_check.py", "--me", "/nonexistent", stdin="x")
        self.assertNotEqual(code, 0, out)


class KitCheck(unittest.TestCase):
    def test_kit_is_consistent(self):
        code, out = run("check_kit.py")
        self.assertEqual(code, 0, out)

    def test_rule_copies_must_match(self):
        d = Path(tempfile.mkdtemp()) / "kit"
        shutil.copytree(KIT, d, ignore=shutil.ignore_patterns("site", ".git", "node_modules"))
        f = d / "skills" / "job-search-kit" / "SKILL.md"
        f.write_text(f.read_text(encoding="utf-8") + "\n- An extra rule only here.\n", encoding="utf-8")
        p = subprocess.run([sys.executable, str(d / "scripts" / "check_kit.py")], capture_output=True, text=True)
        self.assertNotEqual(p.returncode, 0, p.stdout)
        self.assertIn("differ", p.stdout)


if __name__ == "__main__":
    unittest.main()
