# Metric reference — release quality dashboard

## Gate checklist (default)

GO only when **all** pass. Adjust thresholds with the user if needed.

| ID | Criterion | Pass when |
|----|-----------|-----------|
| auto-green | Latest automation suite green on each project | No FAILED/INTERRUPTED latest suites |
| auto-fresh | Automation freshness | Latest auto ended within **7 days** (configurable) |
| auto-pb | Product risk cleared | Open PB = 0 and TI = 0 on latest auto (or explicitly accepted) |
| manual-critical | Critical manual plans complete | Every critical plan `covered == total` |
| manual-open | Blocking TO_RUN cleared | No TO_RUN on release-blocking incomplete launches |
| agentic-ti | Latest agentic clean | Latest CheckSuite PASSED and TI = 0 |
| release-ms | Release milestone coherent | Active RELEASE not overdue without decision (COMPLETED or re-baselined) |

## How to compute

### Automation (per project)

1. Take **latest** automation launch for the primary suite (or latest by `startTime` if one suite).
2. Record: status, passed/failed/skipped, defects by type, end time → age in days.
3. Pass % = `passed / (passed + failed + skipped)` of **that** launch only.

### Agentic

1. Prefer `launchType=AGENTIC`.
2. Also treat CheckSuite / `test_session_id` / `check_suite` attributes as agentic even if typed AUTOMATION.
3. Gate uses **latest** CheckSuite only.

### Manual

1. Prefer **plan coverage** from milestones / test plans: `covered / total`.
2. Mark critical plans with the user (default heuristic: Checkout, Payment, Mobile / smoke paths).
3. Open work = incomplete launches with `toRun > 0` (work queue). Do **not** sum every historical demo launch into a “quality %”.
4. If the same plan appears in multiple incomplete launches, say so — coverage is the deduped signal; TO_RUN is the queue.

## Anti-patterns (do not ship these as headlines)

| Misleading metric | Why | Replace with |
|-------------------|-----|--------------|
| Single org pass % (Manual+Auto+Agentic) | Different populations and freshness | Gate checklist + per-type widgets |
| Manual pass % across all launches | Demo re-runs double-count plans | Plan coverage + open TO_RUN |
| `executed / (executed + TO_RUN)` over all history | Old demos inflate “completion” | Critical-plan coverage % |
| Averaging all agentic sessions | Dilutes the only current signal | Latest CheckSuite + TI |
| Treating AB like PB | Wrong owner and severity | Split PB / TI / AB+SI |

## Widget → metric map

| Widget | Metric |
|--------|--------|
| Gate donut | count(pass) / count(criteria) |
| Defect mix | PB, TI, AB+SI on latest auto |
| Freshness bars | days since latest auto/agentic vs SLA line |
| Auto stacked bars | P/F/S on latest suite per project |
| Manual coverage bars | planPct(covered, total) per plan |
| TO_RUN backlog | toRun (+ failed) on incomplete launches |
| Agentic donut | P/F/S of latest CheckSuite |
