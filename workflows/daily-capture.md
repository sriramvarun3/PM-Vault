---
workflow: daily-capture
cadence: end of each work day
suggested_schedule: "0 18 * * 1-5"   # 6 pm, Mon–Fri, in your timezone
side_effects: optional notify (see _meta/config.md)
---

# Daily capture

Record every meaningful meeting from today into the vault, update tasks, and produce a
one-page summary of the day. This is the workflow that makes the vault compound without
daily effort.

## Inputs
- Today's date (system clock, configured timezone).
- **Meetings source** from `_meta/config.md`: calendar plus notes or transcripts, through
  whatever connector your harness has.
- Fallback: any files in `_inbox/` (exported transcripts, meeting notes, your own recaps).
- The previous run: the latest `Reviews/*Daily capture.md` and recent `_meta/log.md` entries,
  so nothing is ingested twice.

## Steps
1. **List today's meetings.** Note which have notes/transcripts and which do not. Skip
   meetings already captured (check `_meta/log.md` and existing `Interactions/` files for
   today), declined meetings, and meetings below the length threshold in config.
2. **For each meeting with content**, run the capture procedure in
   `skills/vault-capture/SKILL.md`:
   - Save an extract (with canonical link) to `Sources/docs/`, or the transcript to
     `Sources/transcripts/`.
   - Write `Interactions/YYYY-MM-DD Person - topic.md`.
   - Propagate to `People/`, `Projects/`, `Topics/`, `Accounts/`, `Decisions/`.
   - Route action items to their single home (project, person, or `Tasks/Inbox.md`).
     Mark items assigned to the vault owner clearly; record others' items with the owner's name.
3. **Meetings with no notes:** list them in the summary as "not captured — no notes".
   Do not reconstruct them from the calendar invite.
4. **Process `_inbox/`** the same way, then move the files into `Sources/`.
5. **Update operational files:** `index.md`, one `## [YYYY-MM-DD] ingest | Daily capture`
   entry in `_meta/log.md`, and open questions.
6. **Run `python3 _bin/vault-lint.py`** and note anything new it found.
7. **Write the day summary** (below).
8. **Notify** only if `_meta/config.md` enables it: send a two-line message ("Vault updated
   for <date> — N meetings captured") with the summary's top points.

## Output — `Reviews/YYYY-MM-DD Daily capture.md`

```markdown
---
type: review
date: YYYY-MM-DD
sources: [[[YYYY-MM-DD Person - topic]], ...]
---
# Daily capture — <Weekday, date>

## Meetings captured (N)
- [[YYYY-MM-DD Person - topic]] — one line: the most important point or decision.

## Key decisions and changes
## New action items (mine)
## Waiting on others
## Not captured
<!-- Meetings with no notes, sources the harness could not reach. -->
## Open questions added
```

## Guardrails
- One page. If it runs long, cut detail, not meetings.
- Only facts from the meeting content. Attribute claims to people.
- Never record or transcribe a meeting yourself; only use notes the user is allowed to have.
