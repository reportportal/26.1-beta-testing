# Prompts for TMS features: Create test case, Plan, Start manual launch

Copy into any MCP-capable AI agent chat (Cursor, Copilot, Claude Desktop, etc.):

---

## Create test case

Use the ReportPortal MCP server on projectKey "{stream-c-project-key}"

Find or create folder "Loyalty & Reviews".
Create a STEPS test case named
"[TMS-LOY-003] Filter hotels by guest review score"
with tags loyalty, reviews, regression.
Steps: open search results → set review score 8+ → apply → only matching hotels remain.

Reply with the folder id and the new case id.

## Plan

Use the ReportPortal MCP server on projectKey "{stream-c-project-key}"

Create milestone "Sprint 26 — Loyalty" (type SPRINT, status TESTING)
with start/end dates this month — or reuse it if it already exists.
Create or reuse test plan "Loyalty smoke" on that milestone and add
TMS-LOY-001, TMS-LOY-002, and TMS-LOY-003.

Reply with the milestone id, plan id, and the case ids on the plan.

## Start manual launch

Use the ReportPortal MCP server on projectKey "{stream-c-project-key}"

Create a manual launch "Stream C — Loyalty smoke" from plan "Loyalty smoke",
including TMS-LOY-001, TMS-LOY-002, and TMS-LOY-003, started now.

Reply with the launch id and the execution ids.