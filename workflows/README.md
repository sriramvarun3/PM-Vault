# Workflows

Plain-Markdown playbooks any agent can run. Each one lists its inputs, steps, outputs,
and the side effects it is allowed to take. They work the same way whether you type
"run the daily capture" in a chat or schedule them (see `docs/setup.md`).

| Workflow | When | What it does | Writes |
|---|---|---|---|
| [`capture.md`](capture.md) | Anytime — "log: …" | Files one recap, doc, or thread into the vault | Episodic + semantic pages |
| [`daily-capture.md`](daily-capture.md) | End of each work day | Ingests every meeting you had today, updates tasks, writes a one-page day summary | `Reviews/YYYY-MM-DD Daily capture.md` + vault pages |
| [`standup-prep.md`](standup-prep.md) | Before a recurring program meeting | Brief: status vs. goal, blockers, what changed since last time, questions, actions by owner | `Reviews/YYYY-MM-DD Standup prep - <program>.md` |
| [`requirements-sweep.md`](requirements-sweep.md) | End of each day | Pulls genuinely new product requirements out of today's notes, de-duplicated | `Drafts/Requirements backlog.csv` |
| [`competitive-tracker.md`](competitive-tracker.md) | Weekly | Checks competitor changelogs/docs since last review and updates the competitive read | `Topics/Competitive read - <market>.md` + weekly note |
| [`weekly-lint.md`](weekly-lint.md) | Weekly | Health check: contradictions, stale claims, orphans, cold contacts, old follow-ups | `_meta/lint-report.md` |
| [`review-rollup.md`](review-rollup.md) | Monthly / quarterly | Evidence-backed rollup or self-review draft, tagged to your competencies | `Reviews/YYYY-MM-DD <Kind>.md` |

## Rules every workflow follows

- Read `AGENTS.md`, `_meta/config.md`, and `index.md` first.
- Use only facts found in sources; cite them. Write "unknown" or "no data" rather than guessing.
- If a source in `_meta/config.md` is unreachable from your harness, say so in the output
  and continue with `_inbox/` files or what you have. Never fabricate a meeting.
- Local writes only, unless `_meta/config.md` turns on a side effect for that workflow.
- Compare with the previous run's output (the last matching file in `Reviews/` or the log)
  so you report what is **new**, **resolved**, or **still open** instead of repeating yourself.
- Finish with a short report and append one entry to `_meta/log.md`.

## Writing your own

Copy any playbook and keep the same sections: **Inputs**, **Steps**, **Output**,
**Guardrails**. Keep personal values (names, links, goals) in `_meta/config.md`, not in the
playbook, so the playbook stays shareable.
