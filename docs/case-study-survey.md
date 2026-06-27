# Case study — the DIVE-PL diving survey

DIVE-PL is demonstrated on a real, registered study: a cross-sectional online
survey of recreational divers in Poland. This document describes the instrument
the framework produced. (Live version: `docs/survey.html` on GitHub Pages.)

## Aim

Assess health status, physical fitness, and safety/training knowledge in relation
to the occurrence of diving-related adverse events among recreational divers in Poland.

**Specific objectives:** estimate cardiorespiratory fitness (VO2max) from a
non-exercise questionnaire; assess knowledge of decompression sickness (DCS),
barotrauma and safe-diving rules; determine the frequency of DCS/barotrauma
symptoms; identify risky behaviours; and test associations between training level,
fitness, health and adverse events.

## Design

Cross-sectional, observational, non-interventional, anonymous online questionnaire
(~12–18 min). No clinical procedures or biological sampling; minimal risk.

## Population

Adults (≥18 years) resident in Poland who completed at least one dive in the past
24 months.

## Instrument sections

| Section | Content |
|---|---|
| Demographics | age, sex, height/weight (BMI), residence |
| Diving exposure & training | certification level (OWD / AOWD / higher), number of dives, years of experience, organisation |
| Health status | chronic conditions, medications, contraindications |
| Physical fitness | physical-activity rating (PA-R) for VO2max estimation |
| Safety knowledge | DCS, barotrauma and safe-diving rules — three difficulty levels |
| Risky behaviours | smoking, alcohol before diving, diving beyond certification |
| Adverse events | self-reported DCS / barotrauma symptoms and diving incidents |

## Fitness estimation

VO2max is estimated with the **University of Houston Non-Exercise Test** from PA-R,
age, BMI and sex — a low-cost, scalable proxy applied here in a diving population.

## Hypotheses

- **H1.** Higher certification (AOWD and above) is associated with better knowledge of diving-related health hazards.
- **H2.** Lower estimated VO2max is associated with a higher frequency of adverse events in the diving history.
- **H3.** Risky behaviours (smoking, pre-dive alcohol) are more frequent among divers with lower certification.

## Endpoint & analysis

Primary endpoint: the proportion of divers reporting at least one diving-related
adverse event. Associations with certification level, estimated VO2max, BMI and
other factors are analysed using multivariable logistic regression.

## Ethics & registration

Approved by the Bioethics Committee, Medical University of Białystok (protocol
**APK.002.228.2026**). Registered on ClinicalTrials.gov (NCT pending — see
`CLINICAL_TRIALS.md`). GDPR/RODO-compliant and fully anonymous; no participant
data are published in this repository.

## Validity caveat

VO2max is **estimated**, not measured. Prior fitness–adverse-event evidence used
directly measured VO2max; testing whether the proxy reproduces that relationship
is part of the study.
