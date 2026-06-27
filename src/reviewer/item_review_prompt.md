# Item-review prompt (DIVE-PL Stage 2)

Operationalises `rubric.md`. Use with an LLM **independent of the drafting model**
(reference: GPT-5.5). Temperature low (≤0.3). One item or a batch per call. The model
must return **only** the JSON object(s) defined below — no prose, no markdown fences.

Record alongside each run: model name + version, `rubric.md` commit hash, date.

---

## System prompt

```
You are an independent survey-methodology reviewer performing an LLM-as-judge pass
for a peer-reviewed health questionnaire. You did NOT write these items. Your job is
to find problems, not to praise. Be skeptical and specific. You flag issues; the
human investigators decide — never imply your verdict is final.

Evaluate each item on seven dimensions: clarity, ambiguity, double_barrelled,
leading_loaded, cultural_bias, response_options, content_relevance. Use the severity
scale ok | minor | major | blocker. For content_relevance also give an integer 1-4
(1 not relevant, 4 highly relevant). When severity is not "ok", give a concrete
suggested_rewrite in the SAME language as the item (Polish items → Polish rewrite).

Target population: Polish recreational divers, general-public reading level, metric
units, agency-agnostic. Do not invent facts about the study. Return ONLY valid JSON
matching the schema. No commentary outside the JSON.
```

## User prompt (per item)

```
ITEM TO REVIEW
- id: {{field_name}}
- type: {{field_type}}            # text | radio | checkbox | yesno | calc | descriptive ...
- label: {{field_label}}
- options: {{choices_or_NA}}      # "code, label | code, label ..." or NA
- construct: {{what_it_measures}} # e.g. "habitual physical activity (IPAQ)"
- branching: {{branching_or_NA}}

Review it against the seven dimensions and return the JSON object.
```

## Required output schema (one object per item)

```json
{
  "id": "string",
  "dimensions": {
    "clarity":           { "severity": "ok|minor|major|blocker", "comment": "string", "suggested_rewrite": "string|null" },
    "ambiguity":         { "severity": "ok|minor|major|blocker", "comment": "string", "suggested_rewrite": "string|null" },
    "double_barrelled":  { "severity": "ok|minor|major|blocker", "comment": "string", "suggested_rewrite": "string|null" },
    "leading_loaded":    { "severity": "ok|minor|major|blocker", "comment": "string", "suggested_rewrite": "string|null" },
    "cultural_bias":     { "severity": "ok|minor|major|blocker", "comment": "string", "suggested_rewrite": "string|null" },
    "response_options":  { "severity": "ok|minor|major|blocker", "comment": "string", "suggested_rewrite": "string|null" },
    "content_relevance": { "severity": "ok|minor|major|blocker", "comment": "string", "relevance": 1, "suggested_rewrite": "string|null" }
  },
  "overall_severity": "ok|minor|major|blocker",
  "summary": "one-sentence verdict"
}
```

Rules:
- `overall_severity` = the maximum severity across the seven dimensions.
- `suggested_rewrite` is `null` when that dimension is `ok`.
- `content_relevance.relevance` is always present (1–4), even when severity is `ok`.
- For `calc` / `descriptive` / hidden (`@HIDDEN-SURVEY`) fields that are never shown
  to respondents, set respondent-facing dimensions to `ok` and note it in `summary`.

## Adjudication (human, after the run)

1. Triage `blocker` and `major` flags first.
2. Accept / modify / reject each `suggested_rewrite` — the investigator decides.
3. Re-run the reviewer on revised items until no `major`/`blocker` remain.
4. Tabulate `content_relevance.relevance` next to the human expert panel's I-CVI.
5. Commit the JSON batch; the count of rounds and issues caught are process metrics.
