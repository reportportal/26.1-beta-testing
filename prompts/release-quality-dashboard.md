# Prompt: Release quality dashboard

Copy into Cursor chat (with ReportPortal MCP connected):

---

Using the ReportPortal MCP server, build a **release quality dashboard** across all projects available to me.

Include:
- **Manual** — Test Plans / Manual Launches
- **Automation** — automated launches
- **Agentic** — AI agent / CheckSuite results

Requirements:
1. Aggregate quality status across projects
2. Break down by testing type: Manual / Automation / Agentic
3. Highlight top risks and incomplete areas
4. Show what looks healthy vs what needs attention
5. Give a clear **GO / NO-GO** with next actions
6. Format as a **dashboard-style Canvas** with an executive summary

Metric rules (follow these):
- Do **not** blend Manual + Automation + Agentic into one org pass rate
- Automation / Agentic: evaluate the **latest** suite/CheckSuite only (status, freshness, PB/TI)
- Manual: use **plan coverage** (`covered/total`) and open **TO_RUN** — not lifetime pass % across all demo launches
- Split defects: **PB** (blocks) · **TI** (classify) · **AB/SI** (test debt)
- Gate = explicit checklist; GO only if all criteria pass

Widgets to include: gate readiness donut, defect mix, freshness vs SLA, type health bars, automation stacked charts, manual coverage + TO_RUN backlog, agentic latest donut, next actions.
