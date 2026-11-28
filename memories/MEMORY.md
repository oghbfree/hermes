# MEMORY.md

Durable facts from periodic daily-processing runs.

_facts below are limited to verified findings. Last refreshed: 2026-11-27 (Fri EOD, compiled 03:14 Sat 28 Nov)._

## 2026-11-27 Consolidated (Fri, EOD) — PRUNED over 26 Nov
- 💼 **2Real: FB Marketplace Batch Poster FIXED 27 Nov — 5 posts/day @10:00, schedule verified + QUEUE REFILLED to 600 fresh Jiji items** (old 289 preserved next50.json.backup_20261127_110053; ~Mar 2027 refill). **FB flooder storm now MOOT** (posting resumes). 🔴 **checkin-mum c3db50 STILL ENABLED (empty WA-spam) — KILL still open.** Jiji ~1,404 · WA cat complete/queue 0 · content STALE ~30d.
- 💰 **25 Nov = Ske-man bulk CLEARANCE 3,440 GHS / ~95%† / profit ~3,240†** (10 Amazon bags + 10 non-working TVs + 4 carpets + table + 4 garden machines = 3,000 + sink 300 + spray 10 + back-roller massager 130; **COGS ~186 EXCLUDES bulk, cost TBD — warehouse clearance + faulty goods**). Row in-log dated "27/11 Wed" = weekday Wed ⇒ **25 Nov (typo)**. → **ONLY 17 + 20 + 26 + 27 Nov rows UNLOGGED** (now 4 working-day gaps). Warehouse-turnover strategy working.
- 👵 **Mum: 🟠 silent-report gap WIDENING — no inbound since 24 Nov 20:09 (25–28 Nov + 18–19 Nov = ~6 unaccounted days in 2 wks).** Last vitals 24 Nov **BP 122/85 · P80 · T36.4** (diastolic high-normal). BP streak clean all captured (9→13→14→16→20→21→22→23→24 Nov); **Furosemide stop-rule (<100/>140 RIGHT arm) NEVER fired.** ⚠️ **Imodium STILL OUT (11+ wks; 23 Nov diarrhoea ×3; Na 161 + Furosemide = dehydration risk)**. Na recheck labs overdue · Kenus-spa ask open · **ACTION: H call Stephanie 0548236698** to restore care-report flow.
- 🦷 **H (52): 🔴 15-DAY food-diary gap (14–28 Nov; last 13 Nov).** Renerve ZERO ~61d · 31 Aug review ~89d undocumented · labs (1,075 GH) pending · dental ~47d · **no vitals ~96d** (longest). 🟢 ~60 days acute-free.
- 👴 **Dad:** 🔴 winter jabs unbooked (window ~6 Dec) · ONE GP call closes foot+AAA+PSA+jabs. Check-in retry possible (WhatsApp PASS-ISH).
- 💰 **Hagija 4,000 OVERDUE 25d (DO FIRST)** · Joycelyn 2,500 · content STALE ~30d · WA Ads dark ~39d · VAT 10-M UNCONFIRMED. TAIWAH reel ON HOLD (17 Nov ruling) · face LOCKED MASTER_LOCK.png.
- 🔒 **Security 26 Nov 08:44: 🟡 STABLE** — TG token VALID (getMe), gateway PID 17840 alive, **WhatsApp PASS-ISH** (creds fresh 24 Nov), **0 backup .env copies**, no InvalidToken (all historical), no provider 4xx. Persistent WARNs: Nous Portal revoked (unremediated — `hermes auth add nous`) · dual-root token divergence (stale `~/.hermes/.env`) · Telegram ConnectError flapping 08:42 (3rd+ consecutive cycle, self-healed) · MATRIX_HOME_ROOM UnscopedSecretError → gateway restart · 24/55 silent cron targets · 2 dead-thread Mom jobs → 424.
- 🖥️ **System:** ✅ Backup VERIFIED Mon 23 Nov 03:56 — 16,270 files / 3,503 dirs / 0 errors; **next Sun 30 Nov 23:03**. github-memory-backup 27 Nov 06:02 ✅. Integrated-daily-synthesis (d719cd80fa5b, 5 22 * * *) healthy; this run = overnight 27-Nov fill.

## Superseded daily detail (26 Nov) — pruned
- Full per-day detail preserved in `Vault/insights/INTEGRATED_INSIGHTS_2026-11-2X.md` + `Vault/Daily/2026-11-2X.md` (24, 26, 27 Nov). Carried forward as standing rules: Sun/Mon days-off rule, kidney-capsule=Dr Morris (powdered), FB-poster/checkin-mum flooding, Hagija/Joycelyn, VAT 10-M, WA catalogue done + queue 0, TAIWAH exit-narrative ban, faulty-grinder pattern.

## Standing rules & durable facts (NOT day-specific)
- **SOURCING POLICY (H 24 Oct 2026):** non-stock customer requests INTERNAL-ONLY → hold → `sourcing_log.json` → research → H approves → nothing leaves 2Real.
- **SALES RULE (H 16 Nov 2026):** Sun + Mon = H days off — **NO sales expected; missing rows are NOT gaps, never chase; only log if a sale genuinely happened.** Working week Tue–Sat.
- **Mum med rules:** Furosemide 20mg — **STOP/HOLD if BP <100 or >140 (RIGHT arm, standardise)**. Kidney capsule = AVS Dr Morris med, taken **powdered in water** (liquid NOT taken). Phase-out list (Na 161 / K 5.48): banana, orange, pineapple, groundnut, butter, grains, smoked fish (+ plantain drift flagged).
- **FB doctrine (standing):** 2Real FB Marketplace = H's personal, manually-published; agent holds system-side (Jiji/WhatsApp) only. Page posts = scheduled lane via Professional Dashboard. **27 Nov: H raised batch poster to 5/day @10:00 + refilled 600-queue (fix doc `FB_MARKETPLACE_POSTER_FIX_27NOV26`, refill `FB_QUEUE_REFILL_27NOV26`).**
- **Meta agent trial (NEW 6 Nov):** agent in TEST MODE awaiting first clean trading week; approval gate ~1 full trading week clean; rollback = re-enable Hermes f3228b7ede78 + reactivate whatsapp-customer-gate.
- **Content doctrine — 2Real/Taiwah reels (H 17 Nov 2026 RULING, in DECISION_LOG):** **NO exit / no-longer-importing / clearing / "emptying the container" framing in any reel** — the container was offloaded long ago; goods sit in a **RENTED shop**. Speak of origin as past, rented-shop as present; no invented scarcity deadlines. TAIWAH Christmas brief **ON HOLD** until H adds context. Taiwah face LOCKED to MASTER_LOCK.png.

## Archived (before 2026-11-08)
- Daily consolidation entries 2026-08-18 → 2026-11-07 were **pruned from MEMORY.md** to keep the working store lean. Full per-day detail preserved in `Vault/insights/INTEGRATED_INSIGHTS_<date>.md` and `Vault/Daily/<date>.md`.

## System
- Canonical vault path: `C:\Users\User\.hermes\workspace\Vault\`.
- Python full path: `C:\Users\User\AppData\Local\Programs\Python\Python314\python.exe` (uv-managed cp311 on PATH).
- **Current live state (27 Nov 2026 EOD):** Gateway TG up (PID 17840) · **Security 26 Nov STABLE (TG VALID, 0 .env; WhatsApp PASS-ISH creds fresh; Nous Portal revoked; TG morning flapping self-healed)** · **FB poster FIXED+REFILLED 27 Nov (5/day); checkin-mum c3db50 still enabled — KILL** · **Mum no inbound since 24 Nov (~6 unaccounted days; Imodium OUT; H call Stephanie 0548236698)** · **H food gap 15d RED, Renerve ZERO ~61d** · **2Real: 25 Nov Ske-man 3,440 LOGGED (row dtd 27/11 typo); 17/20/26/27 Nov UNLOGGED; Hagija 4,000 OVERDUE 25d** · WA cat done · Jiji ~1,404 · content STALE ~30d · **Backup RAN 23 Nov 03:56 (16,270 files, 0 errors); next Sun 30 Nov 23:03** · cron model pinned deepseek-v4-flash.
- Integrated-daily-synthesis job (`d719cd80fa5b`, `5 22 * * *` daily) present and healthy; delivers to Telegram topic 20.