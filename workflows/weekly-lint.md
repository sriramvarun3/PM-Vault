---
workflow: weekly-lint
cadence: weekly
suggested_schedule: "0 16 * * 5"   # 4 pm Friday
side_effects: none
---

# Weekly lint

Keep the vault trustworthy. **Lint proposes; the human promotes.**

## Steps
1. Run `python3 _bin/vault-lint.py` (deterministic checks: broken links, orphans,
   unsourced topics, missing stamps, stale pages, cold contacts, old follow-ups,
   past-due dates, competency gaps).
2. Do the judgment checks the script can't:
   - Contradictions recorded but never revisited.
   - Claims superseded by newer sources.
   - Dated claims that have come due ("target: September").
   - Concepts mentioned 3+ times with no Topic page.
   - Decisions whose "Revisit when" trigger has fired.
   - Gaps a workplace or web search could close.
3. Write `_meta/lint-report.md`: the script output, then your judgment findings, each
   with a proposed fix and the page it applies to.
4. Refresh `Tasks/This week.md` as a pointer list to next week's most important open
   items (links to their home notes; never copies).
5. Append `## [YYYY-MM-DD] lint | Weekly` to `_meta/log.md`.

## Guardrails
- Do not apply fixes in bulk. Small mechanical fixes (a broken link, a missing `updated:`)
  are fine; anything that changes meaning waits for the user.
