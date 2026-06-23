# 📚 WEEKLY LEARNING & INSIGHTS REPORT — Week of June 17–23, 2026

**Generated:** 2026-06-23 (end of week)
**Sources:** 7 × `INTEGRATED_INSIGHTS` files (Jun 17–23)
**Coverage:** 7 days, 46 cron jobs, 50+ team members, 3 monitored subjects

---

## 1. EXECUTIVE SUMMARY

This week's dominant theme: **reliability improving, debt accumulating.** Cron SLA climbed from a mid-week low of 53% to 76.7% by Monday, but the same security and health logging failures are now running unaddressed for 6–8 consecutive audit cycles. The WhatsApp bridge (60+ days offline), H's health data gap (11+ days), and Content Pipeline (0 posts for 4 consecutive weeks) represent the three largest systemic risks.

---

## 2. KEY METRICS TREND

| Day | Cron SLA | H Health Gap | Comfort Gap | Security FAIL |
|-----|----------|-------------|-------------|---------------|
| Mon 16 | ~91% | 9 days | 0 (full day) | 3 |
| Tue 17 | ~70% | 7 days | 0 (full day) | 3 |
| Wed 18 | 53% | 8 days | ~36h | 3 |
| Thu 19 | ~60% | 9 days | 8 days | 4 |
| Fri 20 | ~60% | 10 days | 4 days | 4 |
| Sat 21 | ~73% | 12 days | 6 days | 3 |
| Sun 22 | ~73% | 10 days | 6 days | 3 |
| **Mon 23** | **76.7%** | **11 days** | **7 days** | **7** |

**Takeaway:** Cron reliability improved meaningfully after Wednesday. However, security findings worsened (5 → 7 FAIL items by June 23), and health log gaps reached new highs before partially recovering.

---

## 3. IDENTIFIED PATTERNS

### **Pattern A: DNS Resolution — The #1 Cron Failure Mode**

| Day | DNS Failures | Hours Affected | Cron Jobs Impacted |
|-----|-------------|---------------|-------------------|
| Jun 18 | Morning burst | 09:16–09:27 | Health check-ins |
| Jun 19 | Evening OUTAGE | 21:34–22:03 (29 min) | Telegram delivery |
| Jun 19 | OpenRouter DNS | 22:00 (3 retries) | Inventory sync |
| Jun 20 | Morning burst | 08:38–09:11 | Health check-ins |
| Jun 20 | Multiple throughout day | Variable | 8+ jobs |
| Jun 22 | Afternoon cluster | 12:04–18:00 | Inventory sync |
| Jun 23 | Evening cluster | 19:00 | 5 jobs |

**Cumulative `getaddrinfo failed` errors:** 3,065+ by Jun 20 and rising.

**Root cause:** Network/DNS infrastructure (router/ISP level), not Hermes configuration.

**Actionable Improvement:**
- Configure static DNS (8.8.8.8, 1.1.1.1) on the Windows network adapter
- Implement DNS-aware retry with exponential backoff in cron jobs that use `httpx`/`curl`
- Consider a cron job that monitors DNS health independently and alerts when degradation begins

---

### **Pattern B: WhatsApp Bridge — 60+ Days Down, No Resolution Path**

| Date | Days Down | Jobs Affected | Team Impact |
|------|-----------|--------------|-------------|
| Jun 17 | 47+ | 8+ jobs | Sammy, Kanzoni, John, Jnr, Ebony unreachable |
| Jun 18 | 48+ | 8+ jobs | Same + Discord still paused |
| Jun 19 | 55+ | 8+ jobs | 24 supplier inquiries queued but not delivered |
| Jun 20 | 55+ | 8+ jobs | Telegram fallback functional but incomplete |
| Jun 21 | 56+ | 8+ jobs | WhatsApp bridge shows `whatsapp_not_paired` |
| Jun 22 | 60+ | 8+ jobs | 20+ consecutive Sammy failures; Jnr 10+ sends |
| Jun 23 | 60+ | 8+ jobs | Gateway log stale 5+ days |

**Root cause:** `creds.json` missing + `channels.whatsapp.enabled: false` in openclaw.json. Gateway BOM (UTF-8 BOM in `openclaw/package.json`) also blocking gateway restart. QR re-pairing required but H hasn't done it.

**Actionable Improvement:**
1. Decision required from H: **re-pair** (requires interactive QR scan via `hermes whatsapp`) OR **formally disable** all 8 WhatsApp-dependent jobs and document the decision
2. Until resolved, configure **Telegram as primary** for all these jobs (not a fallback) — Benny fallback has been working but it's labeled as fallback
3. Consider creating a `JOB_STATUS_WHATSAPP.md` flag file that abstracts delivery routing so jobs don't need individual updates when the channel changes

---

### **Pattern C: Health Log Gaps — Systematic Monitoring Failure**

#### H (Oman Herbert Blankson)
- Last entry: June 10 → grew to **12-day gap** by Jun 21
- Electrical shock incident (Jun 12) — **no medical evaluation ever completed**
- Morning/afternoon check-ins consistently failing via DNS/connection errors
- Evening check-in: sent but no response captured (no `send_message` in cron sessions)
- **Risk:** 🔴 HIGH — missing health trend data, unreviewed head injury

#### Comfort (Mum, 91)
- Last full care log: June 16 (6–8 day gap)
- Severe insomnia (no sleep all night Jun 15–16), BP spike 149/80 AM → normalized PM
- Thumb swelling improving, leg swelling stable (furosemide)
- Critical low water intake (~440ml vs 1.5L target), Ferguson protocol violations (eggs 5× in 3 days)
- Golden Milk added to evening plan (Jun 17)
- **Risk:** 🔴 HIGH — CKD Stage 3b, uncontrolled BP, care log gaps

#### Dad (Robert, 92)
- All 5 dad-health jobs disabled since June 4
- Zero care log data for June
- **Risk:** ⚪ UNKNOWN — no monitoring mechanism

**Actionable Improvement:**
1. **Escalate H's electrical shock** — if 2+ weeks pass without follow-up, assume this needs external medical review
2. **Evening check-in loop must read responses back** — current architecture sends via Telegram but `send_message` is unavailable in cron sessions, so responses never write to log files
3. **Comfort carer coordination** — the 6-day gap suggests the carer isn't receiving/responding to evening prompts. Verify Telegram delivery confirms AND add automated escalation (if no response for 2 days, flag to H)
4. **Formal decision on dad-health** — re-enable jobs OR officially document paused status and communicate to stakeholders

---

### **Pattern D: Security Debt — 6–8 Audit Cycles Without Remediation**

| Finding | First Seen | Cycles Unfixed | Severity |
|---------|-----------|----------------|----------|
| `bws_cache.json` — 15 plaintext API keys | Jun 22 | 4+ | CRITICAL |
| All sensitive files world-readable (0644) | Jun 20 | 4+ | CRITICAL |
| 14–19 `.env` backup copies with live keys | Jun 13 | 8+ | HIGH |
| Google token expired Jun 20 | Jun 20 | 4+ | HIGH |
| AGENTS.md BOM (UTF-8 BOM) | Jun 21 | 6+ | HIGH |
| WhatsApp bridge unpaired 60+ days | Jun 7 | 8+ | HIGH |
| Telegram InvalidToken event Jun 8-9 | Jun 8 | 1+ | HIGH |
| Gateway log stale 120h+ | ongoing | many | HIGH |

**Trend line:** Two new CRITICAL findings appeared Jun 22 (bws_cache.json escalation) and Jun 23 (InvalidToken). The audit itself is failing occasionally (Jun 20 evening, Jun 21 evening, Jun 22 evening all had connection errors).

**Actionable Improvement:**
1. **Blockbuster security day:** Allocate 1 dedicated session (not cron) to address the 3 CRITICAL items — delete bws_cache.json, chmod 600 on sensitive files, strip BOM from AGENTS.md
2. **Automate permission remediation:** Add a cron job that runs `chmod 600` on `.env`, `auth.json`, `google_token.json` and alerts on failures
3. **Break the audit cycle loop:** When an audit finding persists for >3 cycles, automatically downgrade to "ACKNOWLEDGED — awaiting H decision" or escalate to a named Slack/Telegram task card

---

### **Pattern E: Content Pipeline — 4 Consecutive Weeks of Zero Posts**

- Week 25: 194+ assets generated, **0 posted**, GHC 0 revenue
- Content engine last ran Jun 21 (generated 11 images, 28 captions, 2 videos)
- Blockers: No posting automation, no H review/approval for 4 weeks
- 140 planned posts across 4 weeks: all undelivered

**Actionable Improvement:**
1. Build a **review gate** — content assets should require H/team approval before being marked "ready to post"
2. Automate the **publish step** — once approved, schedule to FB Marketplace, Instagram, and 2Real channels
3. Add a review SLA — if content sits unapproved for >48h, escalate

---

### **Pattern F: Recruitment — Healthy Baseline**

- 52 applicants stable (39 nurses, 8 construction, 3 facilitators, 2 financial literacy)
- Google Sheets auth restored Jun 20
- Charlotte Nortey remains top candidate (NMC + car + licence + 3-5 yrs)
- New applicants: Ibrahim Yakubu sose (BECE, no NMC — screening decision pending)
- **Status:** 🟢 Low-risk area; no urgent action needed

---

## 4. KEY LEARNINGS

### Learning 1: DNS Failures Are Infrastructure, Not Configuration
Since Jun 13, DNS problems have consistently disrupted 25–40% of daily cron runs. The pattern (morning window most vulnerable, evening windows also affected) strongly suggests router/ISP-level DNS resolver issues. This isn't fixable by changing Hermes config alone — it needs OS-level network configuration or a network-level fix.

### Learning 2: Telegram Fallback Works, but Shouldn't Be a Fallback
The Telegram fallback pattern (sending to Telegram topic when WhatsApp fails) is **reliable enough to be the primary channel** for most jobs. Configuring it as fallback means jobs still show as "failed" in cron status even when they delivered successfully via Telegram. Change the mental model: Telegram is primary, WhatsApp is secondary.

### Learning 3: Cron Jobs Send Messages but Never Receive
The architecture allows cron agents to send Telegram messages, but **no cron job can call `send_message`** in a headless session. This means health check-in prompts go out, but caregiver/H responses that come back via Telegram DMs are not captured back into log files. This is a fundamental gap in the monitoring loop.

### Learning 4: Unaddressed Security Findings Are the Highest-Risk Pattern
bws_cache.json and the plaintext `.env` backups mean a single system compromise or backup leak exposes 30+ API keys (OpenRouter, Telegram, Google, Firecrawl, Bitwarden, etc.). The `.env` backup count actually *improved* slightly (19 → 14), which gives false hope — the ACTIVE bws_cache.json is the bigger risk.

### Learning 5: WhatsApp Dependency is a Silent Kill
Every day the WhatsApp bridge stays down, more operations fade:
- Supplier inquiries queue but never send
- Sammy/John/Kanzoni field ops become black holes
- Ebony goodnight messages fail silently
- Jnr payment reminders require manual Telegram fallback

The cost is mostly invisible (no errors, just missing outputs) until someone notices the volume of uncompleted tasks.

---

## 5. ACTIONABLE IMPROVEMENTS (Ranked by Priority)

### 🔴 CRITICAL — This Week

| # | Action | Owner | Blocker |
|---|--------|-------|---------|
| 1 | **Delete `bws_cache.json`** — `rm ~/.hermes/cache/bws_cache.json` | H / agent | Permissions |
| 2 | **Strip UTF-8 BOM from `AGENTS.md`** — blocking 10+ cron jobs | H / agent | Admin PowerShell |
| 3 | **Fix gateway BOM** — `openclaw/package.json` BOM blocks gateway startup | H | Admin PowerShell |
| 4 | **Complete H medical evaluation** — Electrical shock Jun 12, 11+ days unreviewed | External doctor | H coordination |
| 5 | **Decision: Re-pair or disable WhatsApp bridge** — 60+ days down | H | Interactive QR scan |
| 6 | **Implement health response loop** — evening check-in responses must write to logs | Agent | Tooling gap |
| 7 | **Restore Comfort care log coverage** — 7-day gap; verify carer is receiving prompts | Care team | Channel verification |

### 🟡 HIGH — Next 2 Weeks

| # | Action | Owner |
|---|--------|-------|
| 8 | **Configure static DNS** — 8.8.8.8 / 1.1.1.1 on Windows network adapter | H / agent |
| 9 | **Restrict sensitive file permissions** — `chmod 600` on `.env`, `auth.json`, `google_token.json` | Agent |
| 10 | **Verify/rotate Telegram bot token** — InvalidToken event Jun 8–9 | H / agent |
| 11 | **Improve backup health** — verify daily job reliability; backup Jun 22 recovered but prior gap was 6 days | Agent |
| 12 | **Flash content review** — Review 194+ assets and schedule posting workflow this week | H / agent |
| 13 | **Set dad-health decision** — Re-enable jobs or document formal pause | H |

### 🟢 LOW — This Month

| # | Action | Owner |
|---|--------|-------|
| 14 | **Audit stale cron jobs** — Disable or fix 8 jobs with >7 day gaps | Agent |
| 15 | **Fix Telegram delivery routing** — Change `origin` to explicit `telegram:-1003784520976:10` for failing jobs | Agent |
| 16 | **Build security debt tracker** — Auto-flag findings persisting >3 audit cycles | Agent |
| 17 | **Content pipeline automation** — Approval gate + publish automation | Agent |
| 18 | **NPM vulnerabilities** — 3 high, 4 moderate, 2 low; patch dependencies | Agent |

---

## 6. WEEKLY TREND ANALYSIS

```
Cron SLA:  ████████████████████░░░░░░░░░░ 76.7% (↑ from 73%)
Health:    ███████████████░░░░░░░░░░░░░░  Concerns at all-time high
Security:  ██████████░░░░░░░░░░░░░░░░░░  3→7 FAIL items, worsening
Business:  ██████████████████░░░░░░░░░░  Operational but channel-starved
Content:   ██████░░░░░░░░░░░░░░░░░░░░░░  4th week of zero posts
```

**Overall verdict:** The week ended stronger than it started, but the underlying issues (security debt, DNS instability, channel failures) are getting worse, not better. The "improvement" in SLA is primarily because fewer jobs are enabled/attempting, not because the infrastructure became more reliable.

---

## 7. CROSS-CUTTING RECOMMENDATIONS

1. **Single weekly "Infrastructure Health" audit** — Instead of 6-hourly security audits producing stale findings, consolidate to a single comprehensive weekly audit that produces a standalone "actions required" list with owners and deadlines.

2. **Channel abstraction layer** — The current pattern of hardcoding Telegram/WhatsApp in each cron job's config means switching channels requires editing 10+ files. A single `CHANNEL_CONFIG.md` with routing rules would make bridge failures less painful.

3. **Health monitoring SLA** — Both H and Comfort have hit 10+ day gaps. If a health check-in fails 2 consecutive days, escalate to named human (not just another cron job).

4. **End the audit cycle without action** — Same findings appearing 6–8 cycles in a row means the audit is generating noise, not signal. Either resolve the items, suppress known risks, or downgrade to ADR-status.

5. **Latent risk inventory** — bws_cache.json, inactive dad-health jobs, 14 .env backup copies — these are all risks that exist silently. Maintain a public "residual risk" register so stakeholders see what's known and intentionally deferred.

---

*Report saved to: `C:\Users\User\.hermes\workspace\memories\insights\WEEKLY_LEARNING_2026-06-23.md`*
*Next weekly review: 2026-06-30*
*Sources: 7 × INTEGRATED_INSIGHTS files (Jun 17–23) + health logs + security audits + business checkins*
