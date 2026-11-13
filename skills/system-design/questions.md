# Questions before drawing — any design

We ask to ground ourselves: we do not know how the system and everything around it works. Every question changes something on the diagram; what changes nothing is said as an assumption. Start with «**Before I draw, a few questions that change the design.**» Answers go on the board at once.

| Where we look | Ask | What it changes on the diagram |
| --- | --- | --- |
| Input | How does it reach us, and is that the only way? Where does the data live today? | write paths, source of truth, outbox / CDC / replica |
| What the input carries | Does it carry the full state or only an ID? Does it know our user? | take the truth from the source; the lookup key |
| Guarantees | Is it worse to lose it or to do it twice? Money: is it worse to be late or to pay too much? | outbox, idempotency key, fail open / fail closed |
| Time | Seconds, minutes, or once a day? Is there a cut-off? | synchronous / workers / a scheduled job |
| Volume | How many a day, what peak, how many targets per item? | numbers for the scale step, a row per recipient |
| Reads | How many reads per write, and how fast must a read be? | cache, a ready answer (read model) |
| Our failure | When we are down, is it better to answer with old data or to refuse? | fail open / fail closed, TTL |
| Consumers | Who uses the result? Does another team need it too? | adapters; a log (Kafka); events or an API instead of our tables |
| Data model | Can one X have many Y? Is this ID unique globally or per customer? | separate tables; (tenant_id, id) in every key |
| History | Do we need every change: audit, replay, refunds? | facts / ledger / events; a correction is a new record |
| Someone else's system | Does it retry, send duplicates, keep order, take an idempotency key, have rate limits? | deduplication, an «unknown» status, a rate limiter, reconciliation |
| Reconciliation | What comes back that lets us check ourselves? | a daily reconciliation, a mismatch queue with an owner |
| The past | Can past data change, for example a refund or late data? | rebuilding the last N days by overwrite |
| Changes at the source | If nobody tells us about a change, how often must we notice it? | scheduled polling, keeping the previous state and comparing |

## Choosing 4–5 START questions
- **The base four:** input, guarantees, time, volume. If one answer is obvious from the task, do not ask — say it as an assumption and give the place to a question for this type of task.
- **Plus 1–2 by type:** event delivery — consumers; money — «late or too much» and reconciliation (they decide the skeleton); state and access — what the input carries and reads; metrics — what we count and where the data is; an external source without notifications — changes at the source.
- **4–5 in total, 6 at most.** The rest is LATER.

## Assumptions aloud — do not ask
- «One database per service; other teams get events or an API, not our tables.»
- «Exactly once is not possible over a network: at-least-once and deduplication by ID.»
- «I will not promise strict order; every event has an ID and a timestamp.»
- «Analytics never runs on the production database.»
- A business rule is unclear and the answer is «your call» → «Then I assume X», and write it on the board.

## Do not ask
- «Which database should I use? Should I use Kafka?» — that is your decision.
- How someone else's system works inside — it has its own API and limits and can be down; that is enough.
- Ten questions in a row — START first, the rest as you go.

## After the questions
«Let me sum up what I heard…» — 3–4 answers in one sentence, then the skeleton.
