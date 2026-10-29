# Vault schema — the agent's operating contract

This file governs how an agent maintains this vault. It is deliberately harness-neutral:
Claude Code, Codex, Glean Tau, Cursor, Gemini CLI, OpenCode, or a plain chat window can
all follow it. `README.md` is for the human; this file is for you. If the two disagree,
fix `README.md` and tell the user.

**Purpose of the vault:** help a Product Manager do excellent work and make that work
visible. Two outcomes it must serve, in this order:
1. **Decision-grade recall** — answer "what do we know about X, and who said it?" without re-deriving it.
2. **Legible impact** — make performance reviews, self-reviews and comp conversations
   a matter of assembly rather than recollection.

**Start of every session:** read this file, then `index.md`, then `_meta/config.md`
(the user's timezone, sources, and which side effects are allowed). Workflows live in
`workflows/`; when the user names one ("run the daily capture"), read and follow it.

---

## 0. Portability rules

1. **All paths are relative to the vault root** (the folder containing this file).
   Never hard-code an absolute path into a note.
2. **Use the system clock for dates**, in the timezone set in `_meta/config.md`.
   Never guess today's date.
3. **Capabilities vary by harness. Degrade, don't fabricate.** If you cannot reach a
   source (calendar, meeting notes, chat, docs, email), say which one, then use what is
   available: files in `_inbox/`, text the user pasted, or a question to the user.
   Never invent the content of a meeting you could not read.
4. **Local writes only by default.** Write inside this vault. Sending messages, posting
   to chat, editing shared docs or sheets, creating tickets, committing, or pushing are
   *side effects*: do them only when `_meta/config.md` enables that specific side effect
   for that workflow, or the user explicitly asks in the current session.
5. **Unattended runs are conservative.** In a scheduled run there is no one to answer a
   question, so record unresolved placement questions in `_meta/open-questions.md`
   instead of guessing, and finish with a report of what you did and skipped.

---

## 1. Layers

Four layers with different mutability. Never blur them.

| Layer | Folders | Mutability | Owner |
|---|---|---|---|
| **Raw** | `Sources/` | **Immutable.** Read, never edit. | The world |
| **Episodic** | `Interactions/`, `Journal/`, `Decisions/` | Append-only in spirit. Correct errors; don't rewrite history. | Human + agent |
| **Semantic** | `Topics/`, `People/`, `Projects/`, `Accounts/` | Continuously revised. This is the compounding layer. | Agent |
| **Operational** | `index.md`, `_meta/`, `_reference/`, `_templates/`, `_bin/`, `workflows/` | Maintained every ingest. | Agent |

Outputs (`Drafts/`, `Reviews/`, `Tasks/`) are products of the vault, not part of its
knowledge graph. `_inbox/` is a drop zone for raw files waiting to be ingested.

### Folder contract

| Folder | Contains | Naming |
|---|---|---|
| `_inbox/` | Unprocessed exports: transcripts, notes, pasted threads. Emptied by ingest. | anything |
| `Sources/transcripts/` | Raw meeting transcripts | `YYYY-MM-DD Person - topic (raw transcript).txt` |
| `Sources/docs/` | Extracts of internal docs/PRDs/dashboards/meeting notes, with canonical URL in frontmatter | `Author - Doc title.md` |
| `Sources/clips/` | External articles, blog posts, competitor material | `Publisher - Title.md` |
| `Interactions/` | One note per meaningful conversation | `YYYY-MM-DD Person - topic.md` |
| `Journal/` | Work + learnings entries, competency-tagged. Feeds reviews. | `YYYY-MM-DD Title.md` |
| `Decisions/` | One note per consequential decision, incl. the options not taken | `Subject - the choice.md` |
| `Topics/` | **Living knowledge pages.** One concept, system, market question or domain per page. Flat — no subfolders. | `Topic name.md` |
| `People/` | One note per person: scope, leverage, relationship state | `Full Name.md` |
| `Projects/` | Workstream hubs: goal, role, milestones, next actions | `Project.md` |
| `Accounts/` | Customers/prospects (create lazily, when there is real data) | `Account name.md` |
| `Drafts/` | PM artifacts in flight — briefs, strategy docs, PRDs, requirement backlogs | free |
| `Reviews/` | Generated briefs, daily captures, rollups, self-review drafts | `YYYY-MM-DD Kind.md` |
| `Tasks/` | Standalone to-do lists. **Do not restructure.** | see `README.md` |

"Log" in this file always means `_meta/log.md`, the operations ledger.

---

## 2. Frontmatter contract

Every markdown page outside `Tasks/`, `_inbox/` and `Sources/transcripts/` carries at minimum:

```yaml
---
type:      # topic | person | project | account | interaction | journal | decision | source | review | reference
status:    # current | review-due | superseded      (semantic + reference pages)
updated:   # YYYY-MM-DD — stamped on every substantive edit
sources: [] # what grounds this page: [[dated notes]] and/or Sources/ paths
tags: []
---
```

Type-specific fields stay as defined in `_templates/`. Dated episodic notes use `date:`
instead of `updated:` and need no `status:`.

`sources:` is **stamped at write time, never inferred at read time.** If you cannot name
what grounds a page, you do not have a page — you have a question for `_meta/open-questions.md`.

---

## 3. Grounding rules (non-negotiable)

1. **Every claim on a `Topics/` page is traceable.** Either it links to the dated
   episodic note or `Sources/` file that asserts it, or it is marked `(inferred)` with
   the reasoning chain named. No exceptions, no silent synthesis.
2. **A Topic page is never the sole grounding for another Topic page.** Grounding
   flows Raw → Episodic → Semantic, never sideways. This stops one fabrication from
   becoming the vault's consensus.
3. **Contradictions are recorded, not resolved.** When two sources disagree, write both
   claims with attribution under `## Contradictions / open disagreements` and leave it
   open. PM work runs on unresolved stakeholder disagreement — that disagreement is
   often the most decision-useful thing on the page. Never pick a winner on the user's
   behalf; surface it at lint time.
4. **Attribute stakeholder claims to the person.** "Alex wants September" not
   "the target is September." Who believes what is load-bearing information.
5. **No confident answer is a valid answer.** If the vault does not contain it, say so
   and propose where to look. Never file a speculative answer back as a page.
6. **When the subject can't be placed, ask one question instead of writing.** In an
   unattended run, log the question to `_meta/open-questions.md` instead.

---

## 4. Operations

### Ingest
Trigger: a transcript, a dictated recap, an internal doc, a chat thread, an article,
files in `_inbox/`, or "log: …" in chat. The detailed procedure is
`skills/vault-capture/SKILL.md`; the summary:

1. Put the raw artifact in `Sources/` (or note that the source is conversational and
   unrecorded). Internal docs: store an **extract plus the canonical URL**, not a
   wholesale copy. Move processed `_inbox/` files into `Sources/`.
2. Write the episodic note — `Interactions/` for a conversation, `Journal/` for work done
   or a learning, `Decisions/` for a choice made.
3. **Propagate to the semantic layer.** This is the step that creates the compounding
   value, and the step that is easiest to skip. A single substantive source normally
   touches 5–15 pages: relevant `Topics/`, the `People/` notes of everyone involved,
   the `Projects/` hub, any `Decisions/` record it revises, `Accounts/` if a customer
   is named. Create a new Topic page when a concept earns its third mention.
4. Route follow-ups by scope, per the table in `README.md`. Never duplicate a task.
5. Update `index.md` and append to `_meta/log.md`.
6. Add anything unresolved to `_meta/open-questions.md`.

Report back with what you touched, so the human can spot-check.

### Query
1. Read `index.md` first. Drill into the pages it names; don't grep blindly.
2. Answer with citations to vault pages, and name the grounding date when recency matters.
3. **File durable answers back.** A comparison, a competitive read, a framework the user
   asked for — that belongs in `Topics/` or `Drafts/`, not lost in chat history.
   Explorations should compound exactly like ingested sources.

### Lint
Run after a substantive ingest, weekly, or on request. Run `python3 _bin/vault-lint.py`
for the deterministic checks (Python 3 standard library only); you do the judgment.
**Lint proposes; the human promotes.** Never bulk-rewrite on a lint pass.

Check for:
- Contradictions recorded but never revisited
- `status: review-due` pages, and pages whose `updated:` is stale relative to newer sources
- Dated claims that have come due ("target: September") and were never resolved
- Orphan pages with no inbound links
- Concepts mentioned 3+ times with no Topic page of their own
- People past their `cadence:` window with no recent interaction
- Follow-ups older than 30 days
- Unsourced claims on Topic pages
- Gaps a workplace search or web search could close

Write the result to `_meta/lint-report.md` and append to `_meta/log.md`.

### Review rollup
Weekly / monthly / quarterly. Built from `Journal/` (competency tags), `Interactions/`,
`Decisions/`. Tag against the framework in `_reference/competencies.md` and note which
progression level the evidence supports. Every claim cites its dated entry.

### Workflows
Repeatable jobs — daily capture, stand-up prep, requirements sweep, competitive tracking,
weekly lint, review rollups — are playbooks in `workflows/`. Each one names its inputs,
steps, outputs, and allowed side effects. They run the same way on demand or on a schedule.

---

## 5. `_meta/log.md` format

Append-only. One line per operation, consistent prefix so it stays greppable:

```
## [YYYY-MM-DD] ingest | Alex Chen 1:1 — platform architecture
```

Ops: `ingest`, `query`, `lint`, `refactor`, `review`, `brief`, `sweep`. Under each entry,
a terse list of pages touched. `grep "^## \[" _meta/log.md | tail -10` gives recent history.

---

## 6. Style

- Terse and declarative. No filler, no restating the obvious back to the user.
- Preserve the user's own phrasing when it is sharper than yours, and quote stakeholders
  verbatim when the wording carries the meaning.
- Every Topic page opens with a 2-sentence summary that stands alone.
- Link generously with `[[wiki-links]]`; links resolve by filename, so files can move
  between folders freely.
- Prefer one dense page over three thin ones. Prefer a linked sibling page
  (`Project - architecture brief.md`) over a subfolder.
- Never invent a name, date, metric, or quote. Garbled transcript names get flagged
  inline, not guessed.

## 7. Privacy

- This vault holds notes about colleagues, customers, and internal work. Keep it private.
  Never copy vault content into a public repository, a public chat, or a prompt to a
  tool the user has not approved for that data.
- Mark internal extracts `confidential: true`. Never store passwords, tokens, or other
  credentials in any note, config, or workflow.
- Do not record colleagues without explicit agreement and applicable law and policy.

## 8. What this vault deliberately does not do

Do not add typed schema validators, confidence-decay engines, vector/embedding search, or
a second agent-only vault. At this scale (a few hundred pages, one user) `index.md` plus
grep plus this contract is sufficient, and ceremony would cost more than it returns.
Revisit vector search past ~300 pages.
