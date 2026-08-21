# Prompt: Portfolio dashboard

Copy into any MCP-capable AI agent chat (Cursor, Copilot, Claude Desktop, etc.):

---

Using the ReportPortal MCP server, build a portfolio dashboard
across projects in my beta organization (Stream A, Stream B, and Stream C if it exists).

Include:
- Manual — Test Plans / Manual Launches
- Automated — automated test launches
- Agentic — AI agent / CheckSuite results

Requirements:
1. Aggregate quality status across projects
2. Break down by testing type: Manual / Automated / Agentic
3. Highlight top risks and incomplete areas
4. Show what looks healthy vs what needs attention
5. Give a clear GO / NO-GO recommendation with next actions
6. Format as a dashboard-style view with a short executive summary (use Canvas when available)

Metric rules:
- Do not blend Manual + Automated + Agentic into one org pass rate
- Automated / Agentic: evaluate the latest suite or CheckSuite only (status, freshness, PB/TI)
- Manual: use plan coverage (covered/total) and open TO_RUN, not lifetime pass % across all demo launches
- Split defects by intent: PB (blocks) · TI (classify) · AB/SI (test debt)
- Gate = explicit checklist; GO only if all criteria pass

Widgets:
- Gate readiness donut
- Defect mix
- Freshness vs SLA
- Testing-type health bars
- Automated tests stacked charts
- Manual coverage + TO_RUN backlog
- Agentic latest-status donut
- Prioritized next actions
