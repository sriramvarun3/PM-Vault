# PM-Vault

An LLM-Wiki style Knowledge Vault for Product Managers to operate in an AI-native manner.

A plain-Markdown knowledge system for Product Managers, run by an AI agent. You talk;
the agent files. Over weeks it compounds into **decision-grade recall** ("what do we know
about X, and who said it?") and **legible impact** (reviews assembled from evidence, not memory).

It works with any agent that can read and write files — Claude Code, Codex, Glean Tau,
Cursor, Gemini CLI, OpenCode — and degrades gracefully to copy-paste in a chat app.
This repository is a **template**: the rules, workflows, and templates, with no content.

## What a day looks like

| When | You | The agent |
|---|---|---|
| After a conversation | `log: met Alex, she owns eval infra, follow up in 2 weeks` | Writes the dated note and updates Alex's page, the project, and the topics involved |
| Before a program sync | Read the brief | `standup-prep`: status vs. goal, blockers new since last time, questions, actions by owner |
| End of day | Nothing | `daily-capture`: files every meeting, routes action items, writes a one-page day summary; `requirements-sweep` adds new asks to the backlog |
| Weekly | Skim the lint report, decide what to fix | `weekly-lint` and `competitive-tracker` |
| Review season | Edit the draft | `review-rollup`: evidence-linked self-review against your competency framework |

See [`examples/end-to-end.md`](examples/end-to-end.md) for one recap turning into seven updated pages.

## Quick start (5 minutes)

1. **Create your own private copy** of this template. Your vault will hold notes about
   people and internal work — never make it public.
2. **Fill in [`_meta/config.md`](_meta/config.md)**: timezone, which sources your agent can reach,
   and which side effects (if any) you allow. By default the agent only writes inside the vault.
3. **Swap in your framework** at [`_reference/competencies.md`](_reference/competencies.md).
4. **Open the folder in your agent** and say `log: <something from today>`.

Per-harness setup and scheduling: [`docs/setup.md`](docs/setup.md). Connecting meeting notes,
chat, and docs: [`docs/connectors.md`](docs/connectors.md). No connectors? Drop exports in
`_inbox/` or paste text — everything still works.

## How it's built

**`AGENTS.md` is the agent's contract** — layers, frontmatter, grounding rules, portability
rules, and operations. `CLAUDE.md` just imports it. This README is the human's guide; if they
disagree, `AGENTS.md` wins on mechanics.

### Four layers

The vault follows the LLM-wiki pattern: knowledge is *compiled once and kept current*, not
re-derived from raw notes on every question.

1. **Raw** (`Sources/`) — immutable transcripts, doc extracts, clipped articles.
2. **Episodic** (`Interactions/`, `Journal/`, `Decisions/`) — dated records of what happened.
3. **Semantic** (`Topics/`, `People/`, `Projects/`, `Accounts/`) — living pages the agent revises. **This layer compounds.**
4. **Operational** (`index.md`, `_meta/`, `_reference/`, `_templates/`, `_bin/`, `workflows/`) — navigation, config, and bookkeeping.

The key move: a fact learned in a conversation gets filed *twice* — once in the dated note
(history) and once on the relevant `Topics/` page (current understanding, revised forever).

### Rules that keep it trustworthy

- Every claim on a Topic page links to the note or source that grounds it, or is marked `(inferred)`.
- Stakeholder claims are attributed: "Alex wants September", not "the target is September".
- Contradictions are recorded and left open for you — never silently resolved.
- No answer is a valid answer. The agent says what's missing instead of guessing.
- Lint proposes; you decide.

### Folders

| Folder | What goes here |
|---|---|
| `_inbox/` | Drop zone for exports and notes waiting to be ingested |
| `Topics/` | Living knowledge pages, one concept each, every claim sourced |
| `People/` | Role, what they own, what to leverage them for, relationship state |
| `Projects/` | Workstreams: goal, role, milestones, next actions |
| `Accounts/` | Customers and prospects (created when there's real data) |
| `Interactions/` | One note per meaningful conversation |
| `Journal/` | Work and learnings, competency-tagged — feeds reviews |
| `Decisions/` | One note per consequential decision, including options not taken |
| `Sources/` | Immutable raw material: `transcripts/`, `docs/`, `clips/` |
| `Drafts/` | Artifacts in flight: briefs, PRDs, the requirements backlog |
| `Reviews/` | Daily captures, stand-up briefs, rollups, self-review drafts |
| `Tasks/` | Standalone to-do lists |
| `workflows/` | Repeatable jobs the agent runs on demand or on a schedule |
| `skills/` | The capture procedure, in the portable Agent Skills format |
| `_meta/` | `config.md`, `log.md`, `open-questions.md`, `lint-report.md` |
| `_templates/` | Note templates |
| `_reference/` | Your competency framework, org map, reference material |
| `_bin/` | `vault-lint.py` — deterministic health checks, Python standard library only |

## Where a task lives (one item, one home)

| Scope | Home | Example |
|---|---|---|
| The work itself | `Projects/<Name>.md` → `## Next actions` | "Draft the architecture brief" |
| Dated program commitments | `Projects/<Name>.md` → `## Milestones` | "v1 shipped — 2026-09-30" |
| A person / relationship | `People/<Name>.md` → `## Follow-ups` | "Ask for customer intros" |
| One conversation only | `Interactions/<note>.md` → `## Follow-ups` | "Confirm the name I misheard" |
| Not yet categorised | `Tasks/Inbox.md` | anything captured fast |
| Non-work | `Tasks/Personal.md` | errands |
| This week's shortlist | `Tasks/This week.md` | a **disposable** pointer list, rewritten weekly |

Never duplicate a task. A new workstream is a new `Projects/` note, not a new task file.

## Workflows

| Playbook | Runs | Output |
|---|---|---|
| [`capture`](workflows/capture.md) | on demand | dated note + updated pages |
| [`daily-capture`](workflows/daily-capture.md) | end of day | `Reviews/<date> Daily capture.md` |
| [`standup-prep`](workflows/standup-prep.md) | before a program sync | `Reviews/<date> Standup prep - <program>.md` |
| [`requirements-sweep`](workflows/requirements-sweep.md) | end of day | `Drafts/Requirements backlog.csv` |
| [`competitive-tracker`](workflows/competitive-tracker.md) | weekly | updated competitive Topic page + weekly note |
| [`weekly-lint`](workflows/weekly-lint.md) | weekly | `_meta/lint-report.md` |
| [`review-rollup`](workflows/review-rollup.md) | monthly / quarterly | rollup or self-review draft |

Write your own by copying one: keep **Inputs, Steps, Output, Guardrails**, and keep personal
values in `_meta/config.md` so the playbook stays shareable.

## What to ask

- "What do we know about proving ROI, and who said it?"
- "Who should I talk to about search ranking?"
- "Who haven't I connected with in a month that I should?"
- "Where am I light on competencies this quarter?"
- "Draft my quarterly self-review from the journal."
- "Lint the vault."

When an answer is durable, say so — it gets filed into `Topics/` or `Drafts/` instead of
disappearing into chat history.

## Cadences

- **Daily (~2 min):** log the 1–3 things worth remembering. Let `daily-capture` do the rest.
- **Weekly (~10 min):** read the lint report; promote or reject its proposals.
- **Monthly (~20 min):** ask for a rollup.
- **Quarterly (~45 min):** ask for a self-review draft against your framework.

**First 90 days in a role:** capture *who does what* and *fresh-eyes observations* — things
that seem odd or improvable fade fast and are uniquely valuable as a newcomer.

## Privacy and safety

- **Keep your vault private.** Share this template, not your notes.
- The agent writes only inside the vault unless you enable a specific side effect in
  `_meta/config.md` (for example, a message to yourself when the daily capture finishes).
- Store extracts plus links for internal docs, not full copies. Never store credentials.
- Follow consent laws and your organization's policy on recording. The vault never records;
  the best input is your own recap, dictated right after a conversation.

## Optional

- **Obsidian** (free) renders the `[[wiki-links]]` as a live graph. The files work fine without it.
- **Local git** in your private vault makes every agent edit recoverable. Never push it to a public remote.

## Deliberately not included

No vector database, embeddings, schema validators, or second agent-only vault. At a few
hundred pages, `index.md` plus grep plus a clear contract is enough.
