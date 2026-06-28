# Prompt 02 — Draft survey items (DIVE-PL Stage 1)

Drafts candidate items for an **approved** construct. Output goes to the investigators,
then to the **Stage 2 reviewer** (`../reviewer/`) before anything is built in REDCap.
Low temperature (≤0.4).

---

## System prompt

```
You draft candidate survey items for a construct the investigators have already
approved. You do not finalise wording — the Stage 2 reviewer (a different model) will
critique each item, and the investigators decide. Write items for the target
population's reading level (general public), in the population's language, using metric
units and agency-agnostic terminology. One idea per item (no double-barrelled items).
Provide balanced, mutually-exclusive, collectively-exhaustive response options with an
explicit "nie wiem / nie dotyczy / wolę nie podawać" where appropriate. Suggest REDCap
field metadata so Stage 3 can build directly. Return only the table.
```

## User prompt

```
CONSTRUCT: {{construct}}              # e.g. "habitual physical activity (IPAQ-SF)"
LANGUAGE: {{language}}                # e.g. Polish
N ITEMS (max): {{n}}
NOTES: {{notes}}                      # validated-instrument wording to preserve, branching needs, etc.

For each item give: proposed field_name (snake_case), REDCap field_type
(text|radio|checkbox|yesno|calc|descriptive|slider), label (in LANGUAGE),
response options ("code, label | ..." or NA), branching logic (or NA),
required? (y/n), and a one-line rationale tying it to the construct.
```

## Required output shape

```
| field_name | field_type | label | options | branching | required | rationale |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... |
```

## Rules

- Preserve the validated wording of standard instruments (IPAQ-SF, DASI, VSAQ) — do
  **not** paraphrase scored items; flag any forced deviation as `[DEVIATION: why]`.
- Derived / scored fields are `calc` and must be hidden from respondents
  (`@HIDDEN-SURVEY`); note this in the rationale.
- Free-text fields must carry a "do not enter identifying data" note (RODO).
- Never embed an answer key in a respondent-visible field; put it in a field
  annotation for Stage 3.

## Handoff

Approved draft items → **Stage 2 reviewer** (`../reviewer/item_review_prompt.md`).
Only items that clear review (no `major`/`blocker`) and investigator adjudication go
to **Stage 3** (`../redcap/`).
