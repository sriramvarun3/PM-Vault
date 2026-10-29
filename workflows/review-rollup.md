---
workflow: review-rollup
cadence: monthly; quarterly; before performance reviews
side_effects: none
---

# Review rollup / self-review draft

Turn a period of journal entries, interactions, and decisions into an evidence-backed
rollup. This is where the vault pays for itself at review time.

## Inputs
- Period (default: last calendar month; quarterly when asked).
- `Journal/`, `Interactions/`, `Decisions/`, and `Projects/` within the period.
- `_reference/competencies.md` — your organization's framework and levels.
- The previous rollup in `Reviews/`.

## Steps
1. Collect entries in the period. Group by project and by competency tag.
2. For each competency, list the strongest evidence (impact first) and judge which level
   it supports. Say plainly where evidence is thin.
3. Pull out wins, shipped work, decisions and their outcomes, feedback received, and growth areas.
4. Compare with the previous rollup: what improved, what is still a gap.
5. Write the output and append `## [YYYY-MM-DD] review | <Kind>` to `_meta/log.md`.

## Output — `Reviews/YYYY-MM-DD <Monthly rollup | Quarterly self-review>.md`

```markdown
# <Kind> — <period>
## Headline (3 bullets)
## Impact
<!-- Outcome, your role, evidence link. -->
## Competency evidence
| Competency | Evidence | Level supported |
## Feedback received
## Gaps and next-period focus
```

## Guardrails
- Every claim links to its dated entry. No evidence, no claim.
- Write in the user's voice, first person, factual. No inflation.
