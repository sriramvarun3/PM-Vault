---
workflow: requirements-sweep
cadence: end of each day, after daily-capture
suggested_schedule: "30 18 * * 1-5"   # 6:30 pm, Mon–Fri
side_effects: optional — write to a shared sheet only if _meta/config.md names one
---

# Requirements sweep

Find genuinely new product requirements surfaced today and add them to a backlog for
review. **Quality over quantity: adding zero rows is a good outcome.**

## Inputs
- Product area and keywords from `_meta/config.md`.
- Vault files created or modified today, especially `Interactions/`, `Accounts/`,
  `Journal/`, `Decisions/`, `Sources/`, and the area's `Topics/` pages.
  A portable way to find them: `find . -name "*.md" -newermt "<today> 00:00"`.
- If reachable: today's chat threads, emails, and tickets that match the keywords.
- The existing backlog (for de-duplication).

## What counts as a requirement
A specific capability, fix, or constraint someone needs, with a reason. Examples: a
customer blocker, a repeated feature ask, a compliance need, a missing integration, a
pricing or packaging constraint. **Not** a requirement: general enthusiasm, a status
update, an item already in the backlog, or your own speculation.

## Steps
1. Collect candidate asks from today's inputs, each with who asked and where.
2. De-duplicate against the backlog. If an existing row is the same ask, do not add a row;
   instead note the new evidence (who, date, link) in the existing row's `evidence` column.
3. Keep only candidates that pass the definition above.
4. Append new rows to the target in `_meta/config.md` (default `Drafts/Requirements backlog.csv`),
   with `status = proposed`. Never edit or delete existing rows except to add evidence.
5. Append `## [YYYY-MM-DD] sweep | Requirements — N added, M reinforced` to `_meta/log.md`.

## Output — backlog columns

```csv
date_added,requirement,reason,requested_by,source,evidence,suggested_priority,status,notes
```

- `requested_by`: person and/or account, as stated.
- `source`: vault page (`[[YYYY-MM-DD Person - topic]]`) or canonical link.
- `suggested_priority`: P0–P3 with a one-clause reason, or blank if unclear.

Finish with a short report: rows added, rows reinforced, candidates rejected and why.

## Guardrails
- Do not edit vault notes in this workflow; it only reads them and writes the backlog.
- If a shared sheet is configured and the write fails, write nothing to it; put the
  candidate rows in the report instead.
