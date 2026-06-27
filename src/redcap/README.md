# src/redcap/ — Stage 3: instrument build & data capture

Reference implementation of **Stage 3** of the DIVE-PL framework (see
[`../../METHODOLOGY.md`](../../METHODOLOGY.md) §4): once the investigators approve
the items, the instrument is built and operated in REDCap — data dictionary,
branching logic, consent, RODO collapsible, validation rules — under investigator
direction.

These artifacts are the **case study** instrument (recreational divers in Poland).
They are committed as a worked example of the framework, not as a generic library.

## Files

| File | What it is |
|---|---|
| `data_dictionary_v4.csv` | Final REDCap data dictionary, **136 fields**. Importable as-is into a REDCap project. Polish UI (Tak/Nie radios), Stop Actions on eligibility items, 8 survey instruments, `@HIDDEN-SURVEY` on all scoring/derived fields, hidden answer key for the knowledge block. |
| `add_fitness.py` | Builds the fitness/physical-activity module on top of the base dictionary: **IPAQ-SF** (7 items), **VSAQ** (self-reported MET capacity), full **DASI-12**, plus an exploratory dive-functional block — and the derived calc fields (MET-min/week, DASI score, estimated VO₂peak). All derived fields are `@HIDDEN-SURVEY`. |
| `fix_dd.py` | Methodological/technical transform pass: hides the knowledge-block answer key as a field annotation, applies `@HIDDEN-SURVEY` to scoring fields, splits lifetime vs 24-month outcomes, adds RODO notices to free-text fields, and preserves the REDCap export column order/format. |

## How the pieces fit

```
base dictionary ──▶ fix_dd.py ──▶ add_fitness.py ──▶ data_dictionary_v4.csv
  (initial items)   (methodology    (fitness module    (final, importable)
                     + scoring        + derived calc
                     hiding + RODO)    fields)
```

The Python scripts are **idempotent dictionary transforms**: they read a REDCap
data-dictionary CSV, apply a defined set of changes, and write a new CSV that
re-imports cleanly. They do not touch participant records and require no API
credentials to run (pure CSV in / CSV out).

## Privacy (RODO/GDPR)

- The data dictionary is **instrument metadata** — it defines the questionnaire and
  contains **no participant responses**. It is whitelisted in the repo `.gitignore`
  (`!src/redcap/*.csv`); the blanket `*.csv` ignore still protects any exported data.
- Free-text fields carry explicit "do not enter identifying data" notices.
- Eligibility items use REDCap **Stop Actions** so non-eligible respondents end the
  survey without leaving superfluous data.
- The study is designed to be genuinely anonymous (no IP, no e-mail, no identifiers).

## Reproduce

1. Create a REDCap project (or use the project's Designer).
2. Import `data_dictionary_v4.csv` via *Designer → Data Dictionary → Upload*.
3. (Optional) To regenerate the dictionary from an earlier base, run
   `python fix_dd.py` then `python add_fitness.py` (adjust the input/output paths
   at the top of each script).

## Provenance

Built iteratively (v0 → v2 → v4) with Claude/Cowork under investigator direction;
item wording was reviewed in Stage 2 (see [`../reviewer/`](../reviewer/)) and
adjudicated by the investigators. Ethics: UMB Bioethics Committee approval
`APK.002.228.2026`; registered on ClinicalTrials.gov (2026-06-20).
