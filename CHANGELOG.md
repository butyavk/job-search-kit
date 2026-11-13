# Changelog

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
