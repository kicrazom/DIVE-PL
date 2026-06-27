# DIVE-PL methodology

This document specifies the framework. It is tool-agnostic where possible; the reference implementation uses Claude/Cowork, GPT, REDCap, and Python/React.

## 1. Design principles

- **Human-in-the-loop.** Every AI output is reviewed and approved by a domain expert before it affects the study. AI augments; it does not replace.
- **Separation of roles.** Drafting and review are kept distinct — investigators (with Cowork assistance) author; an independent model (GPT-5.5) reviews — reducing self-confirmation bias.
- **Reproducibility by construction.** Prompts, instrument definitions, code and analysis are version-controlled and archived with a DOI.
- **Privacy & sovereignty (RODO/GDPR).** No personally identifiable information (PII) enters the repository; anonymisation and local-first processing are defaults.
- **Transparency.** AI involvement is disclosed per artifact (see `AI_USAGE_DISCLOSURE.md`), in line with open-science norms and the EU AI Act's transparency expectations.

## 2. Stage 1 — Design & orchestration (investigators)

The investigators (authors) own this stage: research-question decomposition, item content, study protocol, registration artifacts (ClinicalTrials.gov / OSF), and consent / RODO text. Claude / Cowork may help draft and scaffold these artifacts, but the investigators decide, edit, and approve everything. Design and orchestration are human work.

## 3. Stage 2 — Independent item review (GPT-5.5, LLM-as-judge)

An independent LLM (GPT-5.5) evaluates each item against explicit criteria: clarity / comprehensibility, ambiguity, double-barrelled phrasing, leading / loaded wording, cultural bias, response-option balance, and content-validity relevance. The reviewer returns structured flags and suggested fixes that loop back to the investigators, who adjudicate. Where formal content validity is required, LLM relevance ratings may be reported alongside — never instead of — a human expert panel (e.g., I-CVI / CVI).

## 4. Stage 3 — Instrument build & data capture (Claude / Cowork + REDCap)

Once the investigators approve the items, Claude / Cowork builds and operates the instrument in REDCap — data dictionary, branching logic, consent, RODO collapsible, validation rules — via MCP / browser automation, under investigator direction. REDCap provides access control, an audit trail, and API access. De-identified exports feed Stage 4.

## 5. Stage 4 — Analytics dashboards (Python / React)

AI assists in generating reproducible analysis code and interactive dashboards (Streamlit / Dash / React) for descriptive statistics, hypothesis tests, and figures. Dashboards are published via GitHub Pages and display **aggregated, de-identified data only**.

## 6. Validation & quality control (the "Judge" pass)

Each stage carries a self-audit: source quality, double-counting / leakage, outdated assumptions, and unjustified extrapolation. AI-derived artifacts are explicitly labelled and separated from expert-verified ones.

## 7. Reporting caveats (state these in any paper)

- Much of the supporting evidence for LLM-as-reviewer and AI-built dashboards is **preprint-stage** — flag it.
- The literature is unanimous that AI here is a **complement with human oversight** — state explicitly to preempt reviewer pushback.
- For the case study specifically: VO2max is **estimated** (non-exercise test), not measured — a validity limitation to disclose.
