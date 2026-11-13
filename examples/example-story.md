# Example: one story → blocks → three answers

The candidate is made up (Alex, an EM at the made-up marketplace Shoply; native language Russian, so every block has an `RU:` line). The example shows how a story becomes blocks and how answers to different questions are built from the same blocks.

## What the candidate said (as it was)

«At Shoply our checkout went down about once a week, especially during sales. I was the EM of the payments team then, six people. I sat down myself and looked at the logs and traces — it turned out we called the payment provider synchronously, and when it was slow our connection pool filled up. I proposed a queue and retries with an idempotency key; the team built it in three weeks. The outages went away, and sales conversion grew by 4% — the analysts counted it, comparing with the previous sale. Today I would put an alert on the queue straight away; we only added it a month later.»

Claude's follow-ups (in one message): what exactly did you do yourself? how was the 4% measured? how long did an outage last? what was the team's part and what was yours? anything not to say?

## Blocks

#### CHK-S1 · The whole story
`S` · incident, payments · ~25 s
- EN: At Shoply, our checkout went down almost every week, worst of all during sales. I was the engineering manager of the payments team, six engineers. I went through the logs and traces myself: we called the payment provider synchronously, and its delays filled our connection pool. I proposed a queue with retries and an idempotency key, and the team built it in three weeks. The outages stopped, and sales-day conversion grew by 4%.
- RU: В Shoply чекаут падал почти каждую неделю, хуже всего — в распродажи. Я был EM платёжной команды, шесть инженеров. Сам прошёл логи и трейсы: мы ходили в платёжного провайдера синхронно, и его задержки забивали пул соединений. Предложил очередь с ретраями и идемпотентным ключом, команда сделала за три недели. Падения прекратились, конверсия в распродажу выросла на 4%.

#### CHK-O1 · First line
`O` · incident, reliability · ~5 s
- EN: At Shoply, our checkout went down almost every week, worst of all during sales.
- RU: Чекаут падал почти каждую неделю, хуже всего — в распродажи.

#### CHK-C1 · Who I am and the scale
`C` · team · ~4 s
- EN: I was the engineering manager of the payments team, six engineers.
- RU: Я был EM платёжной команды, шесть инженеров.

#### CHK-A1 · Investigated myself
`A` · hands-on, debugging · ~8 s
- EN: I went through the logs and traces myself. We called the payment provider synchronously, and when it slowed down, our connection pool filled up.
- RU: Сам разобрал логи и трейсы: ходили в провайдера синхронно, и при его задержках забивался пул соединений.

#### CHK-A2 · The fix
`A` · design · ~6 s
- EN: I proposed a queue with retries and an idempotency key, and the team built it in three weeks.
- RU: Предложил очередь с ретраями и идемпотентным ключом, команда сделала за три недели.

#### CHK-R1 · The result
`R` · business impact · ~6 s
- EN: After the queue, the outages stopped, and sales-day conversion grew by 4%.
- RU: Падения прекратились, конверсия в распродажу выросла на 4%.

#### CHK-D1 · How it was measured
`D` · metrics · ~5 s
- EN: Our analysts compared the sale with the previous one.
- RU: Считали аналитики, сравнивали с прошлой распродажей.

#### CHK-L1 · What I would do differently
`L` · lessons · ~6 s
- EN: Today I would add an alert on the queue from day one. We added it a month later.
- RU: Сейчас сразу поставил бы алерт на очередь — мы добавили его только через месяц.

## Three answers from the same blocks

| Question | Chain | Why this way |
| --- | --- | --- |
| T03 Hardest technical problem | `CHK-O1 → CHK-A1 → CHK-A2 → CHK-R1` | the focus is the investigation and the fix |
| T06 Incident you handled | `CHK-O1 → CHK-C1 → CHK-A1 → CHK-R1 → CHK-L1` | the role, the order of actions, the lesson |
| U03 Close to the customer / business impact | `CHK-O1 → CHK-R1 → CHK-D1 → CHK-A2` | business first, then the technology |

The first line is the same for every question, but the meaning of the answer differs: it is set by the order of the blocks and by what is left out.
