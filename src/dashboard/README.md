# src/dashboard/ — Stage 4: analytics & aggregate dashboard

Reference implementation of **Stage 4** of the DIVE-PL framework (see
[`../../METHODOLOGY.md`](../../METHODOLOGY.md) §5). AI-assisted, reproducible analysis
code plus an interactive dashboard that displays **aggregated, de-identified data
only**. The public face is the static site under [`../../docs/`](../../docs/); this
directory is the runnable reference an investigator uses over a real export.

## Files

| File | What it does | Dependencies |
|---|---|---|
| `scoring.py` | Faithful Python mirror of the REDCap `calc` fields in `../redcap/data_dictionary_v4.csv` — BMI, non-exercise VO₂max (Houston), IPAQ-SF MET + category, DASI score/VO₂peak/METs, VSAQ, safety-knowledge score. Pure functions, no I/O. | stdlib only |
| `aggregate.py` | Reads a REDCap export, derives scores, writes `summary.json` with **only** aggregates and **small-cell suppression** (k-anonymity). Refuses to run if the export still has identifier columns. | stdlib only |
| `app.py` | Minimal Streamlit dashboard over `summary.json`. Never reads raw rows. | `streamlit` |
| `requirements.txt` | Dependencies (only the app needs Streamlit). | — |

## Pipeline

```
REDCap export (de-identified, OUTSIDE git)
        │  python aggregate.py --input export.csv --output summary.json --k 5
        ▼
summary.json  (aggregates only, small cells suppressed)
        │  streamlit run app.py -- --summary summary.json
        ▼
interactive dashboard  ──(publish summary.json only)──▶ ../../docs/ (GitHub Pages)
```

## Scoring fidelity

`scoring.py` reproduces the exact REDCap formulas (extracted from the v4 data
dictionary), so offline analysis matches on-capture computation and the scoring logic
is independently auditable rather than buried in the REDCap project. Examples:

- `vo2max_estimated` — University of Houston non-exercise model; **estimated, not
  measured** (validity limitation to disclose in any paper).
- `dasi_score` — weighted DASI items (0–58.2); `dasi_vo2peak = 0.43·score + 9.6`.
- `ipaq_total_met` — `8·d·min (vig) + 4·d·min (mod) + 3.3·d·min (walk)`; low/moderate/high
  per the IPAQ-SF protocol.
- `knowledge_pct` — 10-item answer key → 0–100 %.

## Privacy (RODO/GDPR) — non-negotiable

- The dashboard shows **aggregates only**; raw rows never enter `summary.json`.
- `aggregate.py` suppresses any cell with `n < k` (default `k = 5`) and reports how
  many respondents were hidden.
- It **refuses** to process an export containing identifier columns (IP, e-mail, name,
  PESEL, phone, address, REDCap survey identifier).
- Exports live outside git (repo `.gitignore`); only `summary.json` may be published.

## Reproduce

```bash
pip install -r requirements.txt
python aggregate.py --input /path/to/deidentified_export.csv --output summary.json
streamlit run app.py -- --summary summary.json
```

## Status

Reference scoring + aggregation + app are in place. A React/Pages build that embeds a
published `summary.json` into `../../docs/` is a follow-up (the static site already
hosts the case-study pages).
