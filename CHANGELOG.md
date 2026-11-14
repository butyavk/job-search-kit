# Changelog

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
