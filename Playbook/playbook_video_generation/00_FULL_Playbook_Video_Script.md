# ReportPortal 26.1 Beta Playbook — Full video script

Master voiceover + recording bible for the full walkthrough.  
Use this file for ElevenLabs / TTS, silent screencast takes, and final edit.

| | |
|---|---|
| **Product** | ReportPortal 26.1 Beta |
| **Playbook** | [`../26.1_Beta_Playbook.html`](../26.1_Beta_Playbook.html) · `#walkthrough` Shots 1–6 |
| **Language** | English |
| **Target duration** | ~9–10 minutes |
| **Style** | Spoken demo · present tense · short sentences |
| **Record** | Silent screencast per part → VO from this script → mux |

### Parts (source files)

| # | Author | Topic | Duration | Source |
|---|--------|-------|----------|--------|
| 1 | Vika | Organizations | ~1:05 | [`01_Vika_part1_scenario.md`](01_Vika_part1_scenario.md) · `01_Vika_part1_Screen Recording…mov` |
| 2 | Anatolii | TMS by hand (Shots 2–4) | ~4:30 | [`02_Anatolii_TMS_scenario.md`](02_Anatolii_TMS_scenario.md) |
| 3 | Ilya | MCP at scale (Shot 5) | ~2:45 | [`03_Ilya_MCP_scenario.md`](03_Ilya_MCP_scenario.md) |
| 4 | Vika | Portfolio dashboard (Shot 6) | ~1:30 | [`01_Vika_part2_scenario.md`](01_Vika_part2_scenario.md) · `02_Vika_part2_Screen Recording…mov` |

### Global timeline (edit guide)

| Global | Part | Playbook shot |
|--------|------|---------------|
| **00:00–01:05** | 1 · Organizations | Shot 1 |
| **01:05–05:45** | 2 · TMS | Shots 2–4 |
| **05:45–08:30** | 3 · MCP | Shot 5 |
| **08:30–10:00** | 4 · Portfolio | Shot 6 |

Timestamps below: **Global** = full film · **Local** = within that part (for per-file recording).

---

## Part 1 — Organizations (Vika)

**Global 00:00–01:05** · Shot 1  
**On screen:** All Organizations → dedicated beta org (not Personal) → Projects → Organization users  
**Recording:** `01_Vika_part1_Screen Recording 2026-08-13 at 17.36.14.mov`

| Global | Local | Voiceover |
|--------|-------|-----------|
| **00:00** | 00:00 | Imagine this: you have several streams working in parallel. They all run tests — but the results land in one shared project. Everything gets mixed together. Ownership is unclear. And there’s no clean way to separate results or control access. |
| **00:15** | 00:15 | That’s exactly the pain we’re addressing with Organizations. Now you work inside one organization and create a separate project for each stream. Results stay separated. Access goes only to the right people. |
| **00:29** | 00:29 | Let’s see how it works in ReportPortal. Go to the All Organizations page — here you’ll see every organization available to you. |
| **00:36** | 00:36 | Open your dedicated beta organization — not the tile labelled Personal. Create as many projects as you want inside it, and you’re ready to start working. |
| **00:47** | 00:47 | User management is even easier now. Open the Organization users page, choose Manage assignment, and control a user’s access to every project in the organization from one place. |
| **01:02** | 01:02 | So now your organization is structured the way your teams work: separate projects, clear ownership, and simple access control. And that’s where the next part of the story begins — at the project level. |

---

## Part 2 — TMS walkthrough (Anatolii)

**Global 01:05–05:45** · Shots 2–4  
**On screen:** Stream A/B library & launches → Create Stream C → Loyalty cases → plan → manual launch Passed

| Global | Local | Voiceover / cue |
|--------|-------|-----------------|
| **01:05** | 00:00 | At the project level, every stream in ReportPortal runs the same Test Management path. Write scenarios once. Scope them for a sprint. Execute in a launch. That's the loop you'll walk today — first in streams that are already loaded, then in one you create yourself. |
| **01:23** | 00:18 | Inside your dedicated beta org — not Personal — Playbook is already loaded: a synthetic hotel-booking product split across two teams. Stream A covers search, cancellations, and mobile. Stream B covers checkout and payment. *[Projects list — open Stream A]* |
| **01:37** | 00:32 | The Test Case Library is the source of truth. Open Search & Filters in Stream A. Compare TMS-BOOK-001 — a Steps case — with TMS-BOOK-004 — a Text case. Same library. Two ways to describe a scenario. Tags like smoke and search sit on the case — search by TMS-BOOK in the name, not by folder number. |
| **01:57** | 00:52 | Switch to Stream B. Open TMS-BOOK-010 — room selection into checkout — and TMS-BOOK-013 — happy-path payment. Two streams. Isolated libraries. No mixing. |
| **02:13** | 01:08 | Milestones time-box the work. Test plans group cases for one goal. In Stream A you'll see search and cancellation coverage. In Stream B — smoke and payment plans. *[Quick cut: Milestones / Test Plans]* |
| **02:27** | 01:22 | Manual Launches are where execution lives — per-case status, comments, attachments. Here: passed smoke on TMS-BOOK-010 and 013. Here: failure evidence — a comment on TMS-BOOK-002 in Stream A, or TMS-BOOK-018 in Stream B. And cases still TO_RUN — like mobile TMS-MOB-001 — ready for a live mark. |
| **02:47** | 01:42 | Library → Milestone → Test plan → Manual launch. Stream A and B already show that path. Now you run it end to end — in a clean stream. |
| **02:59** | 01:54 | Back in your organization: Projects → Create project → name it Stream C → open and join. The library is empty on purpose. This is your practice ground. *[Create Stream C]* |
| **03:13** | 02:08 | In Stream C, create a folder — Loyalty & Reviews. Add two cases — copy the names exactly: TMS-LOY-001 — Earn loyalty points after a confirmed booking — Text type. TMS-LOY-002 — Redeem points at checkout — Steps type. Add a loyalty tag. These IDs stay stable when you use MCP later. |
| **03:37** | 02:32 | Create a milestone — Sprint 26 — Loyalty — and a test plan — Loyalty smoke — with both cases on it. Your sprint is scoped. Ready to execute. |
| **03:53** | 02:48 | Start a manual launch from Loyalty smoke. Open TMS-LOY-001. Mark it Passed. Add a short comment if you want. You just completed the full TMS loop by hand — in your own project. |
| **04:13** | 03:08 | One organization. Three streams. Each owns its library and results. Access stays per project. You walked Library → Plan → Launch once, by hand, in Stream C. Everything you created here will roll up when leadership looks at quality across the org. |
| **04:33** | 03:28 | Same path — more cases, more launches — without clicking through every wizard. That's what MCP and an AI assistant do next. Same workflow, at agent speed. |
| **04:47** | 03:42 | *[Hard cut → Part 3 · Ilya]* |

---

## Part 3 — MCP at scale (Ilya)

**Global 05:45–08:30** · Shot 5  
**On screen:** Profile API key → Cursor MCP → agent creates LOY-003 / plan / launch → UI proof  
**Assumes:** Stream C with Loyalty & Reviews, LOY-001/002, Sprint 26 — Loyalty, Loyalty smoke, one manual launch already exist.

| Global | Local | Voiceover / cue |
|--------|-------|-----------------|
| **05:45** | 00:00 | You already walked Library → Plan → Launch by hand in Stream C. Same path. More volume. That's MCP. |
| **05:57** | 00:12 | Connect an AI assistant to this beta instance. Avatar → My Profile → API Keys → Generate API Key — for example mcp-beta. Copy it once. It won't show again. Don't commit it. Don't paste it into a shared chat. *[Blur / hide the key]* |
| **06:13** | 00:28 | In Cursor — or your AI assistant — add ReportPortal MCP. Endpoint: tms.beta.reportportal.io/mcp. Authorization: Bearer with your API key. Skip the X-Project header — the agent picks Stream A, B, or C by projectKey from the URL. *[mcp.json / Tools & MCP connected]* |
| **06:33** | 00:48 | Ask the agent to extend Stream C — same Loyalty & Reviews folder. Create a Steps case: TMS-LOY-003 — Filter hotels by guest review score. Tags: loyalty, reviews, regression. Steps: open search results → set review score 8+ → apply → only matching hotels remain. |
| **06:55** | 01:10 | Put the new case on the same sprint. Reuse milestone Sprint 26 — Loyalty and plan Loyalty smoke. Add TMS-LOY-001, 002, and 003 to the plan. |
| **07:13** | 01:28 | Start a session without the launch wizard. Ask MCP to create a manual launch — Stream C — Loyalty smoke — from that plan, with all three loyalty cases. |
| **07:29** | 01:44 | Prove it in the UI. Stream C library: three loyalty cases side by side. Loyalty smoke: three cases on the plan. Manual Launches: Stream C — Loyalty smoke is there. Open it if you want — mark one execution Passed. *[Cut to UI]* |
| **07:53** | 02:08 | Same workflow you did by hand — folder, case, plan, launch — now at agent speed. Stream C is no longer empty. It's ready to roll up with Stream A and Stream B. |
| **08:07** | 02:22 | When release day comes, you still need one picture across every stream and every testing type. That's next — portfolio view with MCP. |
| **08:17** | 02:32 | *[Hard cut → Part 4 · Vika]* |

---

## Part 4 — Portfolio dashboard (Vika)

**Global 08:30–10:00** · Shot 6  
**On screen:** AI assistant builds release-gate / portfolio dashboard across A + B + C  
**Recording:** `02_Vika_part2_Screen Recording 2026-08-21 at 11.36.39.mov`

| Global | Local | Voiceover |
|--------|-------|-----------|
| **08:30** | 00:00 | Test Management System gives you a complete workflow — cases, plans, launches. But when you're managing multiple streams in parallel, manually organizing and reviewing results becomes a bottleneck. You need to see quality across all your projects instantly. |
| **08:46** | 00:16 | Not stream by stream. Not testing type by testing type. As one unified portfolio. This is where MCP and AI assistants change the game. As a Test Lead or Test Manager, you face a critical question before release: Are we ready to go? But here's the challenge: Your testing results are scattered across multiple projects — Stream A, B, C, and more. And you need to evaluate three different testing types: Manual test plans, Automated launches, and Agentic results from AI agents. A centralized portfolio dashboard is coming to ReportPortal. But you don't have to wait. With the ReportPortal MCP server, you can build it right now. |
| **09:26** | 00:56 | You ask an AI assistant to fetch data from all your projects and create a release gate dashboard. Let me show you how. I'll ask the agent to build a portfolio dashboard across all my projects that shows: Manual coverage and what's still to run, Automated test health and latest results, Agentic test status — all side by side. Then break down the risks, highlight what's healthy versus what needs attention, and give me a clear GO or NO-GO recommendation with the next actions. |
| **09:57** | 01:27 | And here's what we get: A complete release gate dashboard for the organization. The Test Lead sees the full testing picture instantly: which testing types are solid, where the risks are, what could block release. All of this — through MCP and an AI assistant, today. |

---

## Continuous voiceover (paste into TTS)

Generate **four** audio files (one per part), then align in the editor. Or one file with chapter markers at the `[PART n]` lines.

### Part 1 — Vika

```text
Imagine this: you have several streams working in parallel. They all run tests — but the results land in one shared project. Everything gets mixed together. Ownership is unclear. And there’s no clean way to separate results or control access.

That’s exactly the pain we’re addressing with Organizations. Now you work inside one organization and create a separate project for each stream. Results stay separated. Access goes only to the right people.

Let’s see how it works in ReportPortal. Go to the All Organizations page — here you’ll see every organization available to you.

Open your dedicated beta organization — not the tile labelled Personal. Create as many projects as you want inside it, and you’re ready to start working.

User management is even easier now. Open the Organization users page, choose Manage assignment, and control a user’s access to every project in the organization from one place.

So now your organization is structured the way your teams work: separate projects, clear ownership, and simple access control. And that’s where the next part of the story begins — at the project level.
```

### Part 2 — Anatolii

```text
At the project level, every stream in ReportPortal runs the same Test Management path. Write scenarios once. Scope them for a sprint. Execute in a launch. That's the loop you'll walk today — first in streams that are already loaded, then in one you create yourself.

Inside your dedicated beta org — not Personal — Playbook is already loaded: a synthetic hotel-booking product split across two teams. Stream A covers search, cancellations, and mobile. Stream B covers checkout and payment.

The Test Case Library is the source of truth. Open Search and Filters in Stream A. Compare TMS-BOOK-001 — a Steps case — with TMS-BOOK-004 — a Text case. Same library. Two ways to describe a scenario. Tags like smoke and search sit on the case — search by TMS-BOOK in the name, not by folder number.

Switch to Stream B. Open TMS-BOOK-010 — room selection into checkout — and TMS-BOOK-013 — happy-path payment. Two streams. Isolated libraries. No mixing.

Milestones time-box the work. Test plans group cases for one goal. In Stream A you'll see search and cancellation coverage. In Stream B — smoke and payment plans.

Manual Launches are where execution lives — per-case status, comments, attachments. Here: passed smoke on TMS-BOOK-010 and 013. Here: failure evidence — a comment on TMS-BOOK-002 in Stream A, or TMS-BOOK-018 in Stream B. And cases still TO_RUN — like mobile TMS-MOB-001 — ready for a live mark.

Library. Milestone. Test plan. Manual launch. Stream A and B already show that path. Now you run it end to end — in a clean stream.

Back in your organization: Projects. Create project. Name it Stream C. Open and join. The library is empty on purpose. This is your practice ground.

In Stream C, create a folder — Loyalty and Reviews. Add two cases — copy the names exactly: TMS-LOY-001 — Earn loyalty points after a confirmed booking — Text type. TMS-LOY-002 — Redeem points at checkout — Steps type. Add a loyalty tag. These IDs stay stable when you use MCP later.

Create a milestone — Sprint 26 — Loyalty — and a test plan — Loyalty smoke — with both cases on it. Your sprint is scoped. Ready to execute.

Start a manual launch from Loyalty smoke. Open TMS-LOY-001. Mark it Passed. Add a short comment if you want. You just completed the full TMS loop by hand — in your own project.

One organization. Three streams. Each owns its library and results. Access stays per project. You walked Library, Plan, Launch once, by hand, in Stream C. Everything you created here will roll up when leadership looks at quality across the org.

Same path — more cases, more launches — without clicking through every wizard. That's what MCP and an AI assistant do next. Same workflow, at agent speed.
```

### Part 3 — Ilya

```text
You already walked Library, Plan, Launch by hand in Stream C. Same path. More volume. That's MCP.

Connect an AI assistant to this beta instance. Avatar. My Profile. API Keys. Generate API Key — for example mcp-beta. Copy it once. It won't show again. Don't commit it. Don't paste it into a shared chat.

In Cursor — or your AI assistant — add ReportPortal MCP. Endpoint: tms.beta.reportportal.io/mcp. Authorization: Bearer with your API key. Skip the X-Project header — the agent picks Stream A, B, or C by projectKey from the URL.

Ask the agent to extend Stream C — same Loyalty and Reviews folder. Create a Steps case: TMS-LOY-003 — Filter hotels by guest review score. Tags: loyalty, reviews, regression. Steps: open search results, set review score eight plus, apply, only matching hotels remain.

Put the new case on the same sprint. Reuse milestone Sprint 26 — Loyalty and plan Loyalty smoke. Add TMS-LOY-001, 002, and 003 to the plan.

Start a session without the launch wizard. Ask MCP to create a manual launch — Stream C — Loyalty smoke — from that plan, with all three loyalty cases.

Prove it in the UI. Stream C library: three loyalty cases side by side. Loyalty smoke: three cases on the plan. Manual Launches: Stream C — Loyalty smoke is there. Open it if you want — mark one execution Passed.

Same workflow you did by hand — folder, case, plan, launch — now at agent speed. Stream C is no longer empty. It's ready to roll up with Stream A and Stream B.

When release day comes, you still need one picture across every stream and every testing type. That's next — portfolio view with MCP.
```

### Part 4 — Vika

```text
Test Management System gives you a complete workflow — cases, plans, launches. But when you're managing multiple streams in parallel, manually organizing and reviewing results becomes a bottleneck. You need to see quality across all your projects instantly.

Not stream by stream. Not testing type by testing type. As one unified portfolio. This is where MCP and AI assistants change the game. As a Test Lead or Test Manager, you face a critical question before release: Are we ready to go? But here's the challenge: Your testing results are scattered across multiple projects — Stream A, B, C, and more. And you need to evaluate three different testing types: Manual test plans, Automated launches, and Agentic results from AI agents. A centralized portfolio dashboard is coming to ReportPortal. But you don't have to wait. With the ReportPortal MCP server, you can build it right now.

You ask an AI assistant to fetch data from all your projects and create a release gate dashboard. Let me show you how. I'll ask the agent to build a portfolio dashboard across all my projects that shows: Manual coverage and what's still to run, Automated test health and latest results, Agentic test status — all side by side. Then break down the risks, highlight what's healthy versus what needs attention, and give me a clear GO or NO-GO recommendation with the next actions.

And here's what we get: A complete release gate dashboard for the organization. The Test Lead sees the full testing picture instantly: which testing types are solid, where the risks are, what could block release. All of this — through MCP and an AI assistant, today.
```

---

## Full shot list (silent recording)

| Global | Part | Shot | On screen |
|--------|------|------|-----------|
| 00:00–00:29 | 1 | 1 | Pain setup (optional B-roll / title) |
| 00:29–01:05 | 1 | 1 | All Organizations → dedicated org → Projects → Organization users |
| 01:05–02:47 | 2 | 2 | Stream A: 001/004; Stream B: 010/013; plans; launches (Passed + failure + TO_RUN) |
| 02:59–03:13 | 2 | 3 | Create Stream C |
| 03:13–04:13 | 2 | 4 | Folder, LOY-001/002, milestone, plan, launch → Passed |
| 04:13–04:47 | 2 | — | Handoff hold: three projects / Stream C |
| 05:45–06:33 | 3 | 5 | API key (blurred) + Cursor MCP connected |
| 06:33–07:29 | 3 | 5 | Agent: LOY-003 → plan → launch |
| 07:29–08:17 | 3 | 5 | UI proof + handoff |
| 08:30–10:00 | 4 | 6 | Portfolio / release gate dashboard |

---

## Appendix — MCP prompts (Part 3 recording)

Replace `<your-org-slug>` with the org slug from the project URL (`organization-slug.stream-c`).

### Create test case

```text
Use the ReportPortal MCP server on projectKey "<your-org-slug>.stream-c".

Find or create folder "Loyalty & Reviews".
Create a STEPS test case named
"[TMS-LOY-003] Filter hotels by guest review score"
with tags loyalty, reviews, regression.
Steps: open search results → set review score 8+ → apply → only matching hotels remain.

Reply with the folder id and the new case id.
```

### Milestone & plan

```text
Use the ReportPortal MCP server on projectKey "<your-org-slug>.stream-c".

Create milestone "Sprint 26 — Loyalty" (type SPRINT, status TESTING)
with start/end dates this month — or reuse it if it already exists.
Create or reuse test plan "Loyalty smoke" on that milestone and add
TMS-LOY-001, TMS-LOY-002, and TMS-LOY-003.

Reply with the milestone id, plan id, and the case ids on the plan.
```

### Manual launch

```text
Use the ReportPortal MCP server on projectKey "<your-org-slug>.stream-c".

Create a manual launch "Stream C — Loyalty smoke" from plan "Loyalty smoke",
including TMS-LOY-001, TMS-LOY-002, and TMS-LOY-003, started now.

Reply with the launch id and the execution ids.
```

---

## Production notes

- **One voice** recommended for the full film (ElevenLabs); parts can still be recorded by different people on camera if needed.
- **Do not** show a readable API key.
- If Stream C already exists: in Part 2 say “Open Stream C — your practice stream” instead of Create.
- If MCP is already connected: shorten Part 3 setup (05:57–06:33).
- Tips and Feedback sections of the HTML playbook are **out of scope** for this video.
- Keep Manual / Automated / Agentic as **separate** lines on the portfolio — do not blend into one org pass rate.
- Suggested edit order: sync Part 1 footage → Part 2 silent take → Part 3 silent take → Part 4 footage → lay VO → chapter titles between parts (optional).
