# Message skeletons

Short replies the candidate sends in a thread: follow-ups, answers to recruiters, thank-you notes, an offer reply. Claude fills `<…>` from the pack and the tracker, never with a fact that is not in the pack; the text then goes through `english-register` (the script) and the candidate's `never-say.md`. A first note to a stranger is not here: it is built by `outreach` §4.

- **Language:** the vacancy's. In another language, that language's conventions (formal address, salutation, closing: `outreach` §4).
- **Thread:** reply in the same ATS or mail thread; keep the subject as it is («Re: …»). A new mail only when there is no thread; then the subject names the role: «<role> — <candidate name>».
- **Form:** «Hi <first name>,» (a formal culture or an unknown name: «Dear <title> <last name>,» / «Dear <company> team,»), the body, «Best regards,» and the name. No questions about money, currency, location, visa or remote (`outreach` §4).
- **Dates:** a weekday with a date is checked before the draft is shown (`python3 -c "import datetime; print(datetime.date(2026, 11, 18).strftime('%A'))"`).

## Follow-up 1 — application + 10 days
> Hi <first name>,
>
> On <date> I applied for the <role> role at <company>. <One new fact from the pack that answers a requirement, or nothing.> I am still very interested in the role.
>
> Best regards,
> <name>

## Follow-up 2 — the last one, +14 days
> Hi <first name>,
>
> I am writing once more about my application for the <role> role. If the role is still open, I would be glad to talk.
>
> Best regards,
> <name>

## A recruiter asks for times
> Hi <first name>,
>
> Thank you for the invitation. I am available on <weekday, date> from <time> to <time> and on <weekday, date> from <time> to <time>, <time zone>. Any of these times works for me.
>
> Best regards,
> <name>

## After an interview — the same day
> Hi <first name>,
>
> Thank you for the conversation today. I enjoyed discussing <one topic from the call>. <One sentence that links it to a fact from the pack, or nothing.> I am looking forward to the next steps.
>
> Best regards,
> <name>

## A salary question in writing
By `money.approach` and the candidate's money recipe (X03 in `me/recipes.md`); never the floor, no question mark.
- Flexible:
  > I am flexible on the salary. I would like to understand the scope of the role and your range for it first.
- Naming a number:
  > I am looking at about <money.say_aloud> base, plus bonus and equity. I am flexible on the mix.

## A rejection
> Hi <first name>,
>
> Thank you for letting me know, and for your time. I enjoyed learning about <the team or the product>. If a similar role opens later, I would be glad to hear from you.
>
> Best regards,
> <name>

## Asking for more time on an offer
> Hi <first name>,
>
> Thank you for the offer. I am in the final stage of another process and expect an answer by <date>. Could you give me until <date> to reply?
>
> Best regards,
> <name>

## Withdrawing
> Hi <first name>,
>
> Thank you for your time on my application for the <role> role. I have decided to withdraw from the process. I wish you and the team all the best.
>
> Best regards,
> <name>

## Declining an offer
> Hi <first name>,
>
> Thank you for the offer and for the time your team spent with me. I have decided to accept another role. I hope we can stay in touch.
>
> Best regards,
> <name>

## Accepting an offer
The candidate sends it; no rule covers it (`CLAUDE.md` §5).
> Hi <first name>,
>
> Thank you. I am happy to accept the offer for the <role> role. Please send me the next steps and the documents to sign.
>
> Best regards,
> <name>
