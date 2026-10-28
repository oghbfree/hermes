# 🤖 BOT JOB SPECS — the contract for every agent (28/10/26)

> H's principle ("document your workflows") in practice: **every bot has a written JOB DESCRIPTION before it acts.** Each spec covers Role, Trigger, Inputs, Steps, Output, Tool Access, Must-Never, Escalate, Metric. Read YOUR spec before any work. If a task isn't in your spec, you don't do it autonomously — you hand it to sat-nav.

## The 9 fields (use this exact order)
1. **ROLE** — who this bot is, in one line.
2. **TRIGGER** — what starts it (message tag, cron, time).
3. **INPUTS** — the files/channels it reads (real paths only).
4. **STEPS** — the ordered procedure.
5. **OUTPUT FORMAT** — the shape of the deliverable (terse; H reads it).
6. **TOOL ACCESS** — what it may touch (workspace, tools).
7. **MUST NEVER** — the hard no's (approval gates, no-send zones).
8. **ESCALATE** — when to stop and hand to sat-nav / flag H.
9. **METRIC** — how success is measured.

## Files in this folder
- `sat-nav.md` — Chief of Staff / CEO front door / CFO role
- `content-buddy.md` — Kofi · copy, captions, ad creative
- `coach.md` — networking + group strategy
- `taiwah.md` — brand voice / face content
- `hermes.md` — OG gateway / delivery infrastructure
- `harold.md` — local gemma4 (draft-level only — NOT an executor)
- `GUARDRAILS.md` — approval gates, allowed-actions, daily summary, audit log, kill switch, spend ceiling
- `CORRECTIONS_LOG.md` — every correction logged; repeated ones become SOP rules
- `AUDIT_LOG.md` — append-only record of agent actions

## Operating modes (per H, 28/10/26)
- **DRAFT-ONLY is the default** for anything customer-facing or external: the agent PREPARES the message/update, H SENDS. No bot publishes, spends, or sends externally without an approval gate.
- **Log every correction.** At review time, repeated corrections (≥2 same-rule violations) become a written rule in the SOP. This loop is the fix for underperforming agents.

## Master SOP
`Vault/business/2real/2real-agent/HOUSE_RULES.md` — the shared doctrine every bot loads (CTA 0204252252, Jiji=truth, Godin, no-fabrication, SlopMonster 5/5, one front door).
