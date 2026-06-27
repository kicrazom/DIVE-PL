# AI usage disclosure

In the spirit of open science and EU AI Act transparency, this project discloses
where and how AI tools were used. AI is used as an **assistant under human
oversight**; a domain expert reviews and approves all outputs.

Study **design and orchestration are performed by the investigators (authors)** — humans. AI tools execute, assist, and review under their direction.

| Actor | Role in DIVE-PL | Human oversight |
|---|---|---|
| Investigators (authors) | Study design, orchestration, item content, decisions, interpretation | — (this is the human work) |
| Claude / Claude Cowork | Builds and operates the REDCap instrument via MCP / browser automation; drafts and scaffolds artifacts | Investigators direct and approve every action |
| GPT-5.5 (LLM-as-judge) | Independent review/validation of survey items (clarity, bias, content validity) | Investigators adjudicate all flags; final wording is human-approved |
| AI-assisted code generation | Analysis scripts and dashboards (Python/React) | Code reviewed, tested, and version-controlled |

## Principles

- AI **augments, does not replace** expert judgment; AI tools are **not co-authors**.
- Design/orchestration is human; drafting and review are kept **separate** (investigators draft with Cowork assistance; GPT-5.5 reviews) to reduce self-confirmation bias.
- No personal/participant data is processed by external AI services; instrument
  design uses non-identifiable content only.
- All prompts and rubrics are version-controlled for reproducibility.
