# A design card for system design

The order matches the round's frame and the one-page sheet: Scope → Contract → Simple → Scale → Failures → Wrap-up.

## <The task in one sentence, as the interviewer will say it>

**Likelihood and source:** high / medium / low — a review, the product, the interviewer's code, or «from the posting».

### 1. Questions and assumptions
| When | Question | Expected answer | What it changes on the diagram |
| --- | --- | --- | --- |
| START | | | |
| assumption aloud | (do not ask — say it) | — | |
| LATER | | | |

«Expected answer» only from reviews or the company's documentation; without a source, mark it «assumption» and do not present it as a fact about the company.

> Let me sum up what I heard: …

### 2. Contract and data
- API or inputs (2–3 calls / events):
- Tables with keys:

| Table | PK / UNIQUE | FK | Who writes | Who reads |
| --- | --- | --- | --- | --- |

### 3. Simple design (frame 1)
Participants left to right; tables under whoever writes them; a frame around one transaction.

### 4. Numbers and scale (frame 2)
- Assumptions about numbers (say them aloud): volume a day, peak, record size.
- The heaviest part and its number:
- What is added and on which signal (metric, threshold, what is cheaper first):

### 5. Failures (frame 3)
| What broke | What we see | What we do |
| --- | --- | --- |

### Variants with an assumption removed (2–3)
- If there is no <assumption 1>:
- If there is no <assumption 2>:

### Bridges to experience
Only from the candidate's blocks, with IDs: «At <company> I … (ID)». One or two sentences, each story at most once per round.

### 6. The summary in a minute (English, checked by the register script)
> …
