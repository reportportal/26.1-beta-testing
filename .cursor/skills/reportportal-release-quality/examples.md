# Examples

## User prompts that should trigger this skill

- “Build a release quality dashboard across all my ReportPortal projects”
- “Give me a go / no-go for the release from Manual, Automation, and Agentic”
- “Org quality roll-up with risks and next actions”
- “Release readiness from ReportPortal MCP”

## Expected agent behavior (short)

1. Call ReportPortal MCP tools for each configured project.
2. Compute gate + type-valid metrics (see `reference.md`).
3. Write `release-quality-dashboard.canvas.tsx` with visual widgets.
4. Reply with verdict + canvas link.

## Sample chat reply shape

```text
Verdict: NO-GO — N of M gate criteria failing.

Top blockers:
- … (automation / manual / milestone)

Open the dashboard beside the chat: [release-quality-dashboard](…/canvases/release-quality-dashboard.canvas.tsx)
```

## Sample gate outcome (illustrative)

Do not hardcode these numbers into the skill output — always recompute from MCP.

| Criterion | Example evidence |
|-----------|------------------|
| Auto green | 2/2 suites FAILED |
| Auto fresh | 44d > 7d SLA |
| PB cleared | 15 PB · 2 TI |
| Critical plans | 2/23 cases (8.7%) |
| TO_RUN clear | 21 open |
| Agentic TI | PASSED · TI 1 |
| Release MS | TESTING · overdue |
