# Connecting your sources

The vault never depends on a specific tool. Workflows ask for *a meeting source*, *a chat
source*, and so on; you say what you have in `_meta/config.md`. If the agent can't reach a
source, it falls back to files you drop in `_inbox/` or text you paste.

| Source | Examples of how agents reach it | Manual fallback |
|---|---|---|
| Meetings: calendar | Calendar MCP server; workplace search (e.g. Glean); built-in harness connectors | Paste today's agenda |
| Meetings: notes and transcripts | AI notetaker exports or APIs (Zoom, Google Meet/Gemini notes, Teams, Granola, Otter, Fireflies); workplace search | Export to `_inbox/`, or dictate a 2-minute recap |
| Chat | Slack or Teams MCP server; workplace search | Paste the thread |
| Docs | Google Drive, Notion, or Confluence MCP servers; workplace search | Paste the relevant section plus the link |
| Email | Gmail or Outlook MCP server | Forward or paste |
| Tickets and code | Jira, Linear, or GitHub MCP servers; the `gh` CLI | Paste the ticket |
| Web | The harness's web search or fetch tool | Paste the page |

## Choosing what to connect

1. **Start with zero connectors.** Dictate recaps and use `log:`. Most of the value is the
   structure, not the automation.
2. **Add meeting notes next.** That's what makes `daily-capture` hands-off.
3. **Then chat and docs**, for stand-up prep and the requirements sweep.

## Data hygiene

- Connect only tools your organization has approved for this data, and only accounts you're
  allowed to use.
- Store **extracts plus canonical links** for internal docs, not full copies.
- Meeting notes should come from tools and meetings where recording or transcription was
  agreed. The vault never records anything itself.
- Credentials belong in your harness's auth or a secrets manager, never in the vault.
