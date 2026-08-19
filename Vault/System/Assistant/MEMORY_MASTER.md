# MEMORY_MASTER.md — Central Memory Index

> **Purpose:** Single source of truth coordinating all memory, security, and system files.
> **Created:** 2026-08-19 (consolidated from context.md, preferences.md, environment.md, MEMORY.md)
> **Last Updated:** 2026-08-19

---

## 🔗 Canonical File Map

| Domain | File | Purpose |
|--------|------|---------|
| **Memory (hot)** | `~/.hermes/memories/MEMORY.md` | Hermes tool-managed memory (2,200 char limit) |
| **User Profile** | `~/.hermes/memories/USER.md` | User preferences & identity |
| **SOUL** | `~/.hermes/SOUL.md` | Agent identity & core rules |
| **System Context** | `Vault/System/Assistant/context.md` | Life situation, health, operations |
| **System Preferences** | `Vault/System/Assistant/preferences.md` | Communication style, routing |
| **System Environment** | `Vault/System/Assistant/environment.md` | Hardware, paths, troubleshooting |
| **Issues & Fixes Log** | `Vault/System/Assistant/logs/issues-fixes-log.md` | Recurring issue tracking |
| **Security Audits** | `Vault/System/Assistant/` (SECURITY_AUDIT_*.md) | Security audit reports (7-day retention) |
| **Obsidian Vault** | `Vault/` | All operational data |

---

## 👤 User Profile Summary

**Name:** H (Oman Herbert Blankson)
**Time:** Ghana (GMT/UTC) + London property
**Role:** Portfolio entrepreneur — 2Real Enterprises, Akoma Robotics, Property, Farm
**Style:** Direct, no fluff, concise. Act first, confirm back.
**Identity:** When messaging anyone, act as H directly (first person). Never reveal AI.

---

## 🧠 Memory State (from Hermes MEMORY.md)

**Canonical Paths:**
- Memory: `C:\Users\User\.hermes\memories\MEMORY.md`
- User Profile: `C:\Users\User\.hermes\memories\USER.md`
- Workspace: `C:\Users\User\.hermes\workspace`
- SOUL.md: `C:\Users\User\.hermes\SOUL.md`
- Vault: `C:\Users\User\.hermes\workspace\Vault`

**Security (as of Aug 19):**
- bws_cache.json: ✅ PURGED
- Backup .env copies: ✅ 13 removed (0 remaining)
- Remaining: ~33 .env-reader scripts (legacy, being deleted)
- WhatsApp: 🔴 unpaired ~73 days
- Gateway: 🟢 UP PID 12896 (but dual: 12896+17584)
- Token: ✅ VALID (@Ogaitchhermesbot)
- Topic 20: ✅ Present and accepting messages

---

## 📋 Vault Directory Structure

```
Vault/
├── business/
│   ├── 2real/          (SOPs, 2real-agent, inventory, Farming, Nursing)
│   ├── akoma/          (Robotics, proposals, pricing)
│   ├── Content/        (content-assets/, content-output/)
│   ├── construction/   (Property development)
│   ├── Ebay/           (eBay UK)
│   ├── checkins/       (Business check-in logs)
│   └── procurement/
├── family/
│   ├── H/              (Health logs, food master, medical master)
│   ├── mum/            (Care logs, exercises, errands)
│   ├── dad/            (Wellbeing checks, biography)
│   ├── ebony/          (Ebony's info)
│   └── kids/           (Kobena & Nenyi)
├── Daily/              (Daily briefings & processing reports)
├── Inbox/              (Unprocessed items)
├── insights/           (Daily/weekly business & health insights)
├── jobs/               (Recruitment pipeline — nurses, construction, etc.)
├── people/             (Contact management)
├── Personal/           (Personal notes)
├── finance/            (Financial docs)
├── System/Assistant/   (Security audits, context, preferences, environment)
├── archive/            (Archived data)
├── templates/          (Note templates)
├── TASKS.md            (Master task list)
├── tasks-queue.md      (Active task queue)
└── shopping-list.md
```

---

## 🏠 Telegram Topic Routing

| Topic | Name | Vault Path |
|-------|------|------------|
| 1 | General | `Vault/Inbox/` |
| 2 | Health Log (H) | `Vault/family/H/` |
| 4 | Health Log Mum | `Vault/family/mum/` |
| 6 | Container | `Vault/business/2real/` |
| 8 | To-Do List | `Vault/tasks-queue.md` |
| 10 | Briefing | `Vault/Daily/` |
| 12 | Property | `Vault/business/construction/` |
| 14 | Farm | `Vault/business/2real/Farming/` |
| 16 | Action Lab | `Vault/TASKS.md` |
| 18 | Kids | `Vault/family/kids/` |
| **20** | **Memory Review** | **`Vault/System/Assistant/`** |
| 26 | Content Calendar | `Vault/business/Content/` |
| 28 | Jobs | `Vault/jobs/` |
| 424 | Nursing | `Vault/business/2real/Nursing/` |
| 866 | Akoma Robotics | `Vault/business/akoma/` |
| 928 | 2 Real Enterprises | `Vault/business/2real/` |
| 3225 | eBay UK | `Vault/business/Ebay/` |
| 3823 | Dad | `Vault/family/dad/` |
| 5885 | Life | `Vault/Personal/` |

---

## ⏰ Cron Job Pipeline (55 jobs)

**Deliveries to Topic 20 (Memory Review):**
- `security-policy-check` — every 6h → audit report + summary
- `nightly-consolidation` — 03:00 daily → memory review
- `integrated-daily-synthesis` — 22:05 daily (⚠️ MISSING from jobs.json, needs recreation)

**Deliveries to other topics:**
- Topic 2 (Health): health-check morning/afternoon/evening
- Topic 4 (Mum Health): mum-health morning/afternoon/evening, weekly review
- Topic 8 (To-Do): brain-dump-parser
- Topic 10 (Briefing): Market Seller Briefing
- Topic 16 (Dad): 3-day condition check, weekly review
- Topic 26 (Content): sunday-content-engine, saturday-content-performance
- Topic 28 (Jobs): job-applications-check

**Persistent Issues:**
- WhatsApp unpaired ~73 days → ~12 check-in agents silently failing
- 29/55 jobs use `deliver: origin` → silent delivery failure
- Duplicate `eric-property-check-in` deleted Aug 19

---

## 🔐 Security Audit Protocol

- **Frequency:** Every 6 hours (4x daily)
- **Retention:** 7 days, same-day duplicates removed
- **Path:** `Vault/System/Assistant/SECURITY_AUDIT_[DATE].md`
- **Summary delivered to:** Topic 20

**Known persistent findings:**
- WhatsApp unpaired (73+ days) — needs manual QR re-pair
- .env-reader scripts (33 legacy, being cleaned)
- Silent delivery jobs (29/55 use origin/local)

---

## ⚙️ Environment & Technical

| Resource | Value |
|----------|-------|
| OS | Windows 10 |
| Python | 3.11.15 (system) |
| Hermes | Desktop app, default profile |
| Gateway | PID 12896 (⚠️ dual: 12896+17584) |
| Obsidian Vault | `Vault/` |
| State DB | `~/.hermes/state.db` (411 MB) |
| Active Model | openrouter/owl-alpha |
| Fallback | openrouter/qwen/qwen-turbo |

---

*This file is auto-maintained. Update when systemic changes occur.*