---
workflow: competitive-tracker
cadence: weekly
suggested_schedule: "0 9 * * 1"   # 9 am Monday
side_effects: none
---

# Competitive tracker

Keep a living competitive read for one market current, with evidence. Market, competitors,
and sources come from `_meta/config.md`.

## Inputs
- `Topics/Competitive read - <market>.md` (create from `_templates/topic.md` on first run),
  including its `updated:` date — that is the "since" date for this run.
- Public changelogs, release notes, docs, and pricing pages for each competitor.
  Needs web access; if your harness has none, say so and stop.
- Vault mentions since the last run: `Interactions/` and `Accounts/` notes where
  customers or colleagues mentioned a competitor.

## Steps
1. For each competitor, list releases or changes since the last review, with links.
2. For each change, decide: does it matter to our product? Note the implication, or
   "no impact".
3. Add customer or colleague observations from the vault, attributed and linked.
4. Update the Topic page: revise `## Current understanding`, add new disagreements under
   `## Contradictions / open disagreements`, stamp `updated:` and `sources:`.
5. Save public pages you relied on as extracts in `Sources/clips/` when they're load-bearing.
6. Write the weekly note (below) and append `## [YYYY-MM-DD] review | Competitive tracker — <market>`
   to `_meta/log.md`.

## Output — `Reviews/YYYY-MM-DD Competitive tracker - <market>.md`

```markdown
# Competitive tracker — <market> — week of <date>
## Most important change
## Changes by competitor
| Competitor | Change | Date | Implication for us | Evidence |
## What customers said
## Open questions
```

## Guardrails
- Mark anything you cannot verify as "unverified". Never infer a feature from marketing copy alone.
- Public sources only, unless the user explicitly provides internal material.
