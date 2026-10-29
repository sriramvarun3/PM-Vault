---
type: reference
status: current
updated: ""
sources: []
tags: [config]
---

# Vault config

Personal settings the agent reads at the start of every session and every workflow.
Edit this file instead of editing the playbooks. **Never put passwords, tokens, or other
credentials here** — connect tools through your harness's own auth instead.

## Basics
- **Owner:** <your name>
- **Role:** <e.g. Product Manager, Platform>
- **Timezone:** <e.g. America/Los_Angeles>
- **Work days:** Mon–Fri

## Sources the agent may read
<!-- List what your harness can actually reach. Delete the lines you don't have.
     Anything not listed falls back to files in _inbox/ or text you paste. -->
- **Meetings (calendar + notes/transcripts):** <e.g. Google Calendar + Gemini notes | Zoom AI notes | Granola | Otter | a workplace search tool | none — I drop exports into _inbox/>
- **Chat:** <e.g. Slack via MCP | Teams | none>
- **Docs:** <e.g. Google Drive | Notion | Confluence | none>
- **Email:** <e.g. Gmail | Outlook | none>
- **Tickets / code:** <e.g. Jira | Linear | GitHub | none>

## Side effects (off unless you turn them on)
<!-- The agent writes inside the vault only. Each line below opts one workflow into one
     external action. Leave "none" to keep everything local. -->
- **Notify me when a workflow finishes:** none   <!-- e.g. "Slack DM to myself" -->
- **Requirements sweep target:** `Drafts/Requirements backlog.csv`   <!-- or a shared sheet URL, if your harness can edit it -->
- **Commit vault changes to local git:** no   <!-- never push a private vault to a public remote -->

## Workflow settings
- **Daily capture:** run at end of day; include meetings I attended; skip meetings shorter than 10 minutes.
- **Stand-up prep — program:** <program name>
- **Stand-up prep — goal source:** <doc or page that holds this month's goal>
- **Stand-up prep — attendees:** <names>
- **Requirements sweep — product area:** <product or program>
- **Requirements sweep — keywords:** <terms that signal a requirement for this area>
- **Competitive tracker — market:** <e.g. "product analytics tools">
- **Competitive tracker — competitors:** <list>
- **Competitive tracker — sources:** <changelogs, docs, pricing pages>
