---
name: vault-capture
description: Capture work knowledge, meeting recaps, source extracts, and durable answers into a PM Markdown vault that follows AGENTS.md. Use when the user says save, log, capture, or store something in the vault, including requests beginning with "log:", or when processing files in _inbox/.
---

# Capture information into the PM vault

The vault root is the folder containing `AGENTS.md`. All paths below are relative to it.
Read `AGENTS.md` before writing, `_meta/config.md` for timezone and allowed side effects,
and `index.md` before deciding which existing pages to update. Preserve the user's wording
when it carries meaning; never invent names, dates, metrics, quotes, sources, or confidence.

## Workflow

1. **Classify the input and establish grounding.**
   - A meaningful conversation or dictated recap belongs in `Interactions/`.
   - Work performed, a learning, blocker, feedback, win, or idea belongs in `Journal/`.
   - A consequential choice belongs in `Decisions/`, including options not taken and a revisit trigger.
   - A document, dashboard, chat thread, email, transcript, or article may also need an
     immutable extract in `Sources/docs/`, `Sources/transcripts/`, or `Sources/clips/`.
     Files from `_inbox/` move into the matching `Sources/` folder once processed.
   - For an internal document, save an extract plus its canonical URL, not a wholesale copy.
     For an unrecorded conversational recap, say the source is conversational and do not
     fabricate a raw source file.
   - If the subject cannot be placed confidently, ask one concise placement question
     instead of writing. In an unattended run, log it to `_meta/open-questions.md`.

2. **Read the applicable template in `_templates/` and create the dated episodic note.**
   - Use today's date from the system clock in the configured timezone.
   - Follow the naming conventions: `YYYY-MM-DD Person - topic.md` for interactions,
     `YYYY-MM-DD Title.md` for journal entries.
   - Include only claims supported by the input. Attribute stakeholder claims to the person
     who made them. Record contradictions rather than resolving them silently.
   - Route follow-ups to their single home: the project note for work, the person note for
     relationship follow-ups, the interaction note for conversation-specific items,
     `Tasks/Inbox.md` for uncategorised work, `Tasks/Personal.md` for non-work items.
     Never duplicate tasks; `Tasks/This week.md` is the only disposable pointer list.

3. **Propagate durable knowledge to the semantic layer.**
   - Update relevant `Topics/`, `People/`, `Projects/`, and lazily-created `Accounts/`
     pages. A substantive source normally touches several pages; do not stop after the
     dated note.
   - Ground every Topic claim with the dated note or a `Sources/` path. Mark synthesis
     `(inferred)` and name its reasoning chain. A Topic page must never be the sole source
     for another Topic page.
   - Create a new Topic only when a concept earns its third mention or is clearly durable.
     Create person/project/account pages only when the input contains real data about them.
   - Add unresolved questions to `_meta/open-questions.md` rather than filing speculation.

4. **Maintain operational navigation.**
   - Add every new page to `index.md` and revise summaries when needed.
   - Append one `## [YYYY-MM-DD] ingest | title` entry to `_meta/log.md` listing pages
     touched. The log is append-only.
   - Preserve frontmatter contracts and wiki-links. Do not restructure `Tasks/`.

5. **Validate and report.**
   - Run `python3 _bin/vault-lint.py` after a substantive ingest. Lint proposes fixes; do
     not bulk-rewrite findings.
   - Report the source/episodic note, semantic pages, task destinations, operational files,
     unresolved questions, and lint findings so the user can spot-check.

## Safety boundaries

- Write only inside the vault. Do not send messages, publish, share, commit, push, or
  edit shared documents unless `_meta/config.md` enables that action or the user
  explicitly asks in the current session.
- Treat `Sources/` as immutable after capture. Corrections and interpretation go in
  episodic or semantic notes.
- Never store credentials. Do not record colleagues without explicit agreement and
  applicable law and policy; the intended input is the user's own recap or notes.
- If the vault lacks an answer, say so. Do not turn an inference into a confident page.
