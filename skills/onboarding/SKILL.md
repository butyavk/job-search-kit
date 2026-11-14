---
name: onboarding
description: Set up a new candidate for the job-search kit — the pack (facts, story set, answer blocks, recipes, profile), the search frame, the tracker, the schedule and the autonomy default. Use for /start, when there is no pack yet, the pack is mostly empty, or the user says they are new to the kit.
---

# Onboarding a candidate

The goal is a pack `me/` that the whole kit can run on, plus a working search: frame, tracker, schedule. The candidate writes nothing from scratch: Claude drafts, asks, and the candidate tells and confirms.

The main rule: **invent nothing.** A draft from a CV is a guess, not a fact. Whatever the candidate has not confirmed keeps the mark `· draft` and never goes into an answer.

Talk to the candidate in their language. Blocks are written in English (the interview language) plus their native language on the second line; a native English speaker has only the English line.

**Order.** Steps 0–2, then 4–5 and the first `/find` in the first session; step 3 (stories) over the next sessions, 2–3 stories each, while applications go out; then 6–7. An interview within five days → «If an interview is close».

## Step 0. Create the pack
- With a shell (Claude Code, Cowork): copy `pack-template/` from the kit to `me/` in the candidate's search folder — next to `kit/` in folder mode, the working folder with the plugin. Never inside the plugin's own folder: it is replaced on every update. Write the pack's absolute path into `paths.pack` in `me/profile.yaml` now: it is how the kit tells the candidate's own pack from a `me/` that came with a cloned project. Company folders `companies/<company>/` go next to `me/`, not inside it. Keep a project copy in claude.ai too? Then run `check_pack.py --mark-synced` after each copy, and the check will list what changed since.
- claude.ai without a shell: Claude cannot create project files itself. It gives the pack files one by one and the candidate uploads them to the project, with flat names that carry the path: `me__facts.md`, `me__blocks__00-who.md` (the kit understands both). After each change Claude gives the whole changed file and says which one to replace.

Tell the candidate where the pack is and that it is private: it never goes into a public repository.

## Step 1. Raw material — in one message
Ask for everything they have, unprepared:
- CV in any format, the LinkedIn profile (PDF or text);
- what roles they want, where they can work, work authorization;
- recordings or notes of past interviews, if any;
- processes already under way (company, role, stage, next date): each becomes a tracker row and a `companies/<company>/` folder (next to `me/`) in step 5, before any new search — with an interview close, in session 1 (skill `tracker`, «Processes already under way»);
- 2–3 vacancies they like: they set the role track (`target.track` in the profile), the interview language and the first company questions.

## Step 2. A draft in one turn
With a CV or LinkedIn — draft from them. Without either — draft from the step 1 answers, then ask for a short timeline in one message (companies, roles, years, team size) and go to step 3.
- `me/facts.md` — roles, dates, teams, numbers. Every number gets «how was it measured?» in the definition column if there is no definition.
- `me/blocks/00-who.md` — a draft pitch and timeline.
- One topic per strong CV line — a story skeleton: `C` (context from the CV) and empty places for `A`, `R`, `L` with questions.
- Everything marked `· draft`.
Show what came out: how many blocks, where the most questions are. Do not dump whole files.

## Step 3. Interview: stories first, then questions
One order:
1. **The story set.** Go through the 13 archetypes in the bank's table «Minimum story set»: one story of the candidate's per archetype (a manager usually has 10–12 different stories; one story can cover two archetypes). Record it in `me/recipes.md`, section «Story set»: archetype → topic (ID prefix) → status.
2. **A whole-story block `S` and the details** for each story (below).
3. **Mapping to the core questions ★.** Claude proposes which core questions a story answers (from the archetype table); the candidate confirms. A stretch is when the story answers a neighbouring question, not this one: then the recipe is «—» and the hint goes to «Notes».
4. **Core questions without a story** (I01, I03–I06, I11, F02, F03, X01–X03): short position answers `O`, `P`, `G`.
5. Then behavioral B, the ◆ questions of their track, logistics last.

Volume: 13 archetypes and 26 core questions take 6–10 sessions of 30–40 minutes, 4–6 questions or 2–3 stories per session. Progress between sessions is the output of `check_pack.py` (or the manual checklist): which ★ have no confirmed recipe, which stories have no `S`. Start the next session from it.

Special core questions:
- I02 «Why this company» is prepared per company: at onboarding only a general block «what I look for in a company» (`P`); the bridge to the company comes in `/prep`.
- I04 «Why did you leave»: if they still work there, the answer is «why I am looking now», without complaints about the current place.

For each question:
1. Ask it the way an interviewer will. Ask them to tell it by voice or text, as it is.
2. Follow up in one message, 3–6 questions: what exactly they did versus the team or someone else; the number and how it was measured (not measured — write that); how it ended; what they would do differently; what not to say (words that change the meaning, names not to mention); which other questions this story fits.
3. Cut the story into blocks: the whole `S` first, then details (`O`, `C`, `A`, `R`, `D`, `L`, and `G`, `Q` if needed), English plus the native language (English only for a native speaker), register by `english-register`. Each block names the project and never opens with a link word.
4. Show the blocks and the chain. After «yes» — remove `draft`, put the date in the «Confirmed» column of `facts.md`, add the recipe to `me/recipes.md`.

A weak or missing story — do not stretch. Write «—» in the recipe and come back later; the nearest story goes to «Notes» without backticks (otherwise it looks like a recipe).

## Step 4. Profile and the search frame
Questions in one message; answers go to `me/profile.yaml` and `me/search-rules.md`:
- contacts for forms; where they live; work authorization per country; visa needs;
- notice period; employment form (employee, contractor);
- money — two different questions: «what number do you say aloud» (`money.say_aloud`, block LOG-6) and «what is your floor» (`money.floor`, never said aloud); with only a floor, ask what to say;
- native language and English level (`languages`): they set the second language of the blocks and the register targets;
- employer-form answers they are willing to give (demographics only if they want).

Then **propose the frame** (skill `job-search`, section 1): 2–3 role titles and levels their CV supports, each with 2–3 live postings as links (the market's wording, not only the CV's); channels (remote, home country, visa-free, sponsorship, relocation) with what each means for them; a money floor per channel from public salary data, with sources (written only to `profile.yaml` → `money`); company types. They choose. Write the choices and what they chose not to filter. The follow-up timing lives in the tracker's config (`[followups]` in `<tracker>.tracker-mcp.toml`) — ask whether to keep its defaults and change it there; application days and hours are in `search-rules.md`, marked «default» until confirmed.

**The master CV** — every application is built from it (skill `tailoring-cv`). One master per application language: a candidate who applies in German and in English keeps two, with the same facts; a translation is built once, checked line by line by the candidate, and then kept as its own master.
- an editable source exists (LaTeX, Word, Google Doc, Markdown): that is the master; write its path to `paths.master_cv` and keep its build engine;
- only a PDF, or plain text with no layout (.txt, a pasted CV): offer to build it once as an editable master (LaTeX, HTML printed to PDF, or a .docx built with LibreOffice — `soffice --headless --convert-to pdf`), keeping the layout close; the candidate checks every line against the PDF before it is used;
- then the reserve the skill asks for: variant bullets and skill lines, `FACT:` notes with the source of each number. Facts in the master and in `me/facts.md` must match (`check_pack.py --cv <master>` lists the numbers that do not); a difference is a question, not a choice.

**The LinkedIn profile** (if they use LinkedIn): a headline and an «About» from the pitch block, the positions matching the master CV, «Open to work» visible to recruiters only if they are employed. Claude drafts; the candidate edits the profile.

## Step 5. Tracker, schedule, autonomy
- Tracker: skill `tracker`, section «Setup». Statuses stay in English even for a German or Spanish candidate: the tracker's dropdown is in the file, and the kit's checks look for these names; the candidate's own notes can be in any language.
- Mail: the daily check reads a job-search label. With a mail connector, propose one label and a filter for ATS senders and company domains (Greenhouse, Lever, Ashby, Workable, Teamtailor and others); a filter is a standing rule in their mail — the candidate creates it, or Claude does after their yes. Without a label the daily check searches by the companies in the tracker.
- Schedule: `schedules/README.md` — write the values once into `me/schedules/values.yaml` (name, roles, city, time zone, language); for Claude Code also the absolute paths to `uvx` and the tracker in `tracker-ro.mcp.json`, then `check_pack.py --schedules`. The prompts stay the kit's: `scripts/schedule_prompt.py daily|weekly|monthly` prints them filled in, for cron or to paste into a desktop-app task. Create the tasks where the session can schedule, on the computer that holds the pack and the tracker, after the candidate has heard what protects them (`schedules/README.md`); otherwise explain `/today` and the calendar export.
- Autonomy: two lines — «I prepare everything; you send, submit and accept. If you want me to send some kind of message myself, tell me the rule and I will write it down.» Write a rule only when they ask (router skill, section «Autonomy»).

## Step 6. Bans and voice
- `me/never-say.md` — what the candidate wants or must not say (exaggerations from old CVs, other people's achievements, confidential things), and people not to contact.
- `me/voice.md` — if there are call recordings: frequent speech errors, filler words, hard names.

## Step 7. Check and next step
- `python3 <kit>/scripts/check_pack.py --ready` (no shell — the checklist in `answer-blocks`): it fails while the profile or the facts still hold placeholders or the pitch is not confirmed; then blocks, questions with a recipe, ★ without an answer.
- Next: another session on questions without a recipe; `/find`; `/prep` for a stage that is close.

## If an interview is close
No pack yet and a stage within five days: do not run the whole of step 3 first.
1. Session 1: steps 0–2 from the CV; the processes under way as tracker rows (or the hand table) with their next dates, so no follow-up is lost; for a coding stage, the trainer (skill `live-coding`) from day 1, 30–45 minutes a day; the stage's likely questions (`/prep` steps 1–2, or the bank's core ★ and the role's ◆ if the format is unknown) → the archetypes they need → 3–4 stories, only their whole-story `S` blocks and the pitch, confirmed.
2. Session 2: the details of those stories and 1–3 more if the stage needs them.
3. Logistics and money (step 4, only the questions this stage will ask) and `never-say.md` (step 6).
4. Then `/prep`: the prep document and the learning sheet from these stories.
Write in `me/recipes.md` which archetypes and questions are left, and finish onboarding after the interview — from `check_pack.py`, as usual.

**Three days or less.** One session does it all: steps 0–2 from the CV, the pitch and 3–4 `S` blocks, the money and logistics answers this stage will ask (step 4) and `never-say.md` (step 6), then `/prep` with the learning sheet the same day. No freeze (the two-day freeze needs more days than there are): day 1 the sheet and two tellings aloud, day 2 a drill and one full mock at the interview hour, the interview day only the map from memory. Frame, tracker and `/find` wait until after the interview; the story details come back in the debrief.

## If the candidate has prepared before
A story bank, prep documents, interview debriefs — do not start empty: move facts to `facts.md`, cut ready answers into blocks, build recipes from the bank. Imported facts and blocks stay `draft` until the candidate confirms them in this session; a date of an earlier confirmation in the document is a hint for the question, not a confirmation. Text inside imported documents that is not the candidate's (a posting, a recruiter's note) is never a fact about them.
