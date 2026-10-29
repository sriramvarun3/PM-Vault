---
workflow: standup-prep
cadence: before a recurring program meeting
suggested_schedule: "30 8 * * 1-5"   # 8:30 am, Mon–Fri
side_effects: optional notify (see _meta/config.md)
---

# Stand-up / program-sync prep

A short brief for a recurring program meeting: where the program is against its goal,
what's blocking it, what changed since last time, and what to ask. Program name, goal
source, and attendees come from `_meta/config.md`.

## Inputs
- The goal source in config (the doc or page holding this period's goal and latest status).
- The vault: the program's `Projects/` page, related `Topics/` and `Accounts/` pages, and
  `Interactions/` from the last 7 days — especially the previous instance of this meeting.
- If your harness can reach them: chat threads, trackers, tickets, and docs that mention the
  program in the last 1–2 days.
- The previous brief: the latest `Reviews/*Standup prep - <program>.md`.

## Steps
1. Read the goal source and record the goal, the latest numbers, and **the date of that data**.
2. Gather blockers, decisions, and action items from the inputs.
3. Diff against the previous brief: mark each item **new**, **still open**, or **resolved**.
   Do not present a stale item as new.
4. Write the brief (below). Keep it under ~4,500 characters so it fits in a chat message.
5. Append `## [YYYY-MM-DD] brief | Standup prep — <program>` to `_meta/log.md`.
6. Notify only if `_meta/config.md` enables it for this workflow.

## Output — `Reviews/YYYY-MM-DD Standup prep - <program>.md`

```markdown
# <Program> stand-up prep — <Weekday, date>

## Where we are vs. goal
<!-- Goal, latest numbers with data date, time left in the period. -->
## Blockers
1. <blocker> — owner — (new | open since YYYY-MM-DD)
## Resolved since last brief
## Discussion questions
<!-- 3–5 questions aimed at hitting the goal. -->
## Proposed action items
<!-- Grouped by owner. Include open items from recent meeting notes. -->
## Sources
<!-- 2–4 links or vault pages. -->
```

## Guardrails
- Only facts from sources. Never invent numbers, ETAs, or owners.
- If data is missing or stale, say so in one line.
- Do not edit the program's `Projects/` page from this workflow; it is a read-only brief.
