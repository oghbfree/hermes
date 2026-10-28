# 🛡️ GUARDRAILS — control framework for every bot (28/10/26)

> **Before autonomy: approval gates, allowed-actions, daily summary, audit log, kill switch, spend ceiling.** Draft-only by default. Autonomy is granted per-job by H, never assumed.

## 1. Approval gates — required for anything that…
| Action type | Gate |
|---|---|
| **Sends external** (WhatsApp/Telegram/Jiji/FB/email post or DM to customer/third party) | 🔴 H approves the exact text first (draft → H sends, or H says "send") |
| **Spends money** (buying stock, ads, MoMo, rider pre-pay, subscriptions) | 🔴 H approves amount + vendor before any purchase |
| **Publishes** (listing, post, status, group paste, invoice sent) | 🔴 H approves the artifact (SlopMonster 5/5 + real photo + CTA audited) |
| **Deletes / changes price / discounts** | 🔴 H only (business rule: no discounts without H) |
| **Creates/edits cron jobs, skills, memory, credentials** | 🔴 sat-nav owns config; bots never self-modify their spec |
| Owner-number messages (wife 0546081608, Mum's nurse 0548236698 etc.) | 🔴 special rules (owner bypass / silent intake) apply — see HOUSE_RULES |

## 2. Allowed-actions list (per bot)
- A bot may ONLY perform actions listed in its `BOT_JOB_SPECS/<bot>.md` STEPS. Anything else = hand to sat-nav.
- Environment-scoped: bots write to their assigned vault folder(s); never outside their workspace unless the task says so and it's read-only.

## 3. Daily summary (what the agent did)
- The **CoS Daily Bot Digest** (cron `d09cf3095329`, weekdays 08:00, TG topic 1) already reports: ✅ what got done · ⚠️ what needs H's OK · 🎯 do-first. Every bot's accountability answer.
- Bots that ran autonomously during the day must surface their completed actions in that digest (or a log line in AUDIT_LOG.md).

## 4. Audit log — append-only
- `AUDIT_LOG.md` — one line per agent action: `DATE | BOT | ACTION | RESULT`. Written by the acting bot after any state-changing action (send, publish, spend, config edit). H or sat-nav can read it anytime.

## 5. Kill switch
- **"Stop <bot>" / "pause <bot>"** from H = immediate halt of that bot's autonomous work (crons paused, drafts stopped, no new DMs).
- Global: **"Stop all bots"** = halt everything except sat-nav's passive logging. Each bot spec lists its own override line.

## 6. Spend ceiling on model usage
- **Cheap tier first** (Ollama local = $0) → hands (deepseek) → brain (GLM) only when the task needs it. `model_router.py route <kind>` enforces.
- Per-agent daily cap: default **$0.50/day** unless H raises it (recorded in the bot's spec). No bot may burn a paid model on high-volume/low-stakes work.
- Track: OpenRouter dashboard + cron usage audit (CFO role). Any over-run is flagged in the CFO Dashboard's USAGE AUDIT.

## 7. Draft-only default
- Unless a bot's spec says "AUTONOMOUS: <exact scope>" in writing from H, the bot PREPARES and H SENDS. No exceptions by convenience.
