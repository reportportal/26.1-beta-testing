# MCP — same TMS path at scale — voiceover script

| | |
|---|---|
| **Author** | Ilya |
| **Part** | 3 of 4 (full playbook video) |
| **Target duration** | ~2:30–3:00 |
| **Covers** | Playbook Shot 5 — API key → MCP connect → TMS-LOY-003 → plan → launch → UI proof |
| **Previous** | [02 — TMS walkthrough (Anatolii)](02_Anatolii_TMS_scenario.md) |
| **Next** | [04 — Portfolio dashboard (Vika)](01_Vika_part2_scenario.md) |
| **Playbook** | `#mcp-setup` · `#mcp-cases` · `#mcp-planning` · `#mcp-launches` · `#walkthrough` Shot 5 |

**Style:** spoken demo, present tense, short sentences (match Vika Part 1 / Anatolii).

**Record:** silent screencast (ReportPortal UI + Cursor / AI assistant); voiceover from the script below.

**Out of scope:** Organizations setup, Stream C creation by hand, portfolio dashboard / GO–NO-GO (Vika Part 2).

**Assumes from previous segment:** Stream C exists with folder Loyalty & Reviews, TMS-LOY-001 / 002, milestone Sprint 26 — Loyalty, plan Loyalty smoke, and at least one manual launch.

---

## Script

**00:00**  
You already walked Library → Plan → Launch by hand in Stream C.  
Same path. More volume. That's MCP.

**00:12**  
Connect an AI assistant to this beta instance.  
Avatar → My Profile → API Keys → Generate API Key — for example mcp-beta.  
Copy it once. It won't show again. Don't commit it. Don't paste it into a shared chat.

**00:28**  
In Cursor — or your AI assistant — add ReportPortal MCP.  
Endpoint: tms.beta.reportportal.io/mcp.  
Authorization: Bearer with your API key.  
Skip the X-Project header — the agent picks Stream A, B, or C by projectKey from the URL.  
*[On screen: mcp.json / Tools & MCP connected; optional: “What ReportPortal tools are available?”]*

**00:48**  
Ask the agent to extend Stream C — same Loyalty & Reviews folder.  
Create a Steps case: TMS-LOY-003 — Filter hotels by guest review score.  
Tags: loyalty, reviews, regression.  
Steps: open search results → set review score 8+ → apply → only matching hotels remain.  
*[On screen: agent prompt + tool calls]*

**01:10**  
Put the new case on the same sprint.  
Reuse milestone Sprint 26 — Loyalty and plan Loyalty smoke.  
Add TMS-LOY-001, 002, and 003 to the plan.  
*[On screen: agent confirms milestone / plan / case ids]*

**01:28**  
Start a session without the launch wizard.  
Ask MCP to create a manual launch — Stream C — Loyalty smoke — from that plan, with all three loyalty cases.  
*[On screen: agent returns launch id]*

**01:44**  
Prove it in the UI.  
Stream C library: three loyalty cases side by side.  
Loyalty smoke: three cases on the plan.  
Manual Launches: Stream C — Loyalty smoke is there.  
Open it if you want — mark one execution Passed.  
*[On screen: cut to ReportPortal UI — library → plan → launch]*

**02:08**  
Same workflow you did by hand — folder, case, plan, launch — now at agent speed.  
Stream C is no longer empty. It's ready to roll up with Stream A and Stream B.

**02:22**  
When release day comes, you still need one picture across every stream and every testing type.  
That's next — portfolio view with MCP.

**02:32**  
*[Hard cut → Vika Part 2: portfolio / release gate dashboard]*

---

## Shot list (silent recording)

| Block | Time | On screen |
|-------|------|-----------|
| Bridge from TMS | 00:00–00:12 | Stream C library (LOY-001 / 002) or wide org |
| API key | 00:12–00:28 | Profile → API Keys → Generate (blur/hide key) |
| MCP connect | 00:28–00:48 | Cursor mcp.json / Tools & MCP green |
| Create LOY-003 | 00:48–01:10 | Agent chat + MCP tools |
| Plan attach | 01:10–01:28 | Agent adds cases to Loyalty smoke |
| Launch via MCP | 01:28–01:44 | Agent creates Stream C — Loyalty smoke |
| UI proof | 01:44–02:08 | Library → plan → Manual Launches |
| Handoff to Vika | 02:08–02:32 | Hold on launch or org projects |

---

## Agent prompts (for recording — replace project key)

Use these (or playbook equivalents) so the take matches the script.

**Test case**

```text
Use the ReportPortal MCP server on projectKey "<your-org-slug>.stream-c".

Find or create folder "Loyalty & Reviews".
Create a STEPS test case named
"[TMS-LOY-003] Filter hotels by guest review score"
with tags loyalty, reviews, regression.
Steps: open search results → set review score 8+ → apply → only matching hotels remain.

Reply with the folder id and the new case id.
```

**Milestone & plan**

```text
Use the ReportPortal MCP server on projectKey "<your-org-slug>.stream-c".

Create milestone "Sprint 26 — Loyalty" (type SPRINT, status TESTING)
with start/end dates this month — or reuse it if it already exists.
Create or reuse test plan "Loyalty smoke" on that milestone and add
TMS-LOY-001, TMS-LOY-002, and TMS-LOY-003.

Reply with the milestone id, plan id, and the case ids on the plan.
```

**Manual launch**

```text
Use the ReportPortal MCP server on projectKey "<your-org-slug>.stream-c".

Create a manual launch "Stream C — Loyalty smoke" from plan "Loyalty smoke",
including TMS-LOY-001, TMS-LOY-002, and TMS-LOY-003, started now.

Reply with the launch id and the execution ids.
```

---

## Notes

- ~320 words → ~2:30–3:00 at calm demo pace.
- Do **not** recreate Stream C or LOY-001/002 by hand — Anatolii already did that.
- Do **not** build the org portfolio dashboard or say GO/NO-GO — Vika Part 2.
- Hide / blur the API key in frame; never leave it readable in the export.
- projectKey pattern: `organization-slug.stream-c` (copy from the project URL).
- If MCP is already connected in the demo machine: shorten 00:12–00:48 to a quick “MCP is connected” beat.
