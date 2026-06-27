# Item-review rubric (DIVE-PL Stage 2)

Each survey item is scored on **seven dimensions**. For every dimension the reviewer
returns a severity and, when severity is not `ok`, a concrete suggested rewrite. The
reviewer flags problems; the investigators decide.

Severity scale (applies to every dimension):

| Severity | Meaning |
|---|---|
| `ok` | No issue. |
| `minor` | Worth improving; would not by itself invalidate the item. |
| `major` | Likely to bias responses or be misread by a meaningful share of respondents. |
| `blocker` | Item should not be fielded as written. |

The reviewer must also emit an overall `relevance` rating (see dimension 7) on a
1–4 content-validity scale, so LLM ratings can be tabulated next to a human expert
panel (I-CVI). This is reported *alongside*, never instead of, the human panel.

---

## 1. Clarity / comprehensibility

**Check:** Can a respondent in the target population (here: Polish recreational
divers, general public reading level) understand the item on first read? Watch for
jargon, undefined acronyms, nested clauses, and reading level above ~B1/B2.

- ❌ "Czy stosujesz profilaktykę dekompresyjną zgodną z aktualnymi algorytmami RGBM?"
- ✅ "Czy podczas wynurzania robisz przystanek bezpieczeństwa (zwykle 3 min na 5 m)?"

## 2. Ambiguity

**Check:** Could the item be read in more than one way? Vague quantifiers
("regularnie", "często", "zwykle"), unclear referents, undefined time windows.

- ❌ "Czy często nurkujesz głęboko?"  *(„często"? „głęboko"? over what period?)*
- ✅ "W ciągu ostatnich 12 miesięcy, ile nurkowań poniżej 30 m wykonałeś/aś?"

## 3. Double-barrelled phrasing

**Check:** Does the item ask about two things at once, so a single answer cannot
cleanly map to either? Look for "i / oraz / a także" joining two distinct concepts.

- ❌ "Czy czujesz się zdrowy i dobrze wytrenowany?"  *(health AND fitness — split)*
- ✅ Two items: one on health status, one on training status.

## 4. Leading / loaded wording

**Check:** Does the phrasing push toward an answer, presuppose a fact, or carry an
emotional charge? Assumptive framing ("Jak bardzo…"), social-desirability pressure,
or value-laden adjectives.

- ❌ "Czy odpowiedzialnie sprawdzasz sprzęt przed każdym nurkowaniem?"  *("odpowiedzialnie" loads it; social desirability)*
- ✅ "Przed ostatnim nurkowaniem — czy wykonałeś/aś kontrolę sprzętu przed wejściem do wody?"

## 5. Cultural / contextual bias

**Check:** Does the item assume context not universal in the target population
(equipment, certification system, climate, idioms, units)? For a Polish sample:
certification ladders (CMAS vs PADI vs SSI), local dive sites/conditions, metric
units, PL-specific phrasing.

- ❌ Assuming everyone uses Imperial depth or a single agency's terminology.
- ✅ Neutral, agency-agnostic wording; metric units; examples spanning common PL agencies.

## 6. Response-option balance & completeness

**Check (for closed items):** Are options mutually exclusive, collectively
exhaustive, and symmetric? Is there a needed "nie wiem / nie dotyczy / wolę nie
podawać"? Are Likert anchors balanced (equal positive/negative)? Do numeric ranges
overlap or leave gaps?

- ❌ Ranges "0–5, 5–10, 10–20" (overlap at 5 and 10; gap above 20).
- ✅ "0–4, 5–9, 10–19, 20+"; balanced Likert; explicit "nie dotyczy" where relevant.

## 7. Content-validity relevance (rate 1–4)

**Check:** How relevant is this item to the construct it is meant to measure (e.g.
an IPAQ item → habitual physical activity; a knowledge item → safety knowledge)?
Rate on the standard content-validity scale; this rating feeds I-CVI alongside the
human panel.

| Rating | Meaning |
|---|---|
| 1 | Not relevant |
| 2 | Somewhat relevant (item needs major revision) |
| 3 | Quite relevant (minor revision) |
| 4 | Highly relevant |

Items rated 1–2 are flagged for the investigators; final relevance is decided by the
human expert panel, with LLM ratings reported as a secondary column only.

---

## Output contract

For each item the reviewer returns, per the schema in `item_review_prompt.md`:
a per-dimension `{severity, comment, suggested_rewrite?}`, the dimension-7
`relevance` integer (1–4), an `overall_severity` (max across dimensions), and a
short `summary`. No prose outside the JSON object.
