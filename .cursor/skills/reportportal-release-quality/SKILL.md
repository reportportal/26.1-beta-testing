---
name: reportportal-release-quality
description: >-
  Builds a release quality / go-no-go dashboard across ReportPortal projects
  using MCP (Manual, Automation, Agentic). Use when the user asks for release
  readiness, org quality roll-up, go/no-go, test plan coverage, or a
  ReportPortal quality dashboard.
---

# ReportPortal release quality dashboard

Build a **decision dashboard** from live ReportPortal MCP data. Output a Cursor **Canvas** (not a markdown table dump).

## Prerequisites

- ReportPortal MCP server(s) connected (e.g. `reportportal-api`, `reportportal-e2e`)
- Read the canvas skill before writing any `.canvas.tsx`
- Discover project keys from MCP config (`X-Project` / `projectKey`) or user input

## Workflow

1. **Discover projects** available via MCP. Query each configured project.
2. **Pull data** (read-only):
   - `get_launches` — automation + agentic (use `launchType` / CheckSuite attributes)
   - `get_manual_launches` — TMS manual launches + `toRun` + linked test plans
   - `get_milestones_by_filter` — plan `covered/total`, release milestone status
3. **Classify launches**
   - **Automation**: `launchType=AUTOMATION` without CheckSuite / `test_session` markers
   - **Agentic**: `launchType=AGENTIC` OR CheckSuite / `test_session_id` attributes
   - **Manual**: TMS `get_manual_launches` (preferred over MANUAL rows in `get_launches`)
4. **Compute valid metrics** — follow [reference.md](reference.md). Do **not** blend Manual + Automation + Agentic into one org pass rate.
5. **Evaluate gate checklist** — GO only if all criteria pass (see reference).
6. **Render a Canvas** with widgets (see Output). Embed computed numbers inline — no `fetch()` in the canvas.
7. **Chat summary**: 3–6 lines — verdict, top blockers, link to the canvas.

## Metric rules (must follow)

| Type | Gate inputs | Diagnosis | Do not use |
|------|-------------|-----------|------------|
| Automation | Latest suite per project: status, freshness (≤7d default), open PB/TI | Pass % of that latest run; AB/SI separately | Lifetime pass %; blend with Manual |
| Manual | Critical plan coverage (`covered/total`); open TO_RUN on incomplete launches | Failed on open launches; milestone status | Pass % across all historical demo launches |
| Agentic | Latest CheckSuite status + open TI | Skip rate; suite breadth | Average of all past agent sessions |

**Defect taxonomy**: PB = product risk (blocks GO) · TI = unknown (classify first) · AB/SI = test debt (separate).

## Output — Canvas layout

Write to the workspace canvases dir as `release-quality-dashboard.canvas.tsx`.

Required sections (visual first):

1. **Header** — org/projects, snapshot date, NO-GO/GO pill  
2. **Callout** — verdict + why  
3. **Widget row** — Gate readiness (donut + checklist pills) · Defect mix (PB/TI/AB) · Freshness bars vs SLA  
4. **KPI strip** — gate, auto suites red, critical coverage %, TO_RUN, latest agentic  
5. **Health by type** — UsageBars for Automation / Manual / Agentic  
6. **Automation charts** — stacked executions + defect taxonomy; small detail table  
7. **Manual charts** — plan coverage % bars; TO_RUN backlog; critical-path UsageBar  
8. **Agentic + projects** — latest CheckSuite donut; per-project strip  
9. **Gate criteria table** + **Next actions** (TodoList)  
10. Collapsible **metric validity notes** (short)

Design: flat Cursor canvas components only (`cursor/canvas`). No gradients, emojis, box-shadows, or rainbow cards.

## Scope honesty

If MCP is bound to specific `X-Project` headers, state that the roll-up covers those projects only — not every project on the instance.

## Additional resources

- Metric dictionary, gate criteria, anti-patterns: [reference.md](reference.md)
- Example user prompts: [examples.md](examples.md)
- Repo copy-paste prompt: `prompts/release-quality-dashboard.md` (repository root)
