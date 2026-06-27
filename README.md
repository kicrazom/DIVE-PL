# DIVE-PL

**A reproducible AI tool-chain methodology for building survey / questionnaire research studies.**

> Status: scaffold (v0.1.0) · Dual-licensed (MIT for code, CC BY 4.0 for content) · Case study: recreational divers in Poland

[![License: MIT](https://img.shields.io/badge/code-MIT-green.svg)](LICENSE-CODE)
[![License: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20977890.svg)](https://doi.org/10.5281/zenodo.20977890)

---

## What this is

DIVE-PL is a **methods / framework project**: it specifies and demonstrates an end-to-end, fully reproducible pipeline for designing, fielding and analysing questionnaire-based research using an integrated chain of AI tools, wrapped in an open-science layer that makes every step independently verifiable.

The **contribution is the integration**, not any single technique. Each component has prior art (see [`docs/related-work.md`](docs/related-work.md)); to our knowledge the *combination* of all four components plus a full open-science reproducibility layer has not been published as a single survey-study methodology (literature scan, mid-2026).

## The four-component pipeline

1. **LLM agent (Claude / Cowork)** — designs and orchestrates the study: protocol, item drafting, registration artifacts, workflow.
2. **LLM reviewer (GPT, *LLM-as-judge*)** — independently reviews/validates survey items for clarity, bias, double-barrelled wording, and content-validity relevance.
3. **REDCap** — electronic data capture: the validated instrument, consent / RODO logic, and de-identified data store.
4. **AI-built analytics dashboards (Python / React)** — interactive analysis and reporting, published openly.

All four operate **human-in-the-loop**: AI augments and is verified by a domain expert; it does not replace expert judgment.

See [`docs/architecture.mmd`](docs/architecture.mmd) and [`METHODOLOGY.md`](METHODOLOGY.md).

## Open-science layer (the reproducibility "checkmate")

| Channel | Purpose |
|---|---|
| **GitHub** (this repo) | methodology, code, instrument definitions, prompts |
| **Zenodo** | archival DOI per release (citable artifact) |
| **OSF** | project page + preregistration of the case study |
| **GitHub Pages** | live, public analytics dashboard (`site/`) |

The open-science stack is standard FAIR practice — **not** claimed as novel; it is what makes the integrated framework reproducible.

## Repository structure

```
DIVE-PL/
  README.md
  METHODOLOGY.md            # the framework, stage by stage
  LICENSE                   # CC BY 4.0 (content)
  LICENSE-CODE              # MIT (code)
  LICENSING.md              # which license applies where
  CITATION.cff              # how to cite
  AI_USAGE_DISCLOSURE.md    # transparency: which AI did what
  RELEASES.md               # changelog / release notes
  .zenodo.json              # Zenodo deposit metadata
  .gitignore / .gitattributes
  docs/
    index.html              # GitHub Pages landing / dashboard
    .nojekyll
    related-work.md         # component -> nearest precedent -> our difference
    architecture.mmd        # pipeline diagram (Mermaid)
    open-science-checklist.md
    thesis-outline.md       # engineering-thesis (PL) IMRaD skeleton
    CLINICAL_TRIALS.md      # registration details
  src/
    README.md               # code map (agent / reviewer / redcap / dashboard)
  data/
    README.md               # data governance (RODO/GDPR) — NO PII in repo
```

## Case study

The framework is demonstrated on a cross-sectional online survey of recreational divers in Poland (health, fitness via a non-exercise VO2max proxy, safety knowledge, self-reported adverse events). The study is ethics-approved and registered (see [`docs/CLINICAL_TRIALS.md`](docs/CLINICAL_TRIALS.md)). No participant data are stored in this repository.

## How to cite

See [`CITATION.cff`](CITATION.cff). A Zenodo DOI is minted on the first tagged release.

## Authors

**Łukasz Minarowski, MD, PhD** — Department of Respiratory Physiopathology, Medical University of Białystok, Poland · ORCID [0000-0002-2536-3508](https://orcid.org/0000-0002-2536-3508)
**Jakub Matuk**
**Maksymilian Lech**
