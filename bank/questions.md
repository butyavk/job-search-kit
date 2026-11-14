# Universal question bank

Questions asked in almost any interview, plus role packs. Collected from university career-centre lists (UTK, Carleton), lists of the most common questions (Inc., IGotAnOffer), Big Interview competencies, Amazon Leadership Principles, Meta's behavioral signals and engineering-manager question sets (Exponent/Aced), then extended from real interviews. Sources are at the end.

There are no answers here: this is the engine. Answers live in the candidate's pack (`me/recipes.md`): for each ID, a first line and a chain of blocks from `me/blocks/`.

## Layers: from the core outwards

| Layer | What it is | Where |
| --- | --- | --- |
| 0. Core ★ | 26 questions asked in almost every interview for any role. Prepare them first; answer without thinking | marked ★ in sections I, B, F, C, P, J, T, X |
| 1. Behavioral | «Tell me about a time…» by competency: team, conflict, pressure, change, ownership, learning, influence, quality, ethics | B, C, F, K |
| 2. Role packs ◆ | what your role cannot skip. Manager: R, P, H, D, M, J; engineer and tech lead: T, S; product and cross-functional: U; AI: A | ◆ marks the core of a pack |
| 3. Company | why us, their product and competitors, their values | I02, I08–I10, K08 + the company brief |
| 4. Logistics and your questions | location, work authorization, money, timing; your questions at the end | X, Z |

Column «Who»: **mgr** — most likely asked of a manager (EM, Head, Director); **all** — any role. An engineer can skip «mgr» questions. `check_pack.py` counts ◆ by `target.track` in the profile.

Order of preparation: core → behavioral → your role pack → the company. A newcomer (`/start`) goes in the same order.

## Core ★ — 26 questions

| Topic | ID |
| --- | --- |
| About you and motivation | I01 about you · I02 why us · I03 why looking · I04 why you left · I05 what you look for · I06 in 3–5 years · I11 why you |
| Stories | B01 proudest · B02 teamwork · B03 conflict with a colleague · B04 deadline and pressure · B05 leadership · B06 change · B07 ownership beyond the role |
| Mistakes and reflection | F01 a mistake · F02 weakness · F03 strengths · F04 a failure · P08 feedback about you |
| Judgement | C01 disagreeing with your manager · J02 a decision without data |
| Technical | T02 what you built yourself recently · T03 the hardest technical problem |
| Logistics | X01 location and relocation · X02 work authorization and start · X03 money |

Plus always: «Do you have any questions for us?» — section Z.

## Minimum story set

13 archetypes, usually covered by 10–12 stories: one story can cover two archetypes, and each covers many questions. A story is a whole: it has a whole-story block (`S`, 20–40 s, answers the question on its own) and detail blocks added on follow-ups. Every block reads without its neighbours: it names the project or company and does not open with «Then» or «That».

| Archetype | Covers |
| --- | --- |
| 1. The hardest technical problem | T03, T04, T06, B04, B12 |
| 2. Proudest: a system or product with a result | B01, I11, T08, U06, D01 |
| 3. Teamwork, with other functions too | B02, U01, C02 |
| 4. Conflict: with a colleague, with a manager, a lost argument | B03, C01, C03, C04, P10, B09 |
| 5. A mistake and a failure | F01, F04, F05, B11 |
| 6. Leadership and growing people | B05, P02, P05 |
| 7. A decision under pressure or without data | J02, J01, B04, B12 |
| 8. Change and uncertainty | B06, J03 |
| 9. Ownership: beyond the role, raising the bar | B07, B13, B15 |
| 10. Feedback: received and given | P08, P07, F02 |
| 11. A customer or a difficult stakeholder | U03, B16, U02 |
| 12. Learned something new fast | B08, S02, S03 |
| 13. A weak performer and a hard conversation (manager) | P01, P03, B12 |

How to use it:
- **A newcomer** goes through the bank with Claude (`/start`): tells it in their own words, Claude asks follow-ups, cuts the answer into blocks and builds the recipe.
- **Preparing for a company** (`/prep`): Claude takes the stage's questions, puts in the recipes, and shows questions without a recipe as gaps.
- **A new question from an interview** goes to the candidate's pack, `me/questions-extra.md` (IDs `Q01`…): the bank is part of the kit and an update would overwrite it. A question that belongs in the kit for everyone comes as a pull request, with the next free ID; numbers are never reused.

## I — about you and motivation · all roles

| ID | Question | What they check | Follow-ups | Who |
| --- | --- | --- | --- | --- |
| I01 ★ | Tell me about yourself. | 60-second trajectory, level, link to the role | And what are you doing now? | all |
| I02 ★ | Why this company? Why this team? | knows the product, has a reason beyond «the role is open» | What do you know about our product? | all |
| I03 ★ | Why are you looking? What happened at your last job? | calm, no red flags | What exactly closed — your project or more? | all |
| I04 ★ | Why did you leave <previous company>? | the same story, no grudges, no running away | Was your role cut? | all |
| I05 ★ | What are you looking for in your next role? | expectations match the role | What would make you say no? | all |
| I06 ★ | Where do you want to be in three to five years? | ambition and realism | — | all |
| I07 | What do you do now / since your last job? | the pause makes sense | — | all |
| I08 | What gets you most excited about this role? | energy and specifics | — | all |
| I09 | What would you change about our company or product? | looked deep, without arrogance | — | all |
| I10 | Who are our competitors, and how should we win? | market understanding | — | all |
| I11 ★ | Why should we hire you? What makes you different from other candidates? | 2–3 strengths tied to the role, with proof | What would your first win be? | all |
| I12 | What motivates you? | what gives energy, does it match the role | — | all |
| I13 | How would your colleagues or your manager describe you? | self-awareness, matches the references | And what would they criticize? | all |
| I14 | What do you do outside of work? | a person, not a function; no risks | — | all |
| I15 | What should we know that is not on your CV? | something of value beyond the CV | — | all |
| I16 | What did you like and dislike about your last job? | no complaints about people, what you look for | — | all |
| I17 | Why did you choose engineering? How did you start? | origins, interest in the work | — | all |

## B — behavioral competencies · all roles

«Tell me about a time…» questions. Answer with a story: the situation in one sentence, your own action, the result with a number, the lesson.

| ID | Question | What they check | Follow-ups | Who |
| --- | --- | --- | --- | --- |
| B01 ★ | What achievement are you most proud of? | scale, own role, result | Why that one? What was your part? | all |
| B02 ★ | Tell me about a time you worked well in a team. | contribution to the common result, not solo | What did others do? | all |
| B03 ★ | Tell me about a conflict with a colleague. Who was the hardest person to work with? | direct talk, no avoidance, no pressure | How is the relationship now? | all |
| B04 ★ | Tell me about a tight deadline or a time you worked under pressure. How did you prioritize? | prioritization, trade-offs, calm | What did you drop? | all |
| B05 ★ | Tell me about a time you showed leadership. | leadership with or without the title | How did you get people on board? | all |
| B06 ★ | Tell me about a time priorities or requirements changed in the middle. How did you adapt? | flexibility without chaos | What did it cost? | all |
| B07 ★ | Tell me about a time you did something outside your responsibility. | ownership | Who asked you to? | all |
| B08 | Tell me about a time you had to learn something new quickly. | speed and way of learning | How long did it take? | all |
| B09 | Tell me about a time you convinced someone who disagreed with you. | arguments, data, listening | What if they had said no? | all |
| B10 | Tell me about a time you explained a technical topic to a non-technical person. | clarity, the listener's level | — | all |
| B11 | Tell me about a time you were wrong. | admitting it, changing one's mind | — | all |
| B12 | What was the toughest decision you made recently? | weighing, responsibility | Would you decide the same today? | all |
| B13 | Tell me about a time you were unhappy with quality and raised the bar. | high standards | — | all |
| B14 | Tell me about an ethical dilemma or pressure to cut corners. | honesty | — | all |
| B15 | Tell me about a time you were blocked by another person or team. What did you do? | escalation, initiative | — | all |
| B16 | Tell me about a difficult customer or stakeholder. | empathy, boundaries | — | all |
| B17 | What lesson from the last year changed how you work? | reflection, growth | — | all |

## R — role, scale, level · manager

| ID | Question | What they check | Follow-ups | Who |
| --- | --- | --- | --- | --- |
| R01 ◆ | How big was your team? How many direct reports? | real scale, honesty | N reporting to you directly — how did that work? | mgr |
| R02 ◆ | Walk me through your role at <company>. What was your scope? | scope of responsibility, «I» not «we» | What was your part personally? | mgr |
| R03 | How long have you managed people? Was it a people role or a technical one? | years of people management | Who did 1:1s, promotions, exits? | mgr |
| R04 ◆ | Do you want to manage managers? Have you? | level, ambition against the role | — | mgr |
| R05 | How did you structure the team? | org design | Why that split? | mgr |
| R06 | How did your title compare to what you actually did? | checking titles and references | — | mgr |
| R07 | Who did you report to, and how did you work with them? | managing up | — | mgr |

## T — technical depth and hands-on · engineer, tech lead

| ID | Question | What they check | Follow-ups | Who |
| --- | --- | --- | --- | --- |
| T01 ◆ | How hands-on are you today? | share of technical work | When did you last write production code? | mgr |
| T02 ★ | What did you build yourself recently? | «I built» rather than «I reviewed» | Why you and not the team? | all |
| T03 ★ | Tell me about the hardest technical problem you solved. | depth, analysis, a number | What alternative did you consider? | all |
| T04 | Tell me about a performance problem you fixed. | method of analysis | How did you measure it? | all |
| T05 | How do you review designs and code? What do you look at? | quality standards | Do you block merges? | all |
| T06 | Tell me about an incident you handled. | ownership, order of actions, postmortem | What would you do differently today? | all |
| T07 | How do you think about security in your systems? | maturity without «I am the expert» | — | all |
| T08 | Tell me about a system or service you designed. | architectural thinking | What would you change now? | all |
| T09 | Monolith or microservices? How do you draw service boundaries? | pragmatism | — | all |
| T10 | How do you handle events, webhooks and delivery guarantees? | understanding of contracts | At-least-once or exactly-once? | all |
| T11 | How do you version a public API? | platform thinking | — | all |
| T12 | How deep are you technically compared to your staff engineers? | honest self-assessment | — | mgr |

## A — AI · by role

| ID | Question | What they check | Follow-ups | Who |
| --- | --- | --- | --- | --- |
| A01 ◆ | How do you use AI in your work? | specifics on two levels: product and engineering | What exactly did the bot check? | all |
| A02 | How do you build an AI-first engineering organization? | processes, guardrails | What changed for the team? | mgr |
| A03 | How do you measure the quality of an LLM feature? | evals, maturity | — | all |
| A04 | If agents write most of the code, how do you keep quality and security? | review as the bottleneck | — | mgr |
| A05 | How did you choose a model or provider? | data, reversibility | How did you switch? | all |
| A06 | Tell me about an AI product or feature you shipped. | AI in production | — | all |

## P — people · manager (P08 — all roles)

| ID | Question | What they check | Follow-ups | Who |
| --- | --- | --- | --- | --- |
| P01 ◆ | Tell me about a low performer. | noticed early, said it at once, plan, outcome | How exactly did you help? What if it had not worked? | mgr |
| P02 ◆ | How do you grow people? Tell me about someone you promoted. | growing people and leads | How did you know they were ready? | mgr |
| P03 | Tell me about letting someone go. | hard decisions, fairness | — | mgr |
| P04 ◆ | How do you run one-to-ones? How often? | management rhythm | What do you ask your leads? | mgr |
| P05 | How do you coach a team lead? | managing through leads | — | mgr |
| P06 | How do you notice and prevent burnout? | care and structure | — | mgr |
| P07 | How do you give feedback? Tell me about hard feedback you gave. | directness with respect | — | mgr |
| P08 ★ | Tell me about feedback you received about yourself. | self-criticism | What did you change? | all |
| P09 | How do you recognize good work? | culture | — | mgr |
| P10 | How do you handle a conflict between two engineers? | mediation | — | mgr |
| P11 | How do you build trust in a new team? | the first weeks | — | mgr |

## H — hiring · manager

| ID | Question | What they check | Follow-ups | Who |
| --- | --- | --- | --- | --- |
| H01 ◆ | How do you hire? | structure, fairness | What do you look for? | mgr |
| H02 | Tell me about a hire that failed. | admitting a mistake, the lesson | What did you change? | mgr |
| H03 | How do you make hiring fair and consistent? | the same tasks and format | — | mgr |
| H04 | Who would your first hires be here? | understanding of the team and the business | — | mgr |

## D — delivery and process · manager, senior

| ID | Question | What they check | Follow-ups | Who |
| --- | --- | --- | --- | --- |
| D01 ◆ | How do you ship? How did you speed up delivery? | delivery system, numbers | How did you measure it? What happened to incidents? | mgr |
| D02 | What engineering practices did you introduce? | ADRs, reviews, postmortems | What changed after? | mgr |
| D03 | How do you balance features and technical debt? | prioritization | Do you have a fixed share? | mgr |
| D04 | How do you plan and estimate? | Scrum/Kanban without dogma | How do you handle unplanned work? | all |
| D05 | How do you make technical decisions in a team? | ADRs, delegation | When do you overrule a lead? | mgr |
| D06 | How do you run incidents and postmortems? | blameless, process | — | mgr |
| D07 | How do you manage on-call? | load and reliability | — | mgr |
| D08 | How do you roll out risky changes? | flags, gradual rollout | How did you know the new version was better? | mgr |

## M — metrics · manager

| ID | Question | What they check | Follow-ups | Who |
| --- | --- | --- | --- | --- |
| M01 ◆ | How do you measure your team? What metrics do you use? | DORA/SPACE without a cult | — | mgr |
| M02 | How did you measure <number from your CV>? | defending numbers: definition, baseline, period | — | mgr |
| M03 | How would you know in six months that this area works well? | business metrics | Three metrics? | mgr |
| M04 | Tell me about OKRs you set. | goals the team can move | — | mgr |

## U — product and customer · senior, manager

| ID | Question | What they check | Follow-ups | Who |
| --- | --- | --- | --- | --- |
| U01 ◆ | How do you work with product and other functions? | partnership, cross-functional work | — | all |
| U02 | Tell me about a time you said no to product. | influence with data | Who decided in the end? | all |
| U03 | Tell me about a time you were close to a customer. | customer obsession | — | all |
| U04 | Tell me about something you simplified. | 80/20 | — | all |
| U05 | How do you decide what not to build? | prioritization, MoSCoW | — | mgr |
| U06 | Tell me about a product built from zero. | zero to one | What would you do differently? | all |

## C — conflict and influence · all roles

| ID | Question | What they check | Follow-ups | Who |
| --- | --- | --- | --- | --- |
| C01 ★ | Tell me about a disagreement with your manager or a founder. | disagree and commit | What did you change after? | all |
| C02 | Tell me about a change you drove across teams. | influence without authority | Who was against it? | all |
| C03 | Tell me about a time you disagreed and lost. | maturity | — | all |
| C04 | Your tech lead disagrees with your decision. What do you do? | decision boundaries | — | mgr |
| C05 | How do you communicate a hard decision? | directness, reasons | — | mgr |

## F — mistakes and lessons · all roles

| ID | Question | What they check | Follow-ups | Who |
| --- | --- | --- | --- | --- |
| F01 ★ | Tell me about a mistake you made. | own share, the lesson | What did it cost? | all |
| F02 ★ | What is your biggest weakness? | self-awareness and what you do about it | — | all |
| F03 ★ | What are your strengths? | specifics with examples | — | all |
| F04 ★ | Tell me about a project that failed. | analysis without blame | — | all |
| F05 | What would you do differently in your last role? | reflection | — | all |

## J — judgement cases · senior, manager (J02 — all roles)

| ID | Question | What they check | Follow-ups | Who |
| --- | --- | --- | --- | --- |
| J01 | A founder writes on Friday evening: we need X by Monday. What do you do? | pushback with data, reversible steps | — | mgr |
| J02 ★ | You need a decision, but there is no data. Give an example. | criticality × reversibility | — | all |
| J03 | Priorities change every week, and the team is tired. What do you do? | protecting the team, explicit trade-offs | — | mgr |
| J04 | What would you do in your first 90 days? | listen, measure, agree, show the result | — | all |
| J05 | What would you move to a shared platform, and what would you leave to teams? | platform thinking | — | mgr |

## K — culture, values, remote work · all roles

| ID | Question | What they check | Follow-ups | Who |
| --- | --- | --- | --- | --- |
| K01 | What is your management philosophy? How do you like to work? | values | — | mgr |
| K02 | Would a small team feel too small after a larger one? | motivation against the role | — | mgr |
| K03 | How do you work across time zones? | remote work | — | all |
| K04 | How do you handle stress and long hours? | balance | — | all |
| K05 | What kind of culture do you build? Give an example. | practices, not words | — | mgr |
| K06 | How do you like to be managed? What do you need from your manager? | fit with the manager | — | all |
| K07 | What is your ideal work environment? Where do you do your best work? | culture fit | — | all |
| K08 | What values matter most to you at work? | values against their values | Give an example. | all |

## S — stack and gaps · engineer, tech lead

| ID | Question | What they check | Follow-ups | Who |
| --- | --- | --- | --- | --- |
| S01 ◆ | What is your stack? | fit and honesty | — | all |
| S02 | Our stack is <X>. Have you worked with it? | reaction to a gap | How would you ramp up? | all |
| S03 | You have not worked in our domain. How will you get into it? | transfer of experience | — | all |
| S04 | How comfortable are you with infrastructure (cloud, Kubernetes, Linux)? | an honest limit | — | all |

## X — logistics · all roles

| ID | Question | What they check | Follow-ups | Who |
| --- | --- | --- | --- | --- |
| X01 ★ | Where are you based? Would you relocate? | location without dodging | — | all |
| X02 ★ | Do you need sponsorship? When can you start? | work authorization, timing | — | all |
| X03 ★ | What are your salary expectations? | a number, flexibility | That is the top of our range. | all |
| X04 | Are you in other processes? | urgency | — | all |
| X05 | Would your family move with you? | relocation risks | — | all |
| X06 | How would you like to be employed (contract, payroll)? | employment form | — | all |
| X07 | Do you have residence and work authorization where you live? | legal setup, audit | — | all |
| X08 | How did you hear about this role? | source, referral | — | all |

## Z — questions for the interviewer · all roles

«Do you have any questions for us?» comes in every interview: keep 2–3 questions ready for each stage.

| ID | Ask whom | Question |
| --- | --- | --- |
| Z01 | recruiter, HM | What does the team own today, and what would the new person take on first? |
| Z02 | recruiter | What will the hiring manager look for in the next conversation? |
| Z03 | recruiter | What are the next steps, and how long does the process usually take? |
| Z04 | HM, CTO | What three results would you expect from this role in six months? |
| Z05 | HM, CTO | Where does it hurt most right now? |
| Z06 | HM | How do you measure whether this area works well? |
| Z07 | engineer | Which team are you on, and what is the hardest part of your work right now? |

## Sources

- [UTK: 50 commonly asked interview questions](https://studentsuccess.utk.edu/career/students/develop-career-tools/interviewing/fifty-commonly-asked-interview-questions/)
- [Carleton: interview questions](https://www.carleton.edu/career/students/application/interviewing/questions/)
- [Inc.: 27 most common job interview questions](https://www.inc.com/jeff-haden/27-most-common-job-interview-questions-and-answers.html)
- [IGotAnOffer: software engineer behavioral questions](https://igotanoffer.com/blogs/tech/software-engineer-behavioral-interview-questions)
- [Big Interview: competency-based questions](https://www.biginterview.com/resources/competency-based-interview-questions)
- [Levels.fyi: Amazon Leadership Principles](https://www.levels.fyi/blog/amazon-leadership-principles.html)
- [Meta behavioral interview cheat sheet](https://www.techinterview.org/post/3233477365/meta-behavioral-interview-cheat-sheet/)
- [Exponent/Aced: top 30 engineering manager questions](https://www.aced.io/blog/top-30-engineering-manager-interview-questions)
- [Story bank: 5–8 STAR stories](https://dev.to/cvpilot/building-your-career-story-bank-5-to-8-star-stories-you-will-reuse-forever-38pj)

