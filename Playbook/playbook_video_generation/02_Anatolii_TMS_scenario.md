# TMS walkthrough — voiceover script

| | |
|---|---|
| **Author** | Anatolii |
| **Part** | 2 of 4 (full playbook video) |
| **Target duration** | ~4:00–4:30 |
| **Covers** | Playbook Shots 2–4 (preloaded streams → Stream C → TMS by hand) |
| **Previous** | [01 — Organizations (Vika)](01_Vika_part1_scenario.md) |
| **Next** | [03 — MCP at scale (Ilya)](03_Ilya_MCP_scenario.md) |
| **Then** | [04 — Portfolio dashboard (Vika)](01_Vika_part2_scenario.md) |
| **Playbook** | `#streams` · `#stream-c` · `#library` · `#planning` · `#launches` · `#walkthrough` Shots 2–4 |

**Style:** spoken demo, present tense, short sentences (match Vika Part 1).

**Record:** silent screencast; voiceover from the script below.

**Out of scope:** Organizations setup, MCP API / Cursor setup, LOY-003 (→ Ilya), portfolio dashboard / GO–NO-GO.

---

## Script

**00:00**  
At the project level, every stream in ReportPortal runs the same Test Management path.  
Write scenarios once. Scope them for a sprint. Execute in a launch.  
That's the loop you'll walk today — first in streams that are already loaded, then in one you create yourself.

**00:18**  
Inside your dedicated beta org — not Personal — Playbook is already loaded: a synthetic hotel-booking product split across two teams.  
Stream A covers search, cancellations, and mobile. Stream B covers checkout and payment.  
*[On screen: Projects list — Stream A, Stream B — open Stream A]*

**00:32**  
The Test Case Library is the source of truth. Open Search & Filters in Stream A.  
Compare TMS-BOOK-001 — a Steps case — with TMS-BOOK-004 — a Text case.  
Same library. Two ways to describe a scenario.  
Tags like smoke and search sit on the case — search by TMS-BOOK in the name, not by folder number.

**00:52**  
Switch to Stream B. Open TMS-BOOK-010 — room selection into checkout — and TMS-BOOK-013 — happy-path payment.  
Two streams. Isolated libraries. No mixing.

**01:08**  
Milestones time-box the work. Test plans group cases for one goal.  
In Stream A you'll see search and cancellation coverage. In Stream B — smoke and payment plans.  
*[On screen: quick cut — Milestones / Test Plans in A or B]*

**01:22**  
Manual Launches are where execution lives — per-case status, comments, attachments.  
Here: passed smoke on TMS-BOOK-010 and 013.  
Here: failure evidence — a comment on TMS-BOOK-002 in Stream A, or TMS-BOOK-018 in Stream B.  
And cases still TO_RUN — like mobile TMS-MOB-001 — ready for a live mark.

**01:42**  
Library → Milestone → Test plan → Manual launch.  
Stream A and B already show that path. Now you run it end to end — in a clean stream.

**01:54**  
Back in your organization: Projects → Create project → name it Stream C → open and join.  
The library is empty on purpose. This is your practice ground.  
*[On screen: Create Stream C]*

**02:08**  
In Stream C, create a folder — Loyalty & Reviews.  
Add two cases — copy the names exactly:  
TMS-LOY-001 — Earn loyalty points after a confirmed booking — Text type.  
TMS-LOY-002 — Redeem points at checkout — Steps type.  
Add a loyalty tag. These IDs stay stable when you use MCP later.

**02:32**  
Create a milestone — Sprint 26 — Loyalty — and a test plan — Loyalty smoke — with both cases on it.  
Your sprint is scoped. Ready to execute.

**02:48**  
Start a manual launch from Loyalty smoke. Open TMS-LOY-001. Mark it Passed. Add a short comment if you want.  
You just completed the full TMS loop by hand — in your own project.

**03:08**  
One organization. Three streams. Each owns its library and results. Access stays per project.  
You walked Library → Plan → Launch once, by hand, in Stream C.  
Everything you created here will roll up when leadership looks at quality across the org.

**03:28**  
Same path — more cases, more launches — without clicking through every wizard.  
That's what MCP and an AI assistant do next. Same workflow, at agent speed.

**03:42**  
*[Hard cut → Ilya — Shot 5: MCP setup, TMS-LOY-003, plan + launch via agent]*

---

## Shot list (silent recording)

| Block | Time | On screen |
|-------|------|-----------|
| Bridge + Playbook | 00:00–00:32 | Stream A/B in project list |
| Shot 2 · Preloaded | 00:32–01:42 | A: 001/004; B: 010/013; plans; launches (Passed + failure + TO_RUN) |
| Shot 3 · Stream C | 01:54–02:08 | Create project Stream C |
| Shot 4 · By hand | 02:08–03:08 | Folder, LOY-001/002, milestone, plan, launch → Passed |
| Handoff to Ilya | 03:08–03:42 | Wide shot: org / three projects / Stream C library |

---

## Notes

- ~480 words → ~4:00–4:30 at calm demo pace.
- Do **not** repeat Vika Part 1: org pain, All Organizations, user management.
- Do **not** cover MCP API key, Cursor setup, or LOY-003 — Ilya (Shot 5).
- Do **not** cover portfolio dashboard or GO/NO-GO — Vika Part 2.
- If Stream C already exists: say “Open Stream C — your practice stream” instead of Create.
- Invite colleague: skipped (optional in playbook; Vika Part 1 already shows Organization users).
