# DIVE-PL

**A reproducible AI tool-chain methodology for building survey / questionnaire research studies.**

> Status: scaffold (v0.1.0) · Dual-licensed (MIT for code, CC BY 4.0 for content) · Case study: recreational divers in Poland

[![License: MIT](https://img.shields.io/badge/code-MIT-green.svg)](LICENSE-CODE)
[![License: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20977890.svg)](https://doi.org/10.5281/zenodo.20977890)

**Authors:** Łukasz Minarowski, MD, PhD ([ORCID](https://orcid.org/0000-0002-2536-3508)) · Jakub Matuk, BEng ([ORCID](https://orcid.org/0009-0002-8986-8609)) · Maksymilian Lech — Department of Respiratory Physiopathology, Medical University of Białystok, Poland

---

## What this is

DIVE-PL is a **methods / framework project**: it specifies and demonstrates an end-to-end, fully reproducible pipeline for designing, fielding and analysing questionnaire-based research using an integrated chain of AI tools, wrapped in an open-science layer that makes every step independently verifiable.

The **contribution is the integration**, not any single technique. Each component has prior art (see [`docs/related-work.md`](docs/related-work.md)); to our knowledge the *combination* of all four components plus a full open-science reproducibility layer has not been published as a single survey-study methodology (literature scan, mid-2026).

## How it works — human-led, AI-assisted

1. **Investigators (authors)** — design and orchestrate the study: research questions, protocol, item content, registration, interpretation. This is human work.
2. **GPT-5.5 (*LLM-as-judge*)** — independently reviews survey items for clarity, bias, double-barrelled wording, and content-validity relevance; fixes loop back to the investigators.
3. **Claude / Cowork** — builds and operates the approved instrument in REDCap via MCP / browser automation, under investigator direction.
4. **REDCap + AI-assisted dashboards (Python / React)** — de-identified electronic data capture (consent / RODO) and aggregated analytics, published openly.

**Human-in-the-loop at every step:** AI tools assist, execute, and review; investigators decide and approve. AI tools are not co-authors.

See [`docs/architecture.mmd`](docs/architecture.mmd) and [`METHODOLOGY.md`](METHODOLOGY.md).

## Open-science layer (the reproducibility "checkmate")

| Channel | Purpose |
|---|---|
| **GitHub** (this repo) | methodology, code, instrument definitions, prompts |
| **Zenodo** | archival DOI per release (citable artifact) |
| **OSF** | project page + preregistration of the case study |
| **GitHub Pages** | live public site + analytics dashboard (`docs/`) |

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
    index.html              # GitHub Pages site (Overview + nav)
    survey.html             # Case study — the DIVE-PL diving survey (live)
    methodology.html  pipeline.html  related-work.html
    reproduce.html  limitations.html  cite.html
    assets/                 # style.css, favicon.svg
    .nojekyll
    case-study-survey.md    # survey description (aim, sections, hypotheses)
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

## Case study — the DIVE-PL diving survey

The framework is demonstrated on a cross-sectional online survey of recreational divers in Poland: health status, physical fitness (VO2max via the University of Houston Non-Exercise Test), safety knowledge (DCS, barotrauma, safe-diving rules), risky behaviours, and self-reported adverse events. Aim, design, instrument sections, hypotheses (H1–H3), endpoint and analysis are described in [`docs/case-study-survey.md`](docs/case-study-survey.md) (live: [Case study page](https://kicrazom.github.io/DIVE-PL/survey.html)).

The study is ethics-approved and registered (see [`docs/CLINICAL_TRIALS.md`](docs/CLINICAL_TRIALS.md)). No participant data are stored in this repository.

## How to cite

See [`CITATION.cff`](CITATION.cff) and DOI [10.5281/zenodo.20977890](https://doi.org/10.5281/zenodo.20977890). Authors are listed under the title above.
