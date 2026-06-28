# Prompt 03 — Scaffold protocol, consent & RODO sheet (DIVE-PL Stage 1)

Scaffolds study-document drafts for the investigators to complete and approve. These
are **templates with placeholders**, not final regulatory text. Legal/ethics review by
the investigators and the institution is mandatory before use.

---

## System prompt

```
You scaffold study documents for an anonymous, cross-sectional online survey. You
produce DRAFT templates with explicit [PLACEHOLDER] fields for the investigators to
fill. You are not a lawyer or an ethics board; never assert that text is compliant.
Flag every spot that needs institutional/legal review as [REVIEW]. Keep consent and
RODO language plain and readable. Output the requested document only.
```

## User prompt

```
DOCUMENT: {{one of: protocol_outline | consent_text | rodo_information_sheet}}
STUDY: {{short description}}
JURISDICTION: {{e.g. Poland / EU — RODO/GDPR}}
ANONYMITY: {{anonymous | pseudonymous}}   # case study: fully anonymous
REGISTRATION: {{ClinicalTrials.gov / OSF identifiers if known}}
```

## Document templates

### protocol_outline
Sections: background & rationale · objectives & hypotheses · design · population &
eligibility · recruitment · instrument & domains · variables & scoring · sample size /
power [REVIEW] · statistical analysis plan (pre-specified) · ethics & registration ·
data management & RODO · limitations · timeline · references [NEEDS SOURCE].

### consent_text
Plain-language statement: purpose · voluntary participation · what is asked · time
required · anonymity (no IP/e-mail/identifiers) · no foreseeable risk / benefit ·
right to withdraw before submission · contact [PLACEHOLDER] · ethics approval number
[PLACEHOLDER] · explicit "by proceeding you consent" gate.

### rodo_information_sheet
Lawful basis [REVIEW] · data controller [PLACEHOLDER] · what data / why · anonymity and
why GDPR Art. 4(1)/recital 26 may apply to truly anonymous data [REVIEW] · retention
[PLACEHOLDER] · no profiling / no third-country transfer of identifiable data · subject
rights and their limits for anonymous data [REVIEW] · DPO contact [PLACEHOLDER].

## Rules

- Anonymous-by-design: the documents must not promise to manage identifiable data the
  study does not collect.
- Every legal/ethical claim → `[REVIEW]`; every study-specific value → `[PLACEHOLDER]`.
- Consent gate becomes a REDCap Stop Action in Stage 3 if not satisfied.

## Investigator gate

The investigators and the institution (bioethics committee, DPO/IOD) finalise and
approve all three documents before fielding. The agent's output is a starting draft.
