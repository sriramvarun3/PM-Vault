---
workflow: capture
cadence: on demand
side_effects: none
---

# Capture — "log: …"

The everyday entry point. Use it right after a conversation, when you learn something,
make a decision, or finish a piece of work.

## Inputs
- Whatever the user gives you: a dictated recap, pasted notes, a link, a chat thread,
  or a file in `_inbox/`.

## Steps
Follow `skills/vault-capture/SKILL.md` exactly. In short:
1. Classify: conversation → `Interactions/`; work or learning → `Journal/`;
   choice → `Decisions/`; document or transcript → `Sources/` extract as well.
2. Write the dated note from the matching template.
3. Propagate facts into `Topics/`, `People/`, `Projects/`, `Accounts/`.
4. Route follow-ups to one home each.
5. Update `index.md` and `_meta/log.md`; run `python3 _bin/vault-lint.py` if substantive.

## Output
A short report: the note created, the pages updated, where each follow-up went, and any
open questions.

## Guardrails
- One clarifying question beats a misfiled note.
- Never invent names, dates, numbers, or quotes. Flag garbled names inline.

## Example prompts
- `log: met Alex Chen (eval infra lead). Open to sharing the eval harness. Follow up in 2 weeks.`
- `log: decided to ship v1 without SSO; revisit if 3+ enterprise prospects block on it.`
- `capture the files in _inbox/`
