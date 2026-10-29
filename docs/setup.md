# Setup — use the vault with any agent

The vault is just a folder of Markdown. Any agent that can read and write files can run
it. `AGENTS.md` is the contract, `workflows/` holds the repeatable jobs, and
`skills/vault-capture/SKILL.md` is the capture procedure.

## 1. Make it yours (all harnesses)

1. Create your vault from this template (GitHub **Use this template**, or clone/copy).
   **Make your copy private** — it will hold notes about people and internal work.
2. Fill in `_meta/config.md`: timezone, which sources your agent can reach, and which
   side effects (if any) you allow.
3. Replace `_reference/competencies.md` with your organization's framework.
4. Run `python3 _bin/vault-lint.py` once to confirm Python works.

## 2. Pick your harness

### Claude Code
- Start it in the vault folder: `cd ~/pm-vault && claude`. `CLAUDE.md` imports `AGENTS.md`.
- Optional: make the capture skill discoverable as a project skill:
  `mkdir -p .claude/skills && cp -r skills/vault-capture .claude/skills/`.
- Connect meetings, chat, and docs through MCP servers your organization approves.
- Try: `log: met Alex, she owns eval infra, follow up in 2 weeks`, or
  `run workflows/daily-capture.md`.

### Codex (CLI or app)
- Start it in the vault folder. Codex reads `AGENTS.md` automatically.
- `AGENTS.md` points to `skills/vault-capture/SKILL.md`, so capture works without
  installing anything. If your Codex version supports skills, you can also copy
  `skills/vault-capture` into its skills folder (see the Codex docs).
- Connect sources through MCP servers configured for Codex.

### Glean Tau
- Open the vault folder as the chat's working folder (or add an instruction to your
  personal `AGENTS.md`: "my vault is at <path>; follow its AGENTS.md").
- Add the capture skill as a personal skill (copy `skills/vault-capture` into your
  personal skills folder, or create it from the Skills Hub).
- Workplace sources (calendar, meeting notes, chat, docs) come through Glean's connectors.
- Schedule workflows with **Automations** (section 3).

### Cursor, Gemini CLI, OpenCode, and others
- Most coding agents read `AGENTS.md` from the folder they open. If yours uses a
  different file name (for example `GEMINI.md`), add a one-line file that tells it to
  follow `AGENTS.md`, the same way `CLAUDE.md` does.

### No agent harness (chat apps)
- Put `AGENTS.md` and the relevant template in a project's instructions, paste your
  notes, and ask for the files it would write. Save them into the vault yourself.
  Slower, but the structure still compounds.

## 3. Schedule the workflows

Every workflow file has a `suggested_schedule`. The prompt is always the same shape:

> Follow `workflows/<name>.md` in this vault. Read `AGENTS.md` and `_meta/config.md` first.

| Harness | How to schedule |
|---|---|
| Glean Tau | Create an Automation per workflow with the prompt above, the working folder set to the vault, and the schedule from the playbook. |
| Claude Code | Run headless from `cron` or `launchd`: `cd ~/pm-vault && claude -p "Follow workflows/daily-capture.md…"`. Give it permission to edit files in the vault (see `claude --help` for permission flags). |
| Codex | Run non-interactively from `cron` or `launchd`: `cd ~/pm-vault && codex exec "Follow workflows/daily-capture.md…"`, with a sandbox setting that allows writes in the workspace only. |
| Anything else | Any scheduler that can run your agent's command-line mode in the vault folder. |

Example crontab (times use the machine's local timezone):

```cron
0 18 * * 1-5  cd ~/pm-vault && claude -p "Follow workflows/daily-capture.md. Read AGENTS.md and _meta/config.md first." >> _meta/cron.log 2>&1
30 18 * * 1-5 cd ~/pm-vault && claude -p "Follow workflows/requirements-sweep.md. Read AGENTS.md and _meta/config.md first." >> _meta/cron.log 2>&1
0 16 * * 5    cd ~/pm-vault && claude -p "Follow workflows/weekly-lint.md. Read AGENTS.md and _meta/config.md first." >> _meta/cron.log 2>&1
```

Things to know about unattended runs:
- The computer must be awake. `launchd` on macOS can catch up on missed runs; plain `cron` can't.
- Connectors must stay signed in without a prompt; otherwise the run falls back to `_inbox/`.
- Give scheduled runs the **least** access they need: edit files in the vault, read from
  your sources, no messaging unless you turned it on in `_meta/config.md`.
- Never put passwords or tokens in a prompt, a workflow, or the config.

## 4. Optional: local version history

Keep your private vault in a local git repo (`git init`) so every change the agent makes
is recoverable. If you schedule snapshot commits, keep them local — never push a private
vault to a public remote.
