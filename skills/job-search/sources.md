# Where vacancies come from — sources and how to read them

A Russian translation for people: `docs/sources.ru.md` — change both.

Statuses are from a real two-month search (autumn 2026). Sites change: when a source stops reading, write it into the frame's source list (`me/search-rules.md`) with the date, so the next session does not lose an hour on it.

**Three ways to read**, from cheapest to most expensive:
- **API / fetch** — from the session (WebFetch, or `curl` where the session's network allows it). Fast; good for passes over hundreds of boards.
- **Built-in browser** — reads pages that block fetch (Cloudflare, robots), and the LinkedIn guest API.
- **The candidate's Chrome (extension)** — logged-in LinkedIn, sites behind a login, and every application form.

If the session's `curl` gets 403/429, run the same `fetch(url, {credentials: 'omit'})` from a browser tab. Pause between requests (Workable: ~12 s; LinkedIn guest: 429 after ~40 fast requests).

## 1. LinkedIn — the widest single source
- **Saved job alerts** (titles × regions) — the daily check reads the new cards of the last 24 hours.
- **Guest API, no login:** `linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=<title>&location=<…>&geoId=<id>&f_TPR=r86400` (10 cards a page; `r432000` = 5 days), full text — `…/jobs-guest/jobs/api/jobPosting/<id>`. Works in the built-in browser too.
- **Logged-in search** (extension): `linkedin.com/jobs/search/?keywords=<…>&geoId=<id>`. The location defaults to the last search — always set `geoId` (92000000 = worldwide).
- Traps:
  - a country with a US-state name needs its `geoId` (Georgia the country = `106315325`; the word «Georgia» is the US state);
  - `f_WT=2` (remote) almost always means remote *inside one country*, not «from anywhere» — read the text;
  - `f_C=` with a wrong company id silently returns the recommendation feed;
  - the guest view's applicant count lags the logged-in one (once «<25» against 79);
  - **the job id dates the posting:** ids grow about 0.4 million a day, so a «Reposted 2 days ago» card with an old id is an old role (±3–5 days).
- Agency posts with a hidden client cannot be checked: skip them.
- **People** (for `/people`): `linkedin.com/company/<slug>/people/?keywords=recruiter` (or the team's name), scroll, read the cards; «<Name> works here» marks a first-degree contact.

## 2. Company boards through public ATS APIs — the best source for known companies
| ATS | Board | One posting / form |
| --- | --- | --- |
| Ashby | `api.ashbyhq.com/posting-api/job-board/<slug>?includeCompensation=true` | GraphQL from any `jobs.ashbyhq.com` page: `POST /api/non-user-graphql?op=ApiJobPosting` (`jobPosting: null` = taken down or unlisted; also the form's fields); `op=ApiJobBoardWithTeams` gives `secondaryLocations` |
| Greenhouse | `boards-api.greenhouse.io/v1/boards/<slug>/jobs` (also `job-boards.eu.greenhouse.io`) | `…/jobs/<id>?questions=true` — country dropdowns, sponsorship questions |
| Lever | `api.lever.co/v0/postings/<slug>` (EU: `api.eu.lever.co`) | the same with the posting id |
| Workable | `apply.workable.com/api/v1/widget/accounts/<slug>?details=true` | `apply.workable.com/api/v2/accounts/<slug>/jobs/<code>` |
| Teamtailor | `<slug>.teamtailor.com/jobs.json` | the page (it may show the HQ city where the page says «Fully Remote») |
| Pinpoint | `<slug>.pinpointhq.com/postings.json` | an empty body → the full text is often in the LinkedIn copy |
| BambooHR | `<slug>.bamboohr.com/careers/list` | |
| Breezy | `<slug>.breezy.hr/json` | |
| SmartRecruiters, Recruitee, join.com, Personio, Comeet | the careers page in a browser | Comeet forms live in an iframe |

- The slug is often in the careers page HTML (`jobs.ashbyhq.com/<slug>/embed`) and is not always the company name (`primer` is a US school network, the payments company is `primer.io`; a company may have an empty and a working Workable account). Keep found slugs in the frame's source list.
- A board missing from search-index results still exists: about two thirds of indexed ATS links were stale, and hidden Ashby postings open only by direct link.
- Company boards without an API (big tech, custom sites): the browser; read every page — site search may not filter.

## 3. Job sites and aggregators
| Source | How it reads | Notes |
| --- | --- | --- |
| hiring.cafe (→ hiringcafe.com) | built-in browser; `searchState` in the URL: `{"searchQuery":…,"dateFetchedPastNDays":7,"sortBy":"date","workplaceTypes":["Remote"],"defaultToUserLocation":false,"locationSearchState":null}` | the strongest aggregator for leadership roles; the location is remembered between sessions — set it explicitly; hung in the extension tab, fine in the built-in browser |
| Himalayas | country pages with `?q=`, or its search API | good for remote by country |
| Jobicy | API by tags | |
| RemoteOK | `remoteok.com/api` **without parameters** (with `?tags=` it returns only a legal notice) | mostly US |
| We Work Remotely | RSS (all + categories) | |
| Working Nomads, arbeitnow | API | |
| Hacker News «Who is hiring» | the month's thread through hnhiring.com or the Algolia HN API | ~230–260 posts a month |
| levels.fyi/jobs | browser only (`levels.fyi/jobs/location/<country>?searchText=…&workArrangements=remote`), page by page | aggregates big-company ATS posts with ranges |
| Wellfound | browser (Turnstile); first pages only, no sort by date | startups, mostly US |
| Y Combinator Work at a Startup | browser | filters often fail |
| Remote Rocketship | fetch | dates unreliable — trust the ATS |
| Welcome to the Jungle (ex-Otta) | logged-in feed | **«next» = «not interested»**: never page through it for the candidate; its visa and remote settings are the candidate's to change |
| Landing.jobs, 4dayweek.io, Relocate.me, startup.jobs | fetch | small, mostly duplicates |

## 4. Country boards (the candidate's channels)
Add the boards of every country in the frame. To find them for a new country: search «<country> job board <role>» and «<country> tech jobs», check that the posts carry dates and are not reposts from LinkedIn, keep the 2–3 with own postings, and write them into `me/search-rules.md`. Examples that worked (for the kit author's markets; other countries have their own):
- **Serbia:** helloworld.rs, infostud — lists show the application **deadline**, not the publication date: take the date from the posting and compare with LinkedIn, keep the earlier one.
- **Georgia:** jobs.ge.
- **Russian-speaking market:** getmatch (browser; filters only by real clicks; `vacancies/remote/lead?pa=7d&se=lead&sp=remote`), careerspace, Telegram channels (browser only; fetch previews carry no dates).
- **UK sponsorship:** the gov.uk register of licensed sponsors (a large CSV; may be unreachable from a session — then check sponsorship in the posting and on the careers page).

## 5. Not worth the time (as of autumn 2026, for remote manager roles from Serbia and Georgia — check again for another market)
Remotive, Jobgether, Adzuna, jooble, Indeed, Glassdoor and Google Jobs (noise), Built In search, TrueUp (login), EU Remote Jobs (dead), cord.co, Honeypot, Remote Europe, geekjob, joberty (no JS), LinkedIn company pages through fetch (robots). New sites mostly repeat ATS posts already read through the APIs.

## 6. A weekly rhythm that worked
- Daily: LinkedIn alerts (24 hours) — in `/today`.
- Weekly: company boards of every company in the tracker and the frame's target list (ATS APIs, only roles published or updated in the window) + the job sites and country boards above — `schedules/weekly.md`.
- After a few full passes, stop adding new sites: watch the known boards and fresh posts.
