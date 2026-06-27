# AI usage disclosure

In the spirit of open science and EU AI Act transparency, this project discloses
where and how AI tools were used. AI is used as an **assistant under human
oversight**; a domain expert reviews and approves all outputs.

| Tool | Role in DIVE-PL | Human oversight |
|---|---|---|
| Claude / Claude Cowork (LLM agent) | Study design, item drafting, protocol & registration artifacts, workflow orchestration, repository scaffolding | Expert reviews and edits every artifact before use |
| GPT (LLM-as-judge) | Independent review/validation of survey items (clarity, bias, content validity) | Expert adjudicates all flags; final wording is human-approved |
| AI-assisted code generation | Analysis scripts and dashboards (Python/React) | Code reviewed, tested, and version-controlled |

## Principles

- AI **augments, does not replace** expert judgment.
- Authoring and reviewing models are kept **separate** to reduce self-confirmation bias.
- No personal/participant data is processed by external AI services; instrument
  design uses non-identifiable content only.
- All prompts and rubrics are version-controlled for reproducibility.
