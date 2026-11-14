---
name: job-search
description: Find, check and rank vacancies against the candidate's search frame — sources, the two-source check, the five-point screener gate, scoring, search passes and the monthly rejection analysis. Use for /find, the vacancy part of /apply and /today, the weekly pass and /review, and whenever a vacancy link comes up.
---

# Finding and ranking vacancies

The search is a series of **passes** over a fixed frame, not an endless feed. Every vacancy is checked and gated before any time goes into a CV or a letter.

## 1. The frame: few hard filters, the rest is ranking
The frame lives in one file, `me/search-rules.md`. Read it first in every search session. When the candidate changes the frame, edit the file in the same turn: date, decision, their words. Do not delete old decisions — mark them «outdated since <date>», or sessions start arguing with each other.

Only three hard filters:
1. **A must-have the candidate cannot honestly meet** (another main language, a required certificate, citizenship, experience they do not have). Quote the requirement in full: «or a comparable stack», «is a plus», «and/or» remove the requirement, and a cut quote gives a false drop.
2. **Geography, real rather than declared.** A country list without theirs, a time-zone window without theirs — out. Sort roles into channels: remote, a country without a visa, a country with sponsorship, relocation.
3. **Money.** The floor per market is written in the frame in advance. No range in the posting — estimate it from the company type and the hiring market; do not treat it as a pass.

Level and company stage go into ranking, not filters. As filters they gave 2–3 live roles per hundred checked; as ranking rules, seven candidates in five days.

### Proposing the frame (in `/start`)
From the candidate's experience, offer concrete options and let them choose: 2–3 role titles and levels that their CV supports, channels (remote / home country / visa-free / sponsorship / relocation) with what each means for them, money floors per channel from public salary data (with sources), company types (stage, size, domain). Write what they chose, and what they chose not to filter.

## 2. Sources
The full catalogue — what each source gives, how it reads (API, built-in browser, the candidate's Chrome), traps and statuses — is in `sources.md` next to this file. In short:
- **LinkedIn** — alerts daily; the guest API and logged-in search for passes; People for finding recruiters.
- **Company boards through public ATS APIs** (Ashby, Greenhouse, Lever, Workable, Teamtailor, Pinpoint, BambooHR, Breezy) — the best source for known companies; weekly over every company in the tracker and the target list.
- **Job sites and aggregators** — hiring.cafe, Himalayas, Jobicy, RemoteOK, We Work Remotely, Working Nomads, HN «Who is hiring», levels.fyi, Wellfound, YC, Welcome to the Jungle (never page through it for the candidate).
- **Country boards** for every country in the frame (helloworld.rs and infostud for Serbia, jobs.ge for Georgia, getmatch and Telegram for the Russian-speaking market…).
- Skip what does not pay off (`sources.md`, section 5); keep the candidate's own source list with statuses in the frame.

A **pass** = date window × titles × locations (for example 5 days, six titles, five locations, 2–3 pages each). The result is a dated file: what was read, how many cards, who passed, who was dropped and why. After a few full passes, switch to weekly monitoring: fresh posts and boards of companies already known to be interesting.

## 3. Checking a vacancy — two ways
Any conclusion about a vacancy — open, closed, «no other roles», date, range, work format — needs two independent sources.
- Its own link: Ashby `jobPosting: null` = taken down; 404 on Greenhouse, Lever or Workable = taken down; the Teamtailor page; logged-in LinkedIn `/jobs/view/<id>/`.
- A second path: the company's whole board, or the copy on LinkedIn. Absence from a board list proves nothing on its own (hidden Ashby postings open by direct link).
- Until the two agree, say «not found in X», not «closed».
- Check before every application: a role can close the day after the letter is ready.
- **Date**: by the ATS (`first_published` in Greenhouse, `publishedAt` in Ashby); LinkedIn paid posts can refresh their date, and a relaunch hides the age (the LinkedIn job id dates it, see `sources.md`).
- **Age is a risk and a place in the queue, not a filter.** Senior roles take 60–75 days to fill. Fresh posts (up to ~4 days) go first, within 24 hours. Older than ~14 days — check that the role is really alive: its ATS page is open, and there is a sign of life in the last 2–3 weeks (`updated_at` or «Reposted», «Actively reviewing applicants», fresh posts by the recruiter or hiring manager). Older than 90 days with no sign of life — the end of the queue (roughly a fifth of postings never end in a hire). Applying cold to an old role is fine; add a note to a person the same day.
- **Applicants**: logged-in LinkedIn (the guest view lags).
- **Range and format**: LinkedIn sometimes shows a range or «hybrid» that the ATS does not have.
- **A yes/no location question in the form** («Are you located in the UK or Poland?») is a hard filter: «No» is a geography zero, whatever the text says about remote.
- **Signals of the hiring form**: 401(k), HSA = US employment; «B2B contract», «tax allowance» = contractor. The country dropdown in the form is often more honest than the text. If all the company's other roles are on-site, remote will not appear.
- A location contradiction («Remote» in the text, a city on the card) is the first question for the recruiter.
- Company headcount: from its LinkedIn page at the time of the check.

## 4. The gate — as the screener will see it
Five points, each 0 / 1 / 2, judged on the CV and form answers that will actually be sent — not on the candidate's real experience:
1. **Level** — titles and scale against the role.
2. **Stack** — the required main language.
3. **Domain** — a must-have domain that is not there.
4. **Geography** — the country in the CV and form against the country list and format.
5. **Money** — the number that will go into the form against the likely range. A number above the range in a salary field is the strongest knockout.

Any zero — no cold application: either a route through a person (referral, recruiter, hiring manager — `/people`) or a conscious «apply anyway», marked in the tracker. The candidate may decide that some zeros never block (for example «managing managers», a different stack in a manager role, a remote country list without their country): write those exceptions into the frame with the date; such a zero is still shown, and the role goes into the queue by priority. The gate goes into the tracker and the vacancy report as one line: `L2 S2 D1 G0 M2 — G: country not in the list`.

Why: in the author's first 40 applications, 9 of 10 CV rejections had at least one knockout. Without knockouts: 2 calls from 13 applications and no CV rejections; with one: 1 call from 19.

## 5. Ranking
Score each vacancy that passed the hard filters, 0–2 per line, and show the total with the two lines that decided it:
- gate total (from section 4);
- channel priority from the frame (for example remote first);
- level fit (the role matches the candidate's last real scope);
- domain and product fit (where their stories are strongest);
- freshness (posted ≤ 4 days = 2, ≤ 14 = 1, older = 0, and older than 90 with no sign of life goes last) and applicants (fewer is better);
- a route through a person (a contact at the company, a reachable hiring manager);
- money (range published and above the floor = 2, unknown = 1, below = 0).
The weights are the candidate's: if the frame says «remote first», channel counts double. Ranking orders the list; it does not drop anything that passed the filters.

## 6. Output of a pass and of a single check
- Short list: at most 8 rows (7 in the daily check). Company — role — format and location — date and applicants — score — why it fits — the main risk or gate zero — the route through a person.
- Dropped: one line each with the reason. Already in the tracker: one line each.
- The tracker: `add_applications` as a dry run; write after the candidate's yes. Never apply.

## 7. Timing
- Apply within 24 hours of the package being ready; there is no limit on the number of packages — about one application in ten reaches a person.
- Monday to Thursday, Tuesday best; the company's morning (6–10 a.m. their time). Not Friday evening or the weekend: the application lands in Monday's pile. When the day and freshness disagree, freshness wins.
- A referral reaches an interview far more often than a cold application (about 40% against 3% in Ashby's 2026 data): look for a person first when one exists.

## 8. The monthly rejection analysis
Template `templates/rejection-analysis.md`. What it found in the author's first 48 applications:
- before any call, the main reasons were location and money (gate knockouts), then the CV's vocabulary;
- applications that reached a person covered 62–80% of the must-haves in the vacancy's own words; rejections and silence, about 39%;
- a template rejection in 0–3 days is almost always a form filter (location, work authorization), not a reading of the CV.
Propose changes to the frame, the CV or the sources with the evidence; change them only after the candidate agrees.
