# src/reviewer/ — Stage 2: independent item review (LLM-as-judge)

Reference implementation of **Stage 2** of the DIVE-PL framework (see
[`../../METHODOLOGY.md`](../../METHODOLOGY.md) §3). An **independent** LLM — kept
separate from whatever model helped draft the items — evaluates each survey item
against explicit criteria and returns structured flags plus suggested fixes. The
investigators adjudicate; the model never has the final word.

Reference model: **GPT-5.5** (any capable model works — the point is *independence*
from the drafting model, to reduce self-confirmation bias).

## Why a separate reviewer

Drafting and reviewing with the same model tends to ratify its own choices. DIVE-PL
keeps the roles apart on purpose: one model (with the investigators) drafts; a
*different* model reviews. This mirrors the editorial separation of author and
reviewer and is the single most important design rule of this stage.

## What it is NOT

- **Not a replacement for human content validity.** Where formal content validity
  is required, LLM relevance ratings may be reported *alongside* — never instead of
  — a human expert panel (e.g. I-CVI / S-CVI). The rubric emits a relevance rating
  precisely so it can be tabulated next to the human panel, not substituted for it.
- **Not an approval gate.** Every flag loops back to the investigators, who decide.

## Files

| File | What it is |
|---|---|
| `rubric.md` | The seven explicit evaluation dimensions, each with what to check, severity levels, and worked good/bad examples. |
| `item_review_prompt.md` | The prompt template that operationalises the rubric, including the required structured (JSON) output schema so flags are machine-collatable and diff-able across rounds. |

## Workflow

```
approved-draft items ──▶ reviewer (LLM, rubric.md + item_review_prompt.md)
                              │
                              ▼
                    structured flags + suggested fixes (JSON)
                              │
                              ▼
                    investigators adjudicate ──▶ revise items ──▶ re-review until clean
```

Run it per item or per batch. Persist the JSON output under version control so the
number of review rounds and the issues caught become **process metrics** for the
methodology evaluation (METHODOLOGY §… / thesis §5.1).

## Reproducibility

Prompts and rubric are plain text and versioned, so any third party can re-run the
same review against the same items and compare. Record the model name + version and
the rubric commit hash alongside each review batch.
