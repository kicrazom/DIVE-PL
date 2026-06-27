# src/ — reference implementation (code map)

Placeholders for the four-component pipeline. Code is added incrementally; no
credentials or PII are ever committed (see `../.gitignore`).

```
src/
  agent/       # Stage 1: LLM-agent prompts & orchestration scripts
  reviewer/    # Stage 2: LLM-as-judge item-review prompts & rubric
  redcap/      # Stage 3: REDCap data dictionary, branching logic, API helpers
  dashboard/   # Stage 4: Python/React analytics dashboard (build output -> ../site)
```

## Conventions
- Python: PEP 8, type hints, small single-responsibility functions, `logging`
  over `print`, `try/except` on I/O.
- Secrets via `.env` (+ `python-dotenv`); never hardcoded.
- Local-first / offline-capable where possible (SQLite/DuckDB, local models).
- Prompts versioned as plain text so reviews are diff-able.
