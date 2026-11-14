# Contributing to Job search kit

Help is welcome: a clearer rule in a skill is as useful as a new command.

## Report a problem
Open an [issue](https://github.com/butyavk/job-search-kit/issues) and say what you ran (`/start`, `/find`, …), what Claude did, and what you expected. Never paste your pack: facts, money and contacts stay private — describe the problem with made-up data.

Useful reports:
- **A step that stalls** — a command that asks for a file that is not there, or a skill that sends Claude to a section that does not exist.
- **A rule that does not hold** — a number in the docs that your search contradicts, a source that stopped working.
- **The Russian text** reads unnaturally or does not match the English.

## Change the kit
- The kit holds **no personal data**. A change that needs a fact about a real person belongs in a pack (`me/`), never here. `.gitignore` blocks `me/`.
- Skills, commands and templates are in English; the README and the guide also have Russian versions — change both.
- `CLAUDE.md` and `skills/job-search-kit/SKILL.md` carry the same rules (folder mode and plugin mode): change one, copy the change to the other.
- Before a pull request, run the checks the CI runs:
  ```bash
  cp -r pack-template /tmp/me && python3 scripts/check_pack.py --me /tmp/me
  echo "I build small teams. They ship often." | python3 scripts/english_check.py
  python3 scripts/check_kit.py   # references, links, the two copies of the rules, skill names
  python3 -m unittest discover -s tests
  claude plugin validate .      # if you have Claude Code
  ```
- A change users will notice bumps the version in `.claude-plugin/plugin.json` (installed plugins update only on a new version) and gets a `## <version>` entry in `CHANGELOG.md`; CI checks the two match. The maintainer publishes it with Actions → release (a tag, the notes, one zip per skill for claude.ai).
- A rule that came from a real search keeps its number and where it came from (see `docs/how-it-works.md`).

## Habits that keep old mistakes from coming back
Past reviews found the same few kinds of error again and again; each change is checked against them.
- **One rule, one place.** A check used by two scripts lives in one function (`phrase_pattern`, `native_is_english`, `yaml_scalars`, `friendly_errors` in `check_pack.py`); text that must exist twice (the two rule copies, the three cron lines, an English page and its Russian copy) has a test that compares the copies.
- **Read it the way the reader does.** A check on YAML follows indentation and refuses keys set twice; a check on a path resolves it (links, `..`, letter case on macOS) instead of comparing the text.
- **Allow, do not block.** Where a check guards something, it names what is allowed (actions, settings keys, versions, value forms) and refuses the rest; a default that cannot tell refuses.
- **Normalise both sides.** Apostrophes, letter case, Unicode forms and invisible characters are folded the same way in the pattern and in the text.
- **Match whole words.** A pattern that guards against a word also has a test with innocent text around it («after I submitted», «signal»).
- **Every claim has a test.** A line in the CHANGELOG, a README or a docstring that says what a script does has a test that runs the script, not one that reads its source.
- **No traceback for a user.** Broken input (not UTF-8, a folder or a broken link where a file should be) gives one line naming the file; every script calls `friendly_errors()`.
- **A test must be able to fail.** A new test is first run against the code without the fix and seen failing; break the code on purpose once in a while and check that a test notices.
- **Before a release:** run the new scripts on a real pack and compare their warnings with the last release's (`git worktree add /tmp/old v<last>` and `diff` the `WARN`/`ERROR` lines); a new warning is either a real finding or a false positive to fix first.

## License
By contributing you agree that your contribution is licensed under the MIT license of this repository.
