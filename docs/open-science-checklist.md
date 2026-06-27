# Open-science checklist (DIVE-PL)

Goal: anyone can independently reproduce the methodology and verify the case-study results.

_Last reconciled with live state: 2026-06-28._

## 1. GitHub (this repo)
- [x] Repository created
- [x] Methodology, related work, architecture, licensing, citation
- [x] Repository is **public**
- [~] Add reference implementation under `src/` — `src/redcap/` (Stage 3) and
  `src/reviewer/` (Stage 2) populated; `src/agent/` (Stage 1) and `src/dashboard/`
  (Stage 4) still scaffold

## 2. Zenodo (archival DOI)
- [x] Repo enabled in Zenodo's GitHub integration
- [x] GitHub **release** `v0.1.0` created → Zenodo minted a DOI
- [x] DOI `10.5281/zenodo.20977890` resolves; badge in `README.md`
- [x] DOI present in `CITATION.cff` (`.zenodo.json` left to Zenodo's GitHub integration)

## 3. OSF (project + preregistration)
- [ ] Create OSF project "DIVE-PL"
- [ ] Link the GitHub repo as an OSF component
- [ ] Preregister the case-study analysis plan (H1–H3, variables, tests)
- [ ] Cross-link OSF <-> ClinicalTrials.gov (see `CLINICAL_TRIALS.md`)

## 4. GitHub Pages (live dashboard)
- [x] Pages source prepared in `docs/` (`docs/index.html` + `docs/.nojekyll`)
- [x] Pages enabled: Source = branch `main` / `/docs`
- [x] Site live and **built** at https://kicrazom.github.io/DIVE-PL/
- [ ] Verify the dashboard loads only **aggregated / de-identified** data (RODO)
- [ ] Link the Pages URL from `README.md`

## 5. Privacy gate (RODO/GDPR) — must pass before going public
- [x] No PII or raw participant data anywhere in git history (instrument metadata only)
- [x] `.gitignore` excludes data files (`*.csv`; instrument dictionary whitelisted under `src/redcap/`)
- [ ] Dashboard shows aggregates only
- [ ] Consent + RODO information sheet archived (text, not respondent data)
