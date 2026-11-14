# Payouts: failed payouts at Fintrek

#### PAY-S1 · The whole story
`S` · reliability, payments, hardest problem · ~30 s
- EN: At Fintrek, about two percent of our payouts failed and finance fixed them by hand. I was the engineering manager of the payments team, seven engineers and a QA. I read the payout logs myself and found that our retries sent the same payout twice when the bank was slow. I proposed one idempotency key per payout, and the team built it. By the third quarter, failed payouts fell from 2.1% to 0.4%.
- RU: В Fintrek около двух процентов выплат падали, и финансы чинили их руками. Я была EM платёжной команды: семь инженеров и QA. Сама прочитала логи выплат и нашла, что ретраи отправляли одну выплату дважды, когда банк тормозил. Предложила один идемпотентный ключ на выплату, команда его сделала. К третьему кварталу доля упавших выплат снизилась с 2,1% до 0,4%.

#### PAY-O1 · First line
`O` · reliability · ~5 s
- EN: At Fintrek, about two percent of our payouts failed, and finance fixed them by hand.
- RU: В Fintrek около двух процентов выплат падали, и финансы чинили их руками.

#### PAY-A1 · What I did
`A` · hands-on · ~8 s
- EN: At Fintrek, I read the payout logs myself and found that our retries sent the same payout twice when the bank was slow.
- RU: В Fintrek я сама прочитала логи выплат и нашла, что ретраи отправляли одну выплату дважды при задержках банка.

#### PAY-R1 · Result
`R` · `D` · result · ~6 s
- EN: At Fintrek, failed payouts fell from 2.1% to 0.4% between the first and the third quarter, by the finance dashboard.
- RU: В Fintrek доля упавших выплат снизилась с 2,1% до 0,4% с первого по третий квартал, по дашборду финансов.

#### PAY-L1 · Lesson
`L` · lesson · ~6 s
- EN: Since Fintrek, I check retries for idempotency in every design review.
- RU: После Fintrek я проверяю ретраи на идемпотентность в каждом дизайн-ревью.

#### PAY-C2 · On-call
`C` · `A` · on-call, incidents · ~8 s
- EN: At Fintrek, the payments team ran a weekly 24/7 on-call rotation, and I took a shift too.
- RU: В Fintrek платёжная команда держала круглосуточное дежурство по неделям, и я тоже брала смены.
