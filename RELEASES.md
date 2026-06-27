# Release notes

## Unreleased

- Reference implementation, first slices:
  - `src/redcap/` (Stage 3) — final data dictionary v4 (136 fields) + the
    `add_fitness.py` / `fix_dd.py` dictionary-transform scripts, with README.
  - `src/reviewer/` (Stage 2) — LLM-as-judge rubric, item-review prompt with a
    structured JSON output contract, and README.
- `.gitignore`: whitelist `src/redcap/*.csv` (instrument metadata, not participant data).
- Checklist/release notes reconciled with live state (DOI, Pages, public — see below).

### Done since the v0.1.0 notes were written
- Repository is **public**.
- Zenodo DOI `10.5281/zenodo.20977890` minted on the `v0.1.0` release; badge in
  `README.md`, DOI in `CITATION.cff`.
- GitHub Pages live and built at https://kicrazom.github.io/DIVE-PL/.

### Still TODO before preprint
- Finish `src/agent/` (Stage 1) and `src/dashboard/` (Stage 4).
- Create OSF project + preregistration (H1–H3); cross-link to ClinicalTrials.gov.
- Insert ClinicalTrials.gov NCT number once assigned.
- Confirm final author list / co-authors.

## v0.1.0 — 2026-06-27 (scaffold)

- Initial repository structure (mirrors the open-science layout used in
  `navimed-umb`).
- Methodology specification (`METHODOLOGY.md`).
- Related-work mapping: component -> nearest precedent -> our difference.
- Architecture diagram (Mermaid).
- Open-science checklist (Zenodo / OSF / GitHub Pages).
- Engineering-thesis (PL) outline.
- Dual licensing (MIT + CC BY 4.0), citation metadata, AI usage disclosure.
- GitHub Pages landing page + auto-deploy workflow.

_(The original "TODO before preprint" list lived here; its current state is tracked
under **Unreleased** above and in `docs/open-science-checklist.md`.)_
