# 26.1 Beta Testing — skills & prompts

Shared prompts and Agent Skills for ReportPortal **26.1** beta workflows.

## Compatibility

| Artifact | Portable? | Where it works |
|----------|-----------|----------------|
| **Skill** (`.cursor/skills/…`) | **No** — Cursor format | [Cursor](https://cursor.com) Agent Skills (auto-discovery / named invoke) |
| **Prompt** (`prompts/…`) | **Yes** | Any AI chat that can call ReportPortal MCP (Cursor, Claude Desktop, etc.) |
| **Metric rules** (`reference.md`) | **Yes** (as knowledge) | Can be copied into another tool’s system prompt, docs, or skill format |
| **ReportPortal MCP** | **Yes** (MCP protocol) | Any MCP-compatible client with a configured ReportPortal server |

**Summary:** Skill = Cursor. Prompt = portable. Without ReportPortal MCP, neither path can build a live dashboard.

## Contents

| Path | What it is |
|------|------------|
| [`.cursor/skills/reportportal-release-quality/`](.cursor/skills/reportportal-release-quality/) | **Cursor skill:** live release quality / go-no-go dashboard from ReportPortal MCP |
| [`prompts/release-quality-dashboard.md`](prompts/release-quality-dashboard.md) | **Portable prompt:** same dashboard intent for any MCP-capable agent |

## How to use

### Option A — Prompt (any MCP-capable agent)

1. Connect ReportPortal MCP in your client (token + project / `X-Project` as required).
2. Open [`prompts/release-quality-dashboard.md`](prompts/release-quality-dashboard.md) and paste the prompt into chat.
3. Optional: attach or paste [metric rules](.cursor/skills/reportportal-release-quality/reference.md) if the agent should follow the same gate / validity rules strictly.

Works outside Cursor. Visual **Canvas** output is Cursor-specific; other clients may return markdown / HTML instead.

### Option B — Skill (Cursor only)

1. Open this repository in **Cursor** (project skills under `.cursor/skills/` load automatically).
2. Ask for a release quality / go-no-go / org dashboard — or mention the skill by name: `reportportal-release-quality`.

The agent will query MCP, apply valid metrics (latest automation/agentic, manual plan coverage), and write a **Canvas** dashboard.

## Requirements

**Always**
- ReportPortal MCP server(s) configured and authenticated
- Access to the projects you want in the roll-up

**Cursor skill + Canvas dashboard**
- Cursor with Agent Skills enabled
- Canvas support for the visual dashboard file

**Other agents**
- Use the portable prompt; expect a text/markdown (or that client’s) dashboard, not a `.canvas.tsx` unless the client supports an equivalent

## Notes

- Skills/prompts describe **how** to build the dashboard from **your** live data. They do not ship a frozen snapshot.
- Metric rules and gate checklist: [`.cursor/skills/reportportal-release-quality/reference.md`](.cursor/skills/reportportal-release-quality/reference.md)
