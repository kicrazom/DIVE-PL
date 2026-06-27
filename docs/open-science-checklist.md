# Open-science checklist (DIVE-PL)

Goal: anyone can independently reproduce the methodology and verify the case-study results.

## 1. GitHub (this repo)
- [x] Repository created (private during drafting)
- [x] Methodology, related work, architecture, licensing, citation
- [ ] Add reference implementation under `src/`
- [ ] Flip to **public** at preprint/submission time

## 2. Zenodo (archival DOI)
- [ ] Log in to https://zenodo.org with the GitHub account
- [ ] Enable the **DIVE-PL** repo in Zenodo's GitHub integration
- [ ] Create a GitHub **release** (`v0.1.0`) -> Zenodo mints a DOI
- [ ] Add DOI badge to `README.md` and DOI to `CITATION.cff` / `.zenodo.json`

## 3. OSF (project + preregistration)
- [ ] Create OSF project "DIVE-PL"
- [ ] Link the GitHub repo as an OSF component
- [ ] Preregister the case-study analysis plan (H1–H3, variables, tests)
- [ ] Cross-link OSF <-> ClinicalTrials.gov (see `CLINICAL_TRIALS.md`)

## 4. GitHub Pages (live dashboard)
- [x] Pages source prepared in `site/` + auto-deploy workflow `.github/workflows/pages.yml`
- [ ] Settings -> Pages -> Source = **GitHub Actions** (one-time)
- [ ] Verify the dashboard loads only **aggregated / de-identified** data (RODO)
- [ ] Link the Pages URL from `README.md`

## 5. Privacy gate (RODO/GDPR) — must pass before going public
- [ ] No PII or raw participant data anywhere in git history
- [x] `.gitignore` excludes data files
- [ ] Dashboard shows aggregates only
- [ ] Consent + RODO information sheet archived (text, not respondent data)
