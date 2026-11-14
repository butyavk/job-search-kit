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

## License
By contributing you agree that your contribution is licensed under the MIT license of this repository.
