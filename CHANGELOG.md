# Changelog

## 1.5.0 — 2026-11-14

Safety (a fifth review: red team, claude.ai, a German and a Russian newcomer, docs and scripts)
- Scheduled runs: the three cron lines are written out in full; each may write only today's output file (`$(date +\%F)`), reads stay in the search folder and the kit (`Read(…)` rules also cover Glob and Grep, so the bare `Glob,Grep` allows are gone), `--no-chrome`, `< /dev/null`, and in plugin mode always `--plugin-dir`.
- `check_pack.py --schedules` also refuses the search folder's `.claude/settings*.json` with hooks, environment, helpers or MCP servers; the read-only tracker run from a temporary folder, from inside the search folder or through `..`, a tracker-mcp older than 0.8.3, and relative or temporary `TRACKER_CONFIG` / `TRACKER_BACKUP_DIR`. It warns about a parent folder's CLAUDE.md and about lines besides `@kit/CLAUDE.md` in the search folder's own.
- `values.yaml`: each key has its form (a name has letters only; the time zone is an IANA zone or UTC±H; no sentences or code names); a key set twice, or the file as a link, stops the run; values are NFC-normalised.
- Autonomy rules: the action is only `send_followup` or `send_note` (`other (…)` is gone); the whole entry except the candidate's quote is scanned for what no rule may cover, after look-alike letters and invisible characters are normalised.
- CLAUDE.md §5: right before each send Claude shows the recipient's address (or the form's link) and the first line, even for named items.
- Desktop-app tasks: the «ask» list covers every tool that does more than read, with the tracker's write tools by name; drafts stay in the daily summary, not in the mail; a pasted prompt is re-pasted after a kit update; a pack kept only in a claude.ai project gets no scheduled runs.
- The plugin hook prints the pack's absolute folder and the plugin's folder (it changes with every version); paths are compared as written and resolved; `/proc`, `/dev` and `/sys` are never a pack's recorded path.
- tracker-mcp 0.8.3 or later, pinned inside 0.8 (`==0.8.x` or `>=0.8.x,<0.9`), for the read-only entry (locked writes, per-tracker audit and backups, confined undo).
- A second check of 1.5.0 before release closed more holes: project settings may hold only `permissions.deny` and `permissions.ask` (allows, extra folders, modes, plugins and marketplaces are refused too); autonomy rules are read the way a YAML reader takes them, so a sibling key after a `said: |` quote, a duplicate key, a second `autonomy:` or a comment line cannot hide a rule, and look-alike letters from other scripts are refused outside `said`; the cron lines also deny `Edit(./.git/**)`; temporary-folder checks ignore letter case (macOS); the tracker file itself may not sit in a temporary folder; values name things — a verb that tells a run what to do, a sentence or an unknown time zone stops the run (zones are checked against the system's zone list; UTC+5:30 and names in Devanagari pass); the hook refuses disguised `/proc` paths (`//proc`, `/./`, `/../`); warnings also cover `.claude/CLAUDE.md`, `CLAUDE.local.md`, project agents, commands and skills, and a CLAUDE.md inside `companies/`, `applications/` or `me/`.

Fixed
- `check_pack.py`: files saved with a BOM are read; a file that is not UTF-8, a folder in a file's place or a damaged sync manifest gives «cannot read …» instead of a traceback; `native:` is read on its own line, and «English» means a value that starts with it (not «Russian, English»); the never-say and never-claim checks also run on the native-language line and the CV, allow any spacing and curly apostrophes, keep short parts (CTO, VP, PhD) and read «a» or «b» rows; numbers with units (10x, 150ms, 40h) are checked, clock times and UTC offsets are not; German (Mio., Mrd., Tsd.) and Indian (lakh, crore, LPA, 48,00,000) scales; the money floor is read with scales and words too; German link words in DANGLING; Indian languages in the language codes.
- `--cv`: a scanned PDF says it has no text; .docx line breaks, headers, footers, footnotes and endnotes; UTF-16 files, with or without the mark; HTML block tags become lines; only the contact itself (an address, a link, a phone) is dropped, not its whole line; `\textbf{45}` in TeX keeps its number; HTML without styles, scripts and entities; each unknown number is shown with its line.
- `check_pack.py`: autonomy conditions such as «my application thread», «after I submitted» or «no signal» are not refused any more; versions of Kafka, Redis, OAuth, Spring Boot, C#, macOS, WCAG and others are not amounts; a broken link or a manifest of the wrong shape gives a message, and a non-UTF-8 file is named.
- `english_check.py`: `--help`; never-say phrases match with either apostrophe; German text is told by its common words and umlauts; the longest sentence is shown for any language; «That said nothing» is not the opener.
- `check_kit.py`: a skill file whose front matter is not closed.
- Onboarding: `paths.pack` is written in step 0; company folders next to `me/`; one master CV per application language; statuses stay in English for other languages; with an interview within five days the processes under way are tracker rows in session 1 and a coding trainer starts on day 1. The tracker skill has a recipe for processes under way and, for a hand-kept table, the status list and the +10/+14/30 rule.
- Templates: LOG-2 (work authorization) and LOG-3 (contract form) blocks and the X02 recipe; offer rows for net pay, the tax regime and the work permit; a three-day row in the learning sheet; a manager's round in the design card; «the interview language» instead of «English» in prep, live coding, the prep tabs and the debrief.
- Docs: claude.ai steps copy the project files to a writable folder and run the scripts with `python3`; the project-files zip carries the skills' own files; moving to Claude Code covers « (1)» duplicates, `paths.pack` and the `@kit/CLAUDE.md` line; forms are «submitted only on your yes» on the site and «never under a rule» in the autonomy pages and README; the site's «Edit page» links point at the real files; German and Spanish conventions in outreach; never padding a two-page CV; Type 3 fonts; a stack the trainers do not cover goes to `company-trainer`; `/start` reads in order.

## 1.4.2 — 2026-11-14

Changed (a fourth review)
- A scheduled run's prompt is always the kit's: `scripts/schedule_prompt.py daily|weekly|monthly` builds it at the start from the kit's file and `me/schedules/values.yaml` (name, roles, city, time zone, language; short phrases only; `<kit>` filled by the script; run-time slots such as `<date>` left as they are). No prompt file in the pack is read, so a kit update reaches the runs by itself and an edited file cannot change what they do. `check_pack.py --schedules` checks the values, refuses an old filled copy in the pack, and checks the read-only entry strictly (an absolute uvx path, a `tracker-mcp` version range, no other keys).
- The cron line no longer denies `Edit(./*)`, which blocked the run's own summary; it denies `Edit(./CLAUDE.md)` instead, and quotes its paths.
- Autonomy rules: the action is `send_followup`, `send_note` or `other (…)`; anything else is an error, and `checks:` is scanned too.
- The plugin hook warns unless the profile records this pack by its absolute path.

Fixed
- `check_pack.py`: names glued to digits (37signals, 2FA, 3rd) and ratios (80/20, 24/7) are not amounts to check against `facts.md`; nested keys under `money:` (the template's own layout); «1,234,567 users» is a number again (colours are skipped only in TeX); PostgreSQL, Terraform, Rust, TypeScript, Spark, Windows and Java versions.
- `english_check.py`: «do», «die», «en», «os», «la» no longer make English look like another language; -ly forms (seamlessly, crucially, passionately) are caught; «That said» only where it opens a sentence.
- Docs: forms are submitted only when the candidate names them (README, install pages, CLAUDE.md §5); withdrawals after the signed contract (site prep pages); the tracker extension's «Confirm only in the app's dialog» in the tracker skill; the references message says «late stages».

## 1.4.1 — 2026-11-14

Safety (a third red-team review and a verification of 1.4.0)
- Every Claude Code scheduled run starts with `check_pack.py --schedules`, before Claude: it stops the run when a filled prompt is not the kit's prompt with its `<…>` filled in (an added or changed line, a deleted safety line, a sentence hidden in a value — values are short phrases now), when `tracker-ro.mcp.json` is not exactly the read-only server, or when a run file is dated in the future. `/today` runs the same check first.
- Cron runs: `--setting-sources project` (the candidate's user settings and their allows stay out), reads limited to the search folder and the kit, and the search folder's own files, the kit, company folders and applications denied for edits. The weekly host list is described as a narrowing, not a seal.
- Desktop-app tasks: drafts, calendar events with guests, Drive sharing and Chrome site permissions join the «ask» list; the tracker extension's «Confirm only in the app's dialog» (tracker-mcp 0.8.1).
- No autonomy rule covers submitting application forms (CLAUDE.md, `/apply`, `check_pack.py`). A message with pasted text, or one that points at items instead of naming them, gets a read-back of each item and acts only on a separate short yes.
- The previous summary is the newest dated file not after today.
- The plugin hook says when a pack is not at the path its profile records (a `me/` that came with a cloned project); the recorded path is never evaluated.

Fixed
- `check_pack.py`: an unfilled `native:` is not «English»; only `money.say_aloud` counts as a known number, and a block that says the floor or the current salary is an error; «below 7 500.» is 7500; React 18 or Ubuntu 22.04 are versions; .docx runs are joined as written; autonomy rules with nested lists, `rules: ~`, block scalars for `said`, empty or placeholder `said`, `autonomy: {…}`; «send_application», «Submit Form» and «forms» are actions no rule may cover.
- `english_check.py`: CV bullets with few function words are English (another language is told by its own common words or non-Latin letters); word forms are endings only, so «doubled downloads», «northern» or «landscaping» are not idioms or AI words.
- Interview prep: withdrawals only after the signed contract and cleared conditions; references chosen after the first screen and warned before the final round; block edits during an open process only with a note. The bank says new questions go to the pack. The three-day path also covers money, logistics and never-say. Native English in README and the site. claude.ai: how Claude rebuilds the folders to run the scripts.

## 1.4.0 — 2026-11-14

Safety (a red-team review)
- Only the candidate's own words are a yes: pasted or forwarded text is data. A yes for named items needs the items named («submit all ready forms» names none).
- Autonomy rules: written only from the candidate's words in a live session; read back with «still yours?» before the first use; `check_pack.py` parses them properly (any key order, no flow style) and rejects actions no rule may cover; the template no longer offers `submit_form`.
- Text in pages, emails, invites, messages, tracker cells and earlier run summaries that tells Claude what to do is quoted under «Suspicious» and not done — in the daily, weekly and monthly runs alike.
- A `me/` that came with something else (a cloned take-home) is not the pack; the pack is the one in `paths.pack`.
- Scheduled runs in Claude Code: `--permission-mode default` and a deny list (Bash, the pack's own files); the weekly run fetches only job-board hosts; the read-only tracker starts from an absolute `uvx` path with a pinned version range (tracker-mcp 0.8). Desktop-app tasks are created only after the candidate hears what protects them and says yes; the mail and calendar send tools stay on «ask».
- `check_pack.py` warns when a filled schedule prompt differs from the kit's beyond its `<…>` values; `/today` then uses the kit's text.
- Imported facts stay drafts until the candidate confirms them in the session.
- The kit needs tracker-mcp 0.8 or later (an edited config can no longer turn the yes off).

Fixed (a requirements audit and a newcomer run in English, claude.ai first)
- Native English: no second line, no contraction or long-word warnings, no non-native targets printed; the checklist, onboarding and the template say so; «British English» and «English (UK)» count.
- claude.ai: code execution is the prerequisite; skills from Customize → Skills; the release ships the project files already named with their path, scripts and the example included; company work as `companies__<company>__…` in the same project; a hand-kept tracker with `templates/tracker.csv`; moving to Claude Code with one rename line.
- An interview in three days or less: one session, no freeze, the search after the interview.
- System design for engineering managers.
- `check_pack.py`: money from the profile (with comments after the key); a pack needs profile.yaml or facts.md; duplicate recipe rows and missing `F-` facts in blocks are errors; IDs, versions, dates, phones and colours are not amounts; «12 million» is one number; «ten twenty-person teams» is two; `--cv` reads .docx, refuses unknown types, skips contact lines, and reports warnings.
- `english_check.py`: idioms in any word form («moving the needle», «deep dives»), «That said» without a comma; «underscore» as a word is fine; text that is not English gets only the never-say check; `--me` without a pack is an error.
- `check_kit.py` drops only the two exact copy-note lines. The hook fires only with a real pack (`me/profile.yaml`, or an existing `JOB_SEARCH_ME`).
- The import line is appended to an existing `CLAUDE.md`, never overwriting it. Plugin-safe paths in CLAUDE.md §7 and in the schedule prompts (`<kit>`).
- Offers: pension, holidays, notice both ways, conditional offers, restrictive covenants, IR35-type status; withdrawals only after the contract is signed and its conditions cleared. References are warned before the final round.
- Debrief: block edits during an open process only with a note; new questions to `me/questions-extra.md` everywhere. Time zones as IANA names. `uvx tracker-mcp calendar`.

## 1.3.2 — 2026-11-14

Fixed
- `--cv` on a .tex reads the document body only and skips layout sizes (0.15in, 0.97\textwidth).
- Number words: «hundreds of», «tens of thousands» are not numbers; facts written as €1M, 10K or 2 млн count as the whole number.

## 1.3.1 — 2026-11-14

Added
- GitHub releases: Actions → release publishes the version with its notes and one zip per skill for claude.ai (the install pages point there). CI checks that the plugin version has a CHANGELOG entry and that the hook runs.
- `check_pack.py --cv <CV>`: every number in the CV (.tex, .md, .txt, .html, .pdf) must be in `me/facts.md`; used in tailoring, onboarding and `/review`.
- Numbers written as words in blocks («five percent», «twenty-five») are checked against `me/facts.md`; a rounded fact counts («about two percent» = 2.1%).
- CONTRIBUTING: the checks to run and how a version is published.

## 1.3.0 — 2026-11-14

Fixed (three independent reviews: requirements audit, a newcomer run in Spanish, tracker-mcp 0.7)
- Folder mode: `echo '@kit/CLAUDE.md' > CLAUDE.md` in the search folder (README, site, `/start` writes it), because Claude Code does not load a CLAUDE.md in a subfolder; a skill named in the kit is `<kit>/skills/<name>/SKILL.md` when it is not loaded as a skill.
- Plugin: a SessionStart hook in a search folder (a `me/` or `JOB_SEARCH_ME`) points the session to the kit's rules first.
- Scheduled runs in Claude Code load only the read-only tracker from `me/schedules/tracker-ro.mcp.json` with `--strict-mcp-config`, and may write only into `me/runs/` (daily, monthly) or `me/search/` (weekly); lines for all three, with full paths, the log and the macOS note. A live `/today` uses the read-write tracker. Desktop-app tasks: what protects them and what does not, said plainly.
- A yes in the current message for named items is the yes for exactly those; the forms skill, `/apply` and CLAUDE.md now say the same.
- New interview questions go to the pack (`me/questions-extra.md`, IDs `Q01`…), not the kit's bank; `check_pack.py` reads both.
- `check_pack.py`: real placeholders only (not the template's examples in backticks or «»; headings count); money numbers from the profile; thousands with a dot (65.000); «3 100-person» is two numbers; autonomy rules at any indentation; recipes pointing to a missing `F-` fact; English variants (English (UK), en-GB) need no second line; Spanish and other language names; Spanish openers; an empty folder or a missing one with `--mark-synced` is an error; `--ready` needs profile and facts.
- `english_check.py`: curly apostrophes, it's/that's/let's; hyphenated idioms; no false hits on «network bandwidth» or «the alert that said»; AI words separate from idioms; speech fillers are a warning; a warning when sentence length or long words are off target; native English candidates are not held to the non-native register; no crash on non-English text or a bare `--me`.
- `check_kit.py`: the two copies of the rules must be the same text in the same order; relative Markdown links are checked.
- The pack template's native line is `XX:` (any language), not `RU:`.
- Onboarding asks for processes already under way; a plain-text CV gets an editable master; a reply from a company clears or moves its follow-up; `/today` runs the filled copy from `me/schedules/`.
- Follow-up wording matches the tracker's config (`close_stale` for silent rows); Source and Gate columns proposed at setup and measured in `/review`, with a small-sample caveat.
- Country boards: how to find them for any country; the «not worth the time» list is marked as market-specific. References are chosen after the first screen.
- Offer: payments a year; tasks turned off by the candidate; the accepted offer in the tracker. Mocks write to the sheet's «Marks».
- claude.ai: kit files uploaded with their path in the name (`commands__debrief.md`); the site's autonomy pages carry the consent and tracker rules.

## 1.2.3 — 2026-11-14

Changed (tracker-mcp 0.7)
- The kit needs tracker-mcp 0.7 or later; the tracker setup checks the version.
- Scheduled runs use a second, read-only tracker entry `tracker-ro` (`--read-only`): the server previews and refuses every write. The cron line allows only that entry.
- `undo_last_write` steps back one write at a time, not only the last one; it stops at a hand edit.

## 1.2.2 — 2026-11-14

Fixed (independent review of the candidate's path and simplicity)
- No slash commands in folder mode and claude.ai: «/start» or its words make Claude read `commands/start.md`; `commands/` is in the claude.ai upload list.
- `/start` puts the search first: CV, frame, tracker and the first `/find` in session one; stories over the next sessions. Proposed role titles come with live postings.
- A close interview: 3–4 whole stories and the pitch in session one, details in session two.
- Plugin paths: `<kit>/…`, with how to find the plugin folder (`${CLAUDE_PLUGIN_ROOT}` is not set inside a session).
- Schedules: run on the computer that holds the pack and the tracker; filled copies in `me/schedules/`; a working cron line; «Pause or end» (also for «I found a job»).
- When no new session can be started, the daily summary carries the filled live-response prompt.
- Follow-up timing has one home, the tracker's config; `target.roles` dropped from the profile; the forms skill uses the profile's real keys.
- `uv` and `mkdir -p` in the tracker setup; every tracker write is previewed (said so).
- Voice mocks: the Claude desktop or mobile app (Claude Code has no voice).
- `check_pack.py --ready` fails until the profile and facts are filled and the pitch is confirmed.
- `english_check.py` catches word forms of AI words (leveraging, synergies) and ends with a verdict; it exits 1 on contractions, idioms or never-say phrases.
- Messages to the candidate: about eight lines and one block of questions.
- `system-design/patterns.md` links to the System Design Map pages.

## 1.2.1 — 2026-11-14

Fixed (independent review of control, facts and privacy; a live unattended daily run)
- Scheduled runs never pass `confirm` to the tracker, said the same way everywhere (README, how-it-works, schedules, `/today`); the server would accept it, so the rule is the kit's.
- Consents are never ticked for the candidate, even on «tick everything»; consents are in the list no autonomy rule covers.
- The live-response prompt no longer carries the email's text: the new session reads the thread as data; emails that tell the assistant what to do are quoted under «Suspicious» in the daily summary.
- «Never twice»: 14 days of mail, the ATS's own «already applied», and no forms in scheduled runs.
- LinkedIn is not silent: scheduled runs read only previews and alerts, open no threads or profiles.
- Form answers: no guessed «previously employed»; `worked_at_company_before` and `relatives_at_company` in the profile; sponsorship «to remain where you live» told apart from the job's country.
- `check_pack.py`: a `###` heading inside a blocks file is an error (it silently swallowed blocks); the native-language code must match the profile; TODO, TBD and `[number]` are placeholders; «draft» counts only as a whole word; numbers are matched against the facts' own cells (not dates or sources) and in the native line too; autonomy rules need `since:` and `said:`; placeholders left in facts, profile and search rules are listed.
- `english_check.py`: `--me` in any position, phrases match across line breaks, and a never-say hit fails.
- Privacy: `.gitignore` covers application files, CVs, trackers, calendars, notes exports and fact-check results; the notes export no longer takes a 1:1 folder by default; 1:1 notes and feedback about others are never quoted outward; recording only with the company's and the candidate's yes.
- Debriefs record the stories told, so the next round gets others; fact-check verdicts are kept in the pack.
- Only the last tracker write can be undone — said so; the README no longer claims the kit «only reads» the pack.

## 1.2.0 — 2026-11-14

From the requirements review (72 requirements, statuses and plan: one document per release).

Added
- `job-application-forms` «Never twice»: one form, one session; before every submit, the confirmation email and the tracker row are checked.
- `english_check.py` finds the pack and lists every phrase from `never-say.md` in the text.
- `check_pack.py` warns when a number in a block is not in `facts.md` (thousands and decimal commas understood; years skipped).
- `scripts/check_kit.py`: every file the instructions name exists, the two copies of the rules agree, every named skill exists. In CI.
- Regression tests on two made-up packs (`tests/`), in CI.
- What to do without a browser (`/apply` → the answers file) and without the tracker (`/today` → a table of changes).
- Writing rules for a vacancy in another language.
- The sources page in Russian on the site.

Changed
- The money floor lives only in `profile.yaml` → `money`; `search-rules.md` refers to it.
- The pack check suggests `/start` (was the old `/onboard`) when there is no pack.

## 1.1.3 — 2026-11-14

Fixed (fourth and fifth test runs: a tracker from `tracker-mcp new`, applications, a rejection, follow-ups, the funnel; a stage from the invitation to a debrief with a new fact)
- The daily check no longer writes to the tracker on its own: the server writes only after the candidate's yes, so a scheduled run lists dry runs in the summary, as the weekly and monthly runs already did.
- Silence: `stale_applications` takes the frame's «No answer» days, and a row with a follow-up still due is not closed as silent.
- Where company work lives in folder mode: `companies/<company>/` next to `me/`; a likely question without a story is a gap to compose, not a sheet row.
- How to update the plugin: the real commands (`claude plugin marketplace update`, then `claude plugin update`), now in both READMEs.

## 1.1.2 — 2026-11-14

Fixed (third test run: a real vacancy from a company board, through the gate to the form)
- Standing form answers live in one place, `profile.yaml`, with new keys for common questions (post-employment restrictions, primary language, open-source links, accessibility); `search-rules.md` keeps only wording.
- `tailoring-cv` stops when there is no master CV and sends to onboarding, instead of building from blocks.
- `job-search`: a yes/no «are you located in …» form question is a geography zero.
- claude.ai: Claude writes project files itself where it has a tool for them.

## 1.1.1 — 2026-11-14

Fixed (found in two test runs with made-up candidates)
- Onboarding: the pack goes to the search folder, never inside the plugin's folder, which is replaced on every update.
- `check_pack.py`: questions for the interviewer (Z) count as covered only by a confirmed `ASK-` block, not a template draft; draft and placeholder blocks no longer count towards the English register numbers; no line about a project copy for candidates who keep none.
- The pack template links the logistics questions X01–X03 to the `LOG-` blocks.
- The learning sheet says which language the first sentences are learned in; the debrief sends new questions and weak answers into the next stage's sheet and drill.

## 1.1.0 — 2026-11-14

Added
- Learning what you prepared: step «Learn» in `interview-prep` and `templates/learning-sheet.md` — a one-page map (question → first sentence → story), story anchors in four steps, recall aloud on a timer in random order, a mark per answer, only the misses again, a drill plan by days.
- `/mock drill`: the sheet's questions in random order, ✓ / ~ / ✗ against the anchor, the marks into the sheet.
- `/prep` now ends with the learning sheet and how to start.
- Take-home tasks and the offer in `interview-prep`, with `templates/offer.md`: read the offer whole, compare with the floor and other processes, no decision in the moment, a counter with one number, the contract against the offer, then withdrawals, references, schedules paused, a retro.
- Onboarding: «If an interview is close» — the stories for that stage first, then `/prep`; the rest after the interview.
- Onboarding: the master CV (an editable source, or a PDF rebuilt once and checked line by line), the LinkedIn profile, and a mail label for the daily check.
- A site on GitHub Pages, in English and Russian, with a page on preparing for an interview — https://butyavk.github.io/job-search-kit/

## 1.0.1 — 2026-11-13

Added
- `skills/job-search/sources.md`: every source of vacancies — LinkedIn (alerts, guest API, logged-in search, People), company boards through ATS APIs (Ashby, Greenhouse, Lever, Workable, Teamtailor, Pinpoint, BambooHR, Breezy), job sites (hiring.cafe, Himalayas, Jobicy, RemoteOK, We Work Remotely, Working Nomads, HN «Who is hiring», levels.fyi, Wellfound, YC, Welcome to the Jungle), country boards, what is not worth the time, and how each one reads.
- README: what to connect and what each connection gives.

Changed
- Posting age is a risk and a place in the queue, not a filter: fresh posts first, older than ~14 days checked for signs of life, older than 90 with none goes last.
- Timing: Monday to Thursday, Tuesday best, the company's morning; no limit on the number of packages.
- The candidate can mark gate zeros that never block (managing managers, another stack in a manager role, a remote country list).

## 1.0.0 — 2026-11-13

The whole search with Claude, from the search frame to the offer.

Added
- Nine commands: `/start`, `/find`, `/people`, `/apply`, `/today`, `/prep`, `/mock`, `/debrief`, `/review`.
- Thirteen skills: the entry point with the autonomy rules, onboarding, answer blocks, vacancy search and the screener gate, outreach, the tracker (through tracker-mcp), CV tailoring, English register, application forms, interview prep, system design, live coding, a company trainer.
- Schedules for the daily check, the weekly search pass and the monthly review.
- The universal question bank: 134 questions, 26 core, role packs, 13 story archetypes.
- An empty candidate pack, templates, `check_pack.py` and `english_check.py`.
- README and the guide in English and Russian.
