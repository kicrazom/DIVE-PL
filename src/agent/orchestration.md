# Orchestration — the human-led loop (DIVE-PL Stage 1)

Stage 1 is where the investigators run the study; the AI agent assists. This note
describes the loop and the gates so the process is reproducible — it is **not** an
automation spec. Every arrow labelled *gate* is a human decision.

```
        ┌──────────────────────────────────────────────────────────┐
        │  Investigators (own the study; decide at every gate)      │
        └──────────────────────────────────────────────────────────┘
                   │ topic + constraints
                   ▼
   [prompt_01]  decompose research question ──gate──▶ PECO + H1–H3 + constructs approved
                   │ approved construct
                   ▼
   [prompt_02]  draft items ───────────────────────▶ candidate items
                   │
                   ▼
   Stage 2     reviewer (../reviewer/) — DIFFERENT model ──▶ JSON flags + rewrites
                   │
                   ▼
              investigators adjudicate ──gate──▶ revise; re-review until no major/blocker
                   │ clean, approved items
                   ▼
   [prompt_03]  scaffold protocol / consent / RODO ──gate──▶ investigators + IOD/ethics finalise
                   │ approved instrument + documents
                   ▼
   Stage 3     REDCap build (../redcap/) — agent builds under direction
                   │ fielded, de-identified export
                   ▼
   Stage 4     dashboard (../dashboard/) — aggregated results only
```

## Gates (human, non-skippable)

1. **Question gate** — PECO + hypotheses approved before any item is drafted.
2. **Review gate** — no item reaches REDCap with an unresolved `major`/`blocker`
   reviewer flag; the investigators adjudicate every flag.
3. **Ethics/RODO gate** — protocol, consent, and RODO sheet approved by the
   investigators and the institution (bioethics committee, DPO/IOD) before fielding.
4. **Privacy gate** — only aggregated, de-identified data leaves Stage 4 to the public
   dashboard (see the repo open-science checklist §5).

## Separation of models (anti self-confirmation)

The drafting model (Stage 1) and the reviewing model (Stage 2) are **deliberately
different**. Do not let the model that wrote an item also be the one that signs off on
it. This separation is the core methodological safeguard of DIVE-PL.

## Reproducibility record

For each session log: model name + version, the prompt file commit hash, date, and the
investigator decision. These become the process metrics (rounds, issues caught,
time-to-instrument) reported in the methods paper (thesis §5.1).
