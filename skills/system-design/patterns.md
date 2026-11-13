# Common designs — in short

The patterns that come up most often in system design for backend engineers and engineering managers.

## 1. Delivering events to external systems (webhooks, integrations)
The change and an outbox row in one transaction → a relay or CDC → a log (Kafka) keyed by user → a router writes the event to `events` (history, replay) and a `deliveries` row per recipient with UNIQUE (event_id, destination_id); the offset is committed after → workers take rows with a short lease (SKIP LOCKED), retries with backoff and jitter, after N attempts — dead and a manual retry. A slow recipient is isolated: a worker limit and a token bucket per recipient key. No promise of strict order: an event_id and a timestamp in every event; the recipient can re-read the state through the API.

## 2. A payments API + ledger + bank reconciliation
- **API:** an idempotency key from the client, UNIQUE (merchant_id, idempotency_key); a retry with the same key returns the same result.
- **Payment states:** created → pending → succeeded / failed / **unknown** (a bank timeout is not an error but «unknown»: find out, do not retry blindly).
- **Ledger:** double entry, entries that sum to zero, insert only; a correction is a new entry, never an edit. The balance is a sum of entries or a materialized view.
- **Bank:** an adapter per bank; bank responses and webhooks into a raw table with UNIQUE id; the bank's status is the truth.
- **Daily reconciliation:** import the statement → match by reference, amount and date → matched — closed; not — into a mismatch queue with an owner and a deadline. The bank's cut-off is in the schedule.
- **Money fails closed:** limits, a kill switch; a double payout is SEV1. Events go out through an outbox (pattern 1).

## 3. Payouts and advances against future revenue
A scheduled job computes the available amount (a share of earnings minus debt, limits, a kill switch) → a payout service: the payout and its ledger entry in one transaction, idempotent by (client, date) → the bank. Repayment is a separate step, when the money has arrived and is in both the report and the statement. Reconciliation across three sources: own records, the money source's reports, the bank statement.

## 4. Current state and an access API
The truth is at an external source (an app store, a payment system). Two write paths: synchronous (the client reports a purchase → check with the source) and notifications (ingest with a signature check → a raw table with UNIQUE id → a handler). Both write facts and rebuild the state under a per-user lock, and never write older source data (the source's state time). Reads come from a ready view and a cache (delete the key after commit; TTL as insurance). Access fails open only when our own API does not answer. Missed notifications — catch up through the source's history and reconciliation.

## 5. Polling an external source without notifications
Each record has `next_check_at` → a scheduler hands out tasks (SKIP LOCKED) → a worker takes the full state from the source → compares it with the stored one (a hash of the last response: equal — done) → the difference becomes events, event_id = hash(external id, type), inserting a duplicate does nothing. Count the load at once: N records a day / 86,400 = requests per second. Reduce it: do not poll dead records, check right after an expected change, jitter, a limit per source API key.

## 6. Metrics and charts
The source is a replica or CDC, never the main database → daily aggregates (client × day) → a charts API with a cache. Late data and refunds — rebuild the last N days by overwrite; a recount is published whole. At scale: CDC → a log → storage → a columnar database and transformations.

## 7. A shared rate limiter
A token bucket in shared storage (Redis) per the key the recipient limits (API key, host), not per our client: refill tokens for the elapsed time and take one in one atomic script. No token — postpone without increasing the attempt counter. A 429 with Retry-After outranks our own limit.

## Typical building blocks
Outbox in the same transaction; relay or CDC; a queue or a log (Kafka on a signal: several consumers or offloading the main database); a delivery row per recipient with UNIQUE; retries with backoff and jitter; dead and a manual retry; isolation of a slow recipient; idempotency by key; a cache with the key deleted after commit; a ledger where a correction is a new record; reconciliation; fail open for access, fail closed for money.
