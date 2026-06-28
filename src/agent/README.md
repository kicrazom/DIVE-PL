# src/agent/ — Stage 1: design & orchestration (investigator-led)

Reference implementation of **Stage 1** of the DIVE-PL framework (see
[`../../METHODOLOGY.md`](../../METHODOLOGY.md) §2). The investigators (authors) **own**
this stage: research-question decomposition, item content, study protocol, registration
artifacts, and consent / RODO text. An LLM agent (reference: Claude / Cowork) **drafts
and scaffolds** these artifacts **under investigator direction** — it never decides.

> Design and orchestration are human work. The prompts here make the AI assistance
> explicit, reviewable, and reproducible — not autonomous.

## Why prompts, not a pipeline script

Stage 1 is interactive and judgement-heavy: an investigator works *with* the agent,
accepts/edits/rejects each draft, and loops items to the Stage 2 reviewer. Encoding
that as a one-shot automation would misrepresent the method. So the reference
implementation is a set of **versioned, diff-able prompts** plus an orchestration
note describing the human-led loop. This matches the repo convention (`src/README.md`):
*prompts versioned as plain text so reviews are diff-able*.

## Files

| File | Stage-1 sub-task |
|---|---|
| `prompt_01_decompose_research_question.md` | Turn a topic into a PECO-framed question, hypotheses (H1–H3), and a construct list. |
| `prompt_02_draft_items.md` | Draft candidate survey items for an approved construct (with response options, branching, REDCap field hints). |
| `prompt_03_scaffold_protocol_consent.md` | Scaffold protocol sections, consent text, and the RODO/GDPR information sheet. |
| `orchestration.md` | The human-led loop: how Stage 1 hands off to the Stage 2 reviewer and the Stage 3 REDCap build, and where the investigator gates. |

## Conventions

- The agent **drafts**; the investigators **decide**. Every output is reviewed.
- Keep design content separate from review (Stage 2 uses a *different* model).
- No participant data and no credentials ever enter a prompt (non-identifiable
  instrument content only).
- Record model name + version and the prompt commit hash with each drafting session
  so the contribution is reproducible (feeds the process metrics in thesis §5.1).
