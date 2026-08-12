# 26.1 Beta Testing

Materials for ReportPortal **26.1** beta: try-it scenarios, walkthroughs, and agent helpers.

> More content coming — e.g. Playwright examples with scenarios and how to walk through the app.

## Agent helpers (release quality dashboard)

| | |
|--|--|
| **Cursor skill** | [`.cursor/skills/reportportal-release-quality/`](.cursor/skills/reportportal-release-quality/) — Cursor only |
| **Portable prompt** | [`prompts/release-quality-dashboard.md`](prompts/release-quality-dashboard.md) — any MCP-capable agent |

Both need **ReportPortal MCP**. The skill builds a Canvas in Cursor; elsewhere paste the prompt (optionally with `reference.md` for gate/metric rules).

Details: skill [`SKILL.md`](.cursor/skills/reportportal-release-quality/SKILL.md) · metrics [`reference.md`](.cursor/skills/reportportal-release-quality/reference.md)
