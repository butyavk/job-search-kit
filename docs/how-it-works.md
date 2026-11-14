# How it works

[Русская версия](how-it-works.ru.md)

The kit is a written-down version of a job search that Claude ran with a candidate for two months (engineering-manager roles, remote and relocation). Companies, money and contacts are removed; the methods and the numbers stay.

## The base: memory lives in files, not in a chat
A chat ends and loses its context; files do not. Every rule and every decision goes into a file in the same turn: the candidate's pack (`me/`), the search frame (`me/search-rules.md`), dated pass files and debriefs, a context file per company. **Claude is exactly as strong as its written rules.** A rule that lives only in a chat is broken in the next session.

| What | Where | Why |
| --- | --- | --- |
| Search frame and working rules | `me/search-rules.md` | the single source of truth; read first in every session |
| Facts, blocks, recipes | `me/facts.md`, `me/blocks/`, `me/recipes.md` | every answer, letter and form is built from them |
| Statuses and follow-ups | the tracker (a spreadsheet through tracker-mcp) | the single source of truth for statuses |
| Texts of an application batch | `FORM-ANSWERS.md` | browser tabs close; this file stays |
| A company process | its context file and prep document | every session about the company starts there |

Several sessions can run in parallel (search, a stage, system design); they share only files. **One file, one writer at a time:** two sessions once overwrote each other's CV specs.

## The search
- **Few hard filters, the rest is ranking.** Three filters: a must-have the candidate cannot honestly meet, real geography, the money floor. Level and company stage as filters gave 2–3 live roles per hundred checked; as ranking rules, seven candidates in five days.
- **Passes, not a feed.** A pass is a date window × titles × locations, with a dated file: what was read, who passed, who was dropped and why. After a few full passes — weekly monitoring.
- **Sources that worked:** LinkedIn (alerts daily, the guest API and logged-in search for passes); company boards through public ATS APIs (Ashby, Greenhouse, Lever, Workable, Teamtailor, Pinpoint) weekly over every known company; job sites (hiring.cafe first, then Himalayas, Jobicy, RemoteOK, We Work Remotely, HN «Who is hiring», levels.fyi, Wellfound); country boards for each channel (helloworld.rs and infostud for Serbia, jobs.ge for Georgia). About two thirds of search-index links were stale. The catalogue with how each source reads: `skills/job-search/sources.md`.
- **Age is not a filter.** Senior roles take 60–75 days to fill; fresh posts go first, an older one is checked for signs of life and applied to with a note to a person.
- **Every conclusion about a vacancy — two sources.** A hidden posting is not a closed one.

## The gate — the rule with the biggest effect
Five points, 0 / 1 / 2, as the screener sees the CV and form: level, stack, domain, geography, money. In the first 40 applications, 9 of 10 CV rejections had at least one knockout. Without knockouts — 2 calls from 13 applications and no CV rejections; with one — 1 call from 19. A number above the range in a salary field: none of 12 such applications reached an interview. A zero means no cold application: a route through a person, or a conscious one marked in the tracker.

## Applications
- A CV per vacancy by selection and order from one master, with a keyword coverage table: applications that reached a person covered 62–80% of the must-haves in the vacancy's own words; rejections and silence about 39%. After adding the market's words where they were true, coverage went from 41% to 54%.
- No questions in letters and notes — about money, location, visa or remote. Questions about location twice led to a fast rejection.
- Apply within 24 hours of the package being ready: packages that waited 3–6 days were late. On the same day, a short note to the hiring manager or recruiter; a note two weeks later arrives after the decision.
- A human replied to about 9% of cold applications. Silence for up to three weeks is not a signal.

## Follow-ups and the daily check
Follow-up 1 at application + 10 days, follow-up 2 at +14 more, «No answer» 30 days later; nobody written to twice in 14 days. Every morning a scheduled task reads mail and LinkedIn, prepares the tracker changes for your yes (it never writes them itself), lists new vacancies (at most 7), drafts the follow-ups due, and lists the week's interviews. Before naming a status, Claude checks it against mail and calendar: project documents always lag behind the mail.

## Interview preparation
- **Answer blocks** instead of written answers: the same facts in every round, any question answered by a chain. Each story has a whole-story block for a short answer and details for follow-ups.
- **One story, one round:** interviewers compare notes.
- **Learn, do not reread.** The prep document is the reserve; you learn a one-page map (question → first sentence → story) and 5–7 story anchors in four steps. Recall aloud on a timer, in random order, with a mark per answer; only the misses come back. A daily 15–25-minute drill (`/mock drill`), a full mock two days before, then nothing new.
- **Live coding:** requirements go into a comment in the code at once, and are checked against the code before «done» (an interviewer's answer did not reach the code six times in mocks). Run after every step. Open the platform's sandbox on the first day — once the database version turned out two hours before the interview. A browser trainer built in 6 days gave «Excellent» on both tasks.
- **System design:** questions before drawing, only those that change the design; count the heaviest part first; prepare 2–3 variants of each likely task with an assumption removed — the real task was exactly such a variant.
- **The same-day debrief** from the transcript turns into new blocks and trainer tasks.

## What did not work, and the fix
| What went wrong | The fix |
| --- | --- |
| Too strict filters gave 2–3 vacancies per hundred | level and stage moved into ranking |
| A number above the range in the salary field — rejection in 0–2 days | the gate; no range — estimate it, never count it as a pass |
| Ready packages waited 3–6 days and roles closed | apply within 24 hours of the package being ready; no limit on the number of packages |
| A cut quote of a requirement almost gave a false drop | quote in full, with «is a plus» and «or comparable» |
| The rules file was overwritten by an old version; removed filters came back | one source of truth, edited in the same turn, before any report |
| Two sessions edited one file | one file, one session; check the change time and diff before editing |
| Trainer tasks needed things not yet covered; time targets were unfair | tasks built from covered material; an audit for over-complication |
| A form filled in a temporary browser vanished with the session | forms only in the candidate's own browser, filled and checked in one go |
| A status taken from an outdated document | check mail and calendar before naming a status |
| The mail connector rewrote links in drafts into redirects | no links in drafts; add them by hand |

<a id="claudeai"></a>
## Running it in claude.ai (a Project)
1. Turn on code execution: Settings → Capabilities → «Code execution and file creation» («Create and edit files» in the new layout; on Team and Enterprise the owner turns it on, with Skills). Skills need it, and with it Claude can run the kit's scripts.
2. Skills: Customize → Skills → «+» → «Upload a skill», one zip per skill from the latest [release](https://github.com/butyavk/job-search-kit/releases/latest).
3. Project instructions: the text of `CLAUDE.md`.
4. Project files: everything in `job-search-kit-project-files-<version>.zip` from the same release — commands, templates, schedules, the bank, the pack template, the example story, this guide and the scripts — each named with its path (`commands__debrief.md`, `templates__debrief.md`; some names repeat across folders). There are no slash commands: Claude reads `commands__start.md` when you say «start» or «/start».
5. The pack: Claude gives each pack file as a download named with its path (`me__facts.md`, `me__blocks__10-work.md`); you add it to the project and replace the old one. With code execution it runs `check_pack.py` and `english_check.py` on copies; without it, it goes through the checklist in the `answer-blocks` skill.
6. Work per company: files named `companies__<company>__learning-sheet.md` and so on, in the same project — not a project per company, which would lose the pack and the kit.
7. The tracker: in the browser, a spreadsheet you keep by hand from Claude's row changes, with the columns of `templates__tracker.csv`; in the desktop app, the tracker-mcp `.mcpb` pointed at that file (save the CSV, or open it in Excel and save as .xlsx).
8. The independent fact check needs a session that can start a separate agent (Claude Code or the desktop app).
9. Moving to Claude Code later: download the pack files into the search folder and run `for f in me__*; do p="${f//__//}"; mkdir -p "$(dirname "$p")"; mv "$f" "$p"; done` there; the same for `companies__*`.
