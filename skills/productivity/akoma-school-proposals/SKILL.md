---
name: akoma-school-proposals
description: "Draft school partnership proposals for Akoma Robotics — school-integrated and after-school models. Use when H asks to create, revise, or send a proposal to a school for robotics/AI education programs."
---

# Akoma School Proposals

Draft and iterate on school partnership proposals for Akoma Robotics programs.

## Models

**Track A: After-School Club (Standalone)**
- Parent pays directly (GH¢800-1,000/student)
- School provides venue only
- Voluntary opt-in enrollment
- School earns 20% commission

**Track B: School-Integrated Program**
- Fee rolled into school fees (GH¢200/student/term)
- Whole class/year group participates
- School collects via existing billing
- School earns 10% (GH¢20/student/term)
- Net to Akoma: GH¢180/student/term

## Standard Proposal Structure

1. **Header** — "AKOMA ROBOTICS — SCHOOL-INTEGRATED PROGRAM PROPOSAL" + school name
2. **The Model** — 4 bullet points explaining how it works
3. **Equipment Logistics** — Transport model (no on-site storage), consolidation plan
4. **What's Included** — 12-week term checklist + curriculum phases
5. **Pricing** — Table (keep minimal; per-student rate only unless school-specific rows needed)
6. **Why This Works For [School]** — 5-6 bullets tailored to the school
7. **Comparison: Old vs New** — Table contrasting previous proposal with new
8. **Next Steps** — 5 numbered action items

## Curriculum (12 Weeks)

- Weeks 1–4: Foundations (assembly, mBlock coding, sensors, obstacle avoidance)
- Weeks 5–8: Sensors & Control (line following, remote, sensor fusion, project kickoff)
- Weeks 9–10: AI Awareness (what is AI, smart sensors, ML concepts)
- Weeks 11–12: Project & Showcase (build, test, present, certificates)

## Pricing Rules

- Default: GH¢200/student/term integrated; GH¢800-1,000 standalone
- School share: 10% integrated; 20% standalone
- Keep pricing table minimal — per-student rate only unless asked for class-size rows
- Never include both class-size rows AND full-year rows — user prefers lean tables

## Equipment Logistics (Default)

- Akoma does NOT store equipment on-site
- Transport to/from each session
- Evaluate uptake for consolidated whole-school day model

## File Storage

Save proposals to: `C:\\Users\\User\\.hermes\\workspace\\memories\\business\\akoma\\proposals\\`
Naming: `<school-name>-<model-type>.md` (e.g., `royal-zion-intl-school-integrated.md`)

**Note:** User moved all business files (including proposals) to the `memories/business/` directory. Do NOT use a top-level `akoma/` folder — it was deleted. Everything lives under `.hermes/workspace/memories/business/akoma/`.

## PDF Generation

To convert a proposal to PDF:
1. Use the bundled `scripts/md_to_pdf.py` converter
2. Run via `terminal(python ...)` — do NOT use `execute_code` (sandbox lacks reportlab)
3. System Python has reportlab: use `python` (not `python3`) on this Windows host
4. Syntax: `python <skill_dir>/scripts/md_to_pdf.py <input.md> <output.pdf>`
5. Send the PDF via `send_message` with `MEDIA:<path>`

## Iterative Refinement Pattern

Proposals are built iteratively. Expect:
- Commission rate changes (default 10%)
- School name corrections
- Pricing table row deletions (user prefers minimal tables)
- Always show the full updated proposal after changes
- Always confirm before saving

## Key Context

- Previous proposals to Royal Zion International School were GH¢800/student after-school — rejected as too expensive
- The integrated model replaces that with GH¢200/student/term via school fees
- Akoma provides: facilitator, mBot kits, curriculum, equipment transport, certificates
- School provides: classroom space
