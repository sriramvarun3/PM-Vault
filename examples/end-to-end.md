# Example: one recap, seven pages

A fictional walk-through of a single `log:` capture. All names, companies, and products
are made up.

## The input (typed or dictated in 60 seconds)

> log: 1:1 with Priya Shah (Data Platform lead). She says the usage-analytics export can't
> ship before March because the event pipeline migration slips to Feb. Acme Corp is
> blocked without CSV export — their admin asked twice. Priya thinks we should do a
> limited CSV export from the old pipeline; Marco (eng manager) wants to wait for the new
> one. Follow up with Priya in 2 weeks. I need to write the export one-pager by Friday.

## What the agent writes

**1. Episodic note** — `Interactions/2026-11-03 Priya Shah - export timeline.md`

```markdown
---
type: interaction
date: 2026-11-03
people: [[[Priya Shah]]]
project: "[[Usage analytics]]"
channel: 1:1
---
# 2026-11-03 — Export timeline

## Summary
Priya says the analytics export can't ship before March: the event pipeline migration
slips to February. Acme Corp is blocked on CSV export.

## Key points / decisions
- Priya: ship a limited CSV export from the old pipeline now.
- Marco (per Priya): wait for the new pipeline. Not yet discussed with Marco directly.

## Follow-ups
- [ ] Confirm Marco's position first-hand
```

**2. Semantic updates** — the step that compounds:

| Page | Change |
|---|---|
| `Topics/Analytics export.md` | New claim: "Export not before March (Priya, [[2026-11-03 Priya Shah - export timeline]])". New entry under **Contradictions**: Priya (ship limited CSV now) vs. Marco (wait), both attributed, left open. |
| `People/Priya Shah.md` | Owns the event pipeline migration; `cadence: as-needed`; follow-up "check in on migration date — 2026-11-17". |
| `Projects/Usage analytics.md` | Milestone risk: export slips to March. Next action: "Write export one-pager (due 2026-11-07)". |
| `Accounts/Acme Corp.md` | Created (first real data): blocked on CSV export; admin asked twice. |
| `Drafts/Requirements backlog.csv` | (Requirements sweep, later that evening) one row: "CSV export of usage data — Acme Corp blocked — source: [[2026-11-03 Priya Shah - export timeline]]". |

**3. Operational files** — `index.md` gains the new pages; `_meta/log.md` gets:

```markdown
## [2026-11-03] ingest | Priya Shah 1:1 — export timeline
- Interactions/2026-11-03 Priya Shah - export timeline.md (new)
- Topics/Analytics export.md, People/Priya Shah.md, Projects/Usage analytics.md
- Accounts/Acme Corp.md (new)
```

## Why it matters later

- **Two weeks later:** "What do we know about the export?" returns one page, with who
  said what and the open disagreement — not three meetings to re-read.
- **Next stand-up prep:** the slip and the Acme blocker show up as open items with owners.
- **Review time:** the one-pager you wrote that Friday is a journal entry tagged
  `Execution` and `Communication`, linked to the evidence.
